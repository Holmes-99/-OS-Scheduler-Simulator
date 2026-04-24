# OS Process Scheduler Simulator
> ENCS3390 — Operating Systems Concepts | Birzeit University | Fall 2025/2026

A single-CPU process scheduling simulator with **preemptive priority scheduling**, **round-robin time slicing**, **aging**, **deadlock detection**, and **deadlock recovery**.

---

## Features

- **Preemptive Priority Scheduling** — higher-priority processes immediately preempt lower-priority ones
- **Round Robin** — quantum of 5 time units per process at equal priority
- **Aging** — processes waiting in the ready queue for 10+ units get their priority decremented by 1 (prevents starvation)
- **Resource Management** — processes can request (`R[id, amt]`) and release (`F[id, amt]`) resource instances mid-burst
- **Deadlock Detection** — Banker's-style resource-allocation graph reduction runs every tick
- **Deadlock Recovery** — the lowest-priority deadlocked process is killed and its resources are freed
- **Gantt Chart** — compressed timeline of process execution printed at the end
- **Statistics** — per-process waiting time, resource waiting time, turnaround time, and aging count

---

## Input Format

```
[ResourceID, Instances], [ResourceID, Instances], ...
PID  ArrivalTime  Priority  CPU {burst} IO {burst} CPU {burst} ...
```

- Priority range: **0 (highest) → 20 (lowest)**
- Each process must **start and end with a CPU burst**
- Inside a CPU burst: plain integers = CPU duration, `R[id,amt]` = acquire, `F[id,amt]` = release
- IO bursts are a single integer duration

### Example input file

```
[1,5], [2,3], [5,1]
0  0  1  CPU {R[1,2], 50, F[1,1], 20, F[1,1]}
1  5  1  CPU {20} IO {30} CPU {20, R[2,3], 30, F[2,3], 10}
```

---

## How to Run

```bash
python3 simulator.py
```

The simulator reads from `input.txt` in the same directory.

---

## Output

```
Simulation started...

>>> Time 74: DEADLOCK detected among PIDs [0, 1]. Killing P1

==================== GANTT CHART ====================
[0-10: P2] -> [10-15: P0] -> [15-19: P2] -> ...

==================== DEADLOCK LOG ====================
  Time 74: Deadlock among PIDs [0, 1] → killed P1

==================== FINAL STATS ====================
PID   | State        | Wait   | ResWait  | Turnaround  | Aging
-----------------------------------------------------------------
0     | TERMINATED   | 31     | 30       | 100         | 2
1     | DEADLOCKED   | —      | —        | —           | 2
2     | TERMINATED   | 47     | 0        | 110         | 3
...
Average Waiting Time   : 79.50
Average Turnaround Time: 133.25
```

---

## Scheduling Algorithm

```
Every tick:
  1. Admit newly arrived processes → READY queue
  2. Age processes waiting 10+ ticks in READY → priority--
  3. Advance IO timers; finished IO → READY queue
  4. Unblock WAITING processes whose resource is now available
  5. Sort READY queue by (priority ASC, arrival_time ASC)
  6. Preempt running process if:
       - a higher-priority process is ready, OR
       - quantum (5 ticks) is exhausted
  7. Dispatch next from READY queue
  8. Execute one tick (process R/F/CPU instructions)
  9. Run deadlock detection; kill victim if deadlock found
 10. Accumulate waiting-time stats
```

---

## Deadlock Detection & Recovery

Detection uses a **resource-allocation graph reduction** (Banker's algorithm style):

1. Build `work = available resources`
2. Add resources held by non-blocked processes to `work`
3. Repeatedly: if a WAITING process's request can be satisfied from `work`, mark it done and add its held resources back to `work`
4. Any process still unmarked is in a **deadlock cycle**

Recovery: the deadlocked process with the **lowest scheduling priority** (highest priority number) is terminated and its resources are released immediately.

---

## Test Scenarios

### Scenario 1 — With deadlock

```
[1,2], [2,2], [3,5]
0  0  2  CPU {R[1,2], 20} CPU {R[2,2], 20, F[1,2], F[2,2]}
1  2  2  CPU {R[2,2], 20} CPU {R[1,2], 20, F[2,2], F[1,2]}
2  0  1  CPU {15} IO {10} CPU {15} IO {10} CPU {15}
3  5  3  CPU {R[3,3], 30, F[3,3]} IO {15} CPU {10}
4  10 1  CPU {10, R[1,1], 20, F[1,1]}
```
<img width="1259" height="550" alt="image" src="https://github.com/user-attachments/assets/b3c061f2-bee1-4793-ab5b-8a2b251d6453" />

P0 and P1 form a circular wait → deadlock detected at **t=74**, P1 killed.

### Scenario 2 — No deadlock (aging demo)

```
[1,5], [2,3], [5,1]
0  0  1  CPU {R[1,2], 50, F[1,1], 20, F[1,1]}
1  5  1  CPU {20} IO {30} CPU {20, R[2,3], 30, F[2,3], 10}
```

All processes terminate normally. Low-priority processes age up over time.

---

## Project Structure

```
OS_Task2/
├── simulator.py     # main simulator
├── input.txt        # active test case (swap for different scenarios)
├── scenario1.txt    # deadlock test case
├── scenario2.txt    # no-deadlock / aging test case
└── README.md
```

---

## Requirements

- Python 3.6+
- No external libraries (standard library only)

---


*Birzeit University — Department of Electrical & Computer Engineering*
