<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:ffb6c1,100:ff1493&height=200&section=header&text=OS%20Scheduler%20%26%20Deadlock%20Simulator&fontSize=35&fontColor=ffffff&animation=fadeIn&fontAlignY=38&desc=Priority%20Scheduling%20%7C%20Deadlock%20Recovery%20%7C%20Aging%20%7C%20Birzeit%20University&descAlignY=60&descSize=18&descColor=ffffff"/>

[![Typing SVG](https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=22&duration=3000&pause=1000&color=FF69B4&center=true&vCenter=true&width=800&lines=Preemptive+Priority+Scheduling;Round+Robin+Fair+Sharing;Banker's+Algorithm+Logic;Starvation+Prevention+via+Aging;Pink-Themed+Interactive+Dashboard)](https://git.io/typing-svg)

![Python](https://img.shields.io/badge/Python-3.x-FF69B4?style=for-the-badge&logo=python&logoColor=white)
![Scheduling](https://img.shields.io/badge/Scheduling-Preemptive-ff1493?style=for-the-badge)
![Deadlock](https://img.shields.io/badge/Deadlock-Detection%20%26%20Recovery-purple?style=for-the-badge)
![University](https://img.shields.io/badge/Birzeit%20University-ENCS3390-1a1a2e?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Verified-success?style=for-the-badge)

</div>

---

## 📋 Project Abstract

A high-fidelity **Process Scheduler & Deadlock Management Simulator** developed for the **ENCS3390 Operating Systems** course at Birzeit University. This tool models a single-core environment where processes compete for CPU time and multiple resource instances. 

The simulator features a unique **Interactive "Pink" CLI** that allows users to step through time units, observing how processes move between states, how the scheduler handles preemption, and how the deadlock engine intervenes to save the system from circular waits.

---

## 🎀 Interactive Dashboard Features

The simulator provides a live terminal experience with pink aesthetics:

- **Step-by-Step Mode:** Press `Enter` to advance time by 1 tick to inspect every state transition.
- **Auto-Run Mode:** Type `a` to switch to high-speed execution.
- **Live State Tracking:** Real-time visibility into the **Ready Queue**, **IO Queue**, and **Waiting (Resource) Queue**.
- **Pink Aesthetics:** ANSI-color-coded outputs for professional and readable logs.

---

## ⚙️ Process State Machine

The core logic handles the complex lifecycle of processes using a 6-state model.

```mermaid
graph LR
    A[NEW] -- Arrival --> B[READY]
    B -- Dispatch --> C[RUNNING]
    C -- Preemption/Quantum --> B
    C -- Resource Request --> D[WAITING]
    C -- IO Burst --> E[IO]
    D -- Resource Free --> B
    E -- IO Finish --> B
    C -- Finish --> F[TERMINATED]
    
    style C fill:#ff1493,stroke:#fff,stroke-width:2px,color:#fff
    style B fill:#ffb6c1,stroke:#333,stroke-width:1px
    style D fill:#dda0dd,stroke:#333,stroke-width:1px
🔮 Core System Logic
🧠 Scheduling Architecture
Preemptive Priority: High-priority tasks (Lower priority numbers) immediately seize the CPU.
Round Robin: Processes with equal priority level are managed via a 5-unit Time Quantum.
Aging: To prevent starvation, processes waiting in the Ready Queue have their priority boosted every 10 time units.
🚨 Deadlock Engine
Detection: Implements Resource-Allocation Graph Reduction (Banker's logic) every clock tick.
Recovery: When a deadlock is detected, the system identifies the "Victim" (the process with the lowest priority) and terminates it, instantly releasing its resources to unblock the rest of the system.
📐 Burst Instructions & Parsing
The simulator parses complex process strings that include mid-burst resource manipulation:
Instruction	Code	Description
Request	R[id, amt]	Process attempts to acquire resources; blocks if unavailable.
Free	F[id, amt]	Process releases resources back to the available pool.
Compute	Integer	Execution time consumed on the CPU.
IO	IO {time}	Non-blocking concurrent IO operations.
🧪 Simulation Output Examples
🔴 Case 1: Deadlock Recovery
When circular wait occurs (P0 needs R2, P1 needs R1):
System Detection: Identifies stalled PIDs.
Action: Triggers red alert and preemptively terminates the victim.
PID	State	CPU Wait	Res Wait	Turnaround	Aging
0	TERMINATED	31	30	100	2
1	<font color="#ff1493">KILLED</font>	—	—	—	2
2	TERMINATED	47	0	110	3
🟢 Case 2: Aging in Action
When a low-priority process (Priority 20) is ignored by high-priority ones:
Aging Log: ✨ P0 Aged! Priority is now 19
Result: P0 eventually runs even with high-priority tasks present.
📁 Repository Structure
code
Text
OS-Scheduler-Pink/
├── prj.py           # Main Pink Interactive Engine
├── scenario1.txt    # Deadlock & Recovery Case
├── scenario2.txt    # Aging & Starvation Case
├── scenario3.txt    # 3-Way Deadlock Chain Case
└── README.md        # Documentation
🎓 Academic Information
Course	ENCS3390 — Operating System Concepts
University	Birzeit University 🇵🇸
Department	Electrical & Computer Engineering
Student	Shatha Abualrob
Semester	Fall 2025/2026
<div align="center">
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:ff1493,100:ffb6c1&height=100&section=footer"/>
</div>
```
