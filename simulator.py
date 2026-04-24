import re
import os
from collections import defaultdict


class Process:
    def __init__(self, PID, arrival, priority, bursts):
        self.PID = PID
        self.arrival_time = arrival
        self.priority = priority
        self.original_priority = priority

        # bursts = list of bursts, each burst is a dict:
        #   {'type': 'CPU', 'instructions': [('R',rid,amt)|('F',rid,amt)|('CPU',dur)]}
        #   {'type': 'IO',  'duration': N}
        self.bursts = bursts
        self.burst_index = 0        # which burst we are in
        self.instr_index = 0        # which instruction inside current CPU burst
        self.cpu_timer = 0          # countdown for current CPU sub-burst

        self.state = "NEW"
        self.held_resources = defaultdict(int)
        self.waiting_for = None     # (rid, amt) if WAITING

        self.io_timer = 0           # countdown for IO burst

        self.start_time = -1
        self.finish_time = 0

        self.cpu_time_used = 0
        self.total_waiting_time = 0     # time spent in READY queue
        self.resource_waiting_time = 0  # time spent in WAIT queue

        self.quantum_used = 0
        self.ready_timer = 0        # for aging
        self.aging_count = 0

        self.is_deadlocked = False


def parse_file(filename):
    """
    Parse input file.
    Returns (resources_dict, list_of_Process).

    Each Process has self.bursts = list of burst dicts:
      CPU burst: {'type':'CPU', 'instructions': [...]}
        instructions: ('R', rid, amt) | ('F', rid, amt) | ('CPU', duration)
      IO  burst: {'type':'IO', 'duration': N}
    """
    if not os.path.exists(filename):
        print(f"File '{filename}' not found.")
        return None, None

    with open(filename, 'r') as f:
        lines = [l.strip() for l in f if l.strip()]

    if not lines:
        return None, None

    # --- parse resource line ---
    resources = {int(a): int(b)
                 for a, b in re.findall(r'\[\s*(\d+)\s*,\s*(\d+)\s*\]', lines[0])}

    processes = []
    for line in lines[1:]:
        # split into: PID  ArrivalTime  Priority  <rest>
        parts = line.split(maxsplit=3)
        if len(parts) < 4:
            continue
        pid     = int(parts[0])
        arrival = int(parts[1])
        prio    = int(parts[2])
        rest    = parts[3]

        bursts = []
        # find all top-level CPU{...} and IO{...} blocks IN ORDER
        for btype, content in re.findall(r'(CPU|IO)\s*\{([^}]+)\}', rest, re.IGNORECASE):
            btype = btype.upper()
            if btype == 'IO':
                # IO burst: single integer duration
                m = re.search(r'(\d+)', content)
                if m:
                    bursts.append({'type': 'IO', 'duration': int(m.group(1))})
            else:
                # CPU burst: sequence of R[rid,amt], F[rid,amt], or plain integers
                instructions = []
                # split on commas that are NOT inside brackets
                tokens = re.split(r',\s*(?![^\[]*\])', content)
                for token in tokens:
                    token = token.strip()
                    if not token:
                        continue
                    r_match = re.match(r'R\s*\[\s*(\d+)\s*,\s*(\d+)\s*\]', token)
                    f_match = re.match(r'F\s*\[\s*(\d+)\s*,\s*(\d+)\s*\]', token)
                    n_match = re.match(r'^(\d+)$', token)
                    if r_match:
                        instructions.append(('R', int(r_match.group(1)), int(r_match.group(2))))
                    elif f_match:
                        instructions.append(('F', int(f_match.group(1)), int(f_match.group(2))))
                    elif n_match:
                        instructions.append(('CPU', int(n_match.group(1))))
                    # else ignore unknown tokens
                bursts.append({'type': 'CPU', 'instructions': instructions})

        processes.append(Process(pid, arrival, prio, bursts))

    return resources, processes


# ---------------------------------------------------------------------------
# Deadlock detection: Banker's-style resource-allocation graph reduction
# ---------------------------------------------------------------------------
def find_deadlock(available, all_procs):
    """
    Returns list of PIDs that are in a deadlock cycle.
    Only processes in WAITING state can be in a deadlock.
    """
    work = available.copy()

    # Add back resources held by non-waiting processes (they are not blocked)
    finish = {}
    for p in all_procs:
        if p.state == "TERMINATED":
            finish[p.PID] = True
        elif p.state == "WAITING":
            finish[p.PID] = False   # may or may not be satisfiable
        else:
            # RUNNING / READY / IO: not blocked, treat as done for this check
            for rid, amt in p.held_resources.items():
                work[rid] += amt
            finish[p.PID] = True

    changed = True
    while changed:
        changed = False
        for p in all_procs:
            if not finish[p.PID] and p.state == "WAITING":
                rid, amt = p.waiting_for
                if work.get(rid, 0) >= amt:
                    # This process could eventually get the resource
                    for r, a in p.held_resources.items():
                        work[r] += a
                    finish[p.PID] = True
                    changed = True

    return [p.PID for p in all_procs if not finish[p.PID]]


# ---------------------------------------------------------------------------
# Simulator
# ---------------------------------------------------------------------------
class Simulator:
    QUANTUM = 5   # time-slice length

    def __init__(self, resources, processes):
        self.available    = resources
        self.all_processes = processes
        self.ready_q  = []   # processes ready to run
        self.io_q     = []   # processes doing IO
        self.wait_q   = []   # processes waiting for a resource
        self.running  = None
        self.time     = 0
        self.gantt    = []
        self.deadlock_log = []

    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------
    def run(self):
        print("Simulation started...\n")
        MAX_TIME = 10000

        while self.time < MAX_TIME:
            # Exit if everything is done
            if all(p.state == "TERMINATED" for p in self.all_processes):
                break

            # 1. Admit newly arrived processes
            for p in self.all_processes:
                if p.arrival_time == self.time and p.state == "NEW":
                    p.state = "READY"
                    self.ready_q.append(p)

            # 2. Aging: processes waiting in ready queue too long get priority boost
            for p in self.ready_q:
                p.ready_timer += 1
                if p.ready_timer >= 10 and p.priority > 0:
                    p.priority   -= 1
                    p.ready_timer = 0
                    p.aging_count += 1

            # 3. Advance IO timers; move finished IO back to ready
            for p in self.io_q[:]:
                p.io_timer -= 1
                if p.io_timer <= 0:
                    p.burst_index += 1          # move past the IO burst
                    p.state        = "READY"
                    p.priority     = p.original_priority  # reset aged priority on IO return
                    p.ready_timer  = 0
                    self.io_q.remove(p)
                    self.ready_q.append(p)

            # 4. Check wait queue: unblock if resource is now available
            self._try_unblock_waiting()

            # 5. Sort ready queue by (priority, arrival_time)  [lower number = higher priority]
            self.ready_q.sort(key=lambda x: (x.priority, x.arrival_time))

            # 6. Preemption check
            if self.running:
                top = self.ready_q[0] if self.ready_q else None
                preempt = False
                if top and top.priority < self.running.priority:
                    preempt = True          # strictly higher priority available
                if self.running.quantum_used >= self.QUANTUM:
                    preempt = True          # quantum expired
                if preempt:
                    self.running.state     = "READY"
                    self.running.ready_timer = 0
                    self.ready_q.append(self.running)
                    self.ready_q.sort(key=lambda x: (x.priority, x.arrival_time))
                    self.running = None

            # 7. Pick next process to run
            if not self.running and self.ready_q:
                self.running = self.ready_q.pop(0)
                self.running.state       = "RUNNING"
                self.running.quantum_used = 0
                if self.running.start_time == -1:
                    self.running.start_time = self.time

            # 8. Record Gantt
            if not self.running:
                self.gantt.append("IDLE")
            else:
                self.gantt.append(f"P{self.running.PID}")

            # 9. Execute one tick for the running process
            if self.running:
                self.running.quantum_used  += 1
                self._execute_tick(self.running)

            # 10. Deadlock detection
            deadlocked_pids = find_deadlock(self.available, self.all_processes)
            if deadlocked_pids:
                # Choose victim: highest priority number (= lowest scheduling priority)
                # among deadlocked processes; break ties by PID
                victim_pid = max(deadlocked_pids,
                                 key=lambda pid: (
                                     next(p.priority for p in self.all_processes if p.PID == pid),
                                     pid))
                victim = next(p for p in self.all_processes if p.PID == victim_pid)
                print(f">>> Time {self.time}: DEADLOCK detected among PIDs {deadlocked_pids}. "
                      f"Killing P{victim.PID}")
                victim.is_deadlocked = True
                self._terminate(victim)
                self.deadlock_log.append((self.time, victim.PID, deadlocked_pids[:]))
                # Immediately try to unblock processes freed by the kill
                self._try_unblock_waiting()

            # 11. Accumulate waiting-time stats
            for p in self.ready_q:
                p.total_waiting_time += 1
            for p in self.wait_q:
                p.resource_waiting_time += 1

            self.time += 1

        print("Simulation finished.\n")
        self._print_results()

    # ------------------------------------------------------------------
    # Execute one time-tick for the running process.
    # Processes R/F instructions instantly; advances CPU sub-burst timer by 1.
    # ------------------------------------------------------------------
    def _execute_tick(self, p):
        """
        Advance process p by exactly one time unit.
        - Process all pending R/F instructions (no time cost).
        - Then tick the current CPU sub-burst by 1.
        - Handle burst/process completion.
        """
        while True:
            if p.burst_index >= len(p.bursts):
                # All bursts done
                self._terminate(p)
                return

            burst = p.bursts[p.burst_index]

            if burst['type'] == 'IO':
                # Shouldn't be here; IO is handled by io_q
                # Advance past it (shouldn't happen in normal flow)
                p.burst_index += 1
                continue

            # --- CPU burst ---
            instrs = burst['instructions']

            # Process all R/F instructions before the next CPU sub-burst
            while p.instr_index < len(instrs):
                instr = instrs[p.instr_index]

                if instr[0] == 'R':
                    rid, amt = instr[1], instr[2]
                    if self.available.get(rid, 0) >= amt:
                        self.available[rid]       -= amt
                        p.held_resources[rid]     += amt
                        p.instr_index             += 1
                    else:
                        # Block: move to wait queue
                        p.state       = "WAITING"
                        p.waiting_for = (rid, amt)
                        self.wait_q.append(p)
                        self.running  = None
                        return

                elif instr[0] == 'F':
                    rid, amt = instr[1], instr[2]
                    release = min(amt, p.held_resources.get(rid, 0))
                    self.available[rid]   += release
                    p.held_resources[rid] -= release
                    if p.held_resources[rid] <= 0:
                        del p.held_resources[rid]
                    p.instr_index += 1
                    # Immediately try to wake blocked processes
                    self._try_unblock_waiting()

                elif instr[0] == 'CPU':
                    # This is a CPU sub-burst: consume 1 tick
                    if p.cpu_timer <= 0:
                        p.cpu_timer = instr[1]   # set countdown first time
                    p.cpu_timer      -= 1
                    p.cpu_time_used  += 1

                    if p.cpu_timer <= 0:
                        # Sub-burst finished
                        p.instr_index += 1
                        p.cpu_timer    = 0
                        # Fall through to check next instruction (may be R/F or end)
                        continue     # process next instr in same tick (no CPU cost)
                    else:
                        return       # still counting down, done for this tick
                else:
                    p.instr_index += 1   # unknown, skip

            # All instructions in this CPU burst done → move to next burst
            p.burst_index += 1
            p.instr_index  = 0
            p.cpu_timer    = 0

            if p.burst_index >= len(p.bursts):
                self._terminate(p)
                return

            next_burst = p.bursts[p.burst_index]
            if next_burst['type'] == 'IO':
                # Start IO
                p.state    = "IO"
                p.io_timer = next_burst['duration']
                self.io_q.append(p)
                self.running = None
                return
            # else next burst is CPU, loop back to process it

    # ------------------------------------------------------------------
    # Try to unblock waiting processes whose resource request can now be met
    # ------------------------------------------------------------------
    def _try_unblock_waiting(self):
        changed = True
        while changed:
            changed = False
            for p in self.wait_q[:]:
                rid, amt = p.waiting_for
                if self.available.get(rid, 0) >= amt:
                    self.available[rid]   -= amt
                    p.held_resources[rid] += amt
                    p.waiting_for          = None
                    p.instr_index         += 1       # move past the R instruction
                    p.state                = "READY"
                    p.ready_timer          = 0
                    self.wait_q.remove(p)
                    self.ready_q.append(p)
                    changed = True

    # ------------------------------------------------------------------
    # Terminate a process: release all its resources, remove from queues
    # ------------------------------------------------------------------
    def _terminate(self, p):
        p.state       = "TERMINATED"
        p.finish_time = self.time + 1

        # Release held resources
        for rid, amt in p.held_resources.items():
            self.available[rid] = self.available.get(rid, 0) + amt
        p.held_resources.clear()

        # Remove from all queues
        if p in self.ready_q:
            self.ready_q.remove(p)
        if p in self.wait_q:
            self.wait_q.remove(p)
        if p in self.io_q:
            self.io_q.remove(p)
        if self.running is p:
            self.running = None

    # ------------------------------------------------------------------
    # Output
    # ------------------------------------------------------------------
    def _print_results(self):
        # --- Gantt chart (compressed) ---
        print("=" * 20 + " GANTT CHART " + "=" * 20)
        if self.gantt:
            segments, cur, start = [], self.gantt[0], 0
            for i, label in enumerate(self.gantt):
                if label != cur:
                    segments.append(f"[{start}-{i}: {cur}]")
                    cur, start = label, i
            segments.append(f"[{start}-{len(self.gantt)}: {cur}]")
            print(" -> ".join(segments))
        else:
            print("(empty)")

        # --- Deadlock log ---
        if self.deadlock_log:
            print("\n" + "=" * 20 + " DEADLOCK LOG " + "=" * 20)
            for t, killed, involved in self.deadlock_log:
                print(f"  Time {t}: Deadlock among PIDs {involved} → killed P{killed}")

        # --- Per-process stats ---
        print("\n" + "=" * 20 + " FINAL STATS " + "=" * 20)
        print(f"{'PID':<5} | {'State':<12} | {'Wait':<6} | {'ResWait':<8} | {'Turnaround':<11} | {'Aging':<5}")
        print("-" * 65)

        total_wait, total_turn, count = 0, 0, 0
        for p in sorted(self.all_processes, key=lambda x: x.PID):
            if p.is_deadlocked:
                print(f"{p.PID:<5} | {'DEADLOCKED':<12} | {'—':<6} | {'—':<8} | {'—':<11} | {p.aging_count:<5}")
            elif p.finish_time > 0:
                turnaround = p.finish_time - p.arrival_time
                print(f"{p.PID:<5} | {'TERMINATED':<12} | {p.total_waiting_time:<6} | "
                      f"{p.resource_waiting_time:<8} | {turnaround:<11} | {p.aging_count:<5}")
                total_wait += p.total_waiting_time
                total_turn += turnaround
                count      += 1
            else:
                print(f"{p.PID:<5} | {'INCOMPLETE':<12} | {p.total_waiting_time:<6} | "
                      f"{p.resource_waiting_time:<8} | {'—':<11} | {p.aging_count:<5}")

        print("-" * 65)
        if count > 0:
            print(f"\nAverage Waiting Time   : {total_wait / count:.2f}")
            print(f"Average Turnaround Time: {total_turn / count:.2f}")
        else:
            print("No processes completed normally.")



# Entry point

if __name__ == "__main__":
    res, procs = parse_file("input.txt")
    if res is not None and procs is not None:
        Simulator(res, procs).run()
    else:
        print("Failed to parse input file.")
