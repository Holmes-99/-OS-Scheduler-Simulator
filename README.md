<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:ffb6c1,100:ff1493&height=180&section=header&text=OS%20Scheduler%20%26%20Deadlock%20Simulator&fontSize=36&fontColor=ffffff&animation=fadeIn&fontAlignY=38&desc=Priority%20Scheduling%20%7C%20Deadlock%20Recovery%20%7C%20Aging%20%7C%20Birzeit%20University&descAlignY=60&descSize=15&descColor=ffe4ec"/>

[![Typing SVG](https://readme-typing-svg.herokuapp.com?font=Fira+Code\&size=20\&duration=2500\&pause=800\&color=FF69B4\&center=true\&vCenter=true\&width=750\&lines=Preemptive+Priority+Scheduling;Round+Robin+Fair+Sharing;Deadlock+Detection+%26+Recovery;Starvation+Prevention+via+Aging;Interactive+Pink+CLI+Simulator)](https://git.io/typing-svg)

![Python](https://img.shields.io/badge/Python-3.x-FF69B4?style=for-the-badge\&logo=python\&logoColor=white)
![Scheduling](https://img.shields.io/badge/Scheduling-Priority%20%2B%20RR-ff1493?style=for-the-badge)
![Deadlock](https://img.shields.io/badge/Deadlock-Recovery%20Engine-dc143c?style=for-the-badge)
![CLI](https://img.shields.io/badge/Interface-Interactive%20CLI-ff69b4?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Verified-success?style=for-the-badge)

</div>

---

## 📋 Abstract

A **high-fidelity Operating System simulator** that models:

* CPU scheduling (Preemptive Priority + Round Robin)
* Resource allocation & contention
* Deadlock detection and recovery
* Starvation prevention via aging

Built as an **interactive CLI system**, allowing users to step through execution *tick by tick* and observe real OS behavior in real time.

---

## 🎀 Interactive CLI Experience

```
[Time = 42]

💖 Running:   P2
🎀 Ready:     P0, P3
🌸 Waiting:   P1 (R2)
🌷 IO Queue:  P4 (3 ticks)

Command → [Enter = step | a = auto-run]
```

### Features

* ⏱️ Step-by-step execution (`Enter`)
* ⚡ Auto-run mode (`a`)
* 📊 Live queue visualization
* 🎨 Pink-themed ANSI interface

---

## ⚙️ Process Lifecycle

```mermaid
graph LR
    A[NEW] --> B[READY]
    B --> C[RUNNING]
    C -->|Preempt| B
    C -->|Request Resource| D[WAITING]
    C -->|IO Burst| E[IO]
    D --> B
    E --> B
    C --> F[TERMINATED]
```

---

## 🔮 Scheduling Engine

### 🧠 Hybrid Scheduling Strategy

```
Priority Scheduling (Preemptive)
        +
Round Robin (Same Priority)
        +
Aging Mechanism
```

### Behavior

* 🎯 **Higher priority always wins**
* 🔁 **Same priority → Round Robin (Quantum = 5)**
* ✨ **Aging every 10 ticks → prevents starvation**

---

## 🚨 Deadlock Engine

### Detection

* Resource Allocation Graph (Banker-style reduction)
* Runs **every clock tick**

### Recovery Strategy

```
1. Detect circular wait
2. Select victim (lowest priority)
3. Terminate process
4. Release all resources
5. Resume system safely
```

---

## 📐 Instruction Model

| Type    | Example  | Description                   |
| ------- | -------- | ----------------------------- |
| CPU     | `5`      | Execute for 5 time units      |
| Request | `R[1,2]` | Request 2 units of Resource 1 |
| Free    | `F[1,2]` | Release resources             |
| IO      | `IO{3}`  | Perform IO for 3 ticks        |

---

## 🧪 Simulation Scenarios

### 🔴 Deadlock Recovery

```
P0 holds R1 → needs R2
P1 holds R2 → needs R1

💥 Deadlock detected!
💀 Killing victim: P1
🔓 Resources released
```

---

### 🟢 Starvation Prevention (Aging)

```
Initial Priority: P0 = 20 (very low)

✨ Aging Triggered
→ P0 priority: 20 → 19 → 18 ...

✅ Eventually scheduled
```

---

## 🖥️ Example Output

```
[T=15]

Running → P1
Ready   → P0, P2
Waiting → P3 (R1 unavailable)

✨ Aging: P0 priority improved → 4

----------------------------------
[T=16]

🚨 Deadlock Detected!
💀 Terminating P3
🔓 Resources Released
```

---

## 📁 Project Structure

```
OS-Scheduler-Pink/
├── prj.py              # Core simulation engine
├── scenario1.txt       # Deadlock case
├── scenario2.txt       # Aging case
├── scenario3.txt       # Complex deadlock chain
└── README.md
```

---

## ▶️ How to Run

```bash
python prj.py scenario1.txt
```

### Controls

| Key    | Action         |
| ------ | -------------- |
| Enter  | Step forward   |
| a      | Auto-run       |
| Ctrl+C | Stop execution |

---

## 🌟 Why This Project Stands Out

* Simulates **real OS concepts**, not simplified models
* Combines **3 scheduling techniques in one system**
* Implements **actual deadlock recovery logic**
* Fully **interactive (rare for OS projects)**
* Designed with **clear visualization in mind**

---

## 🎓 Academic Info

|            |                              |
| ---------- | ---------------------------- |
| Course     | ENCS3390 — Operating Systems |
| University | Birzeit University 🇵🇸      |
| Student    | Shatha Abualrob              |
| Semester   | Fall 2025/2026               |

---

<div align="center">
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:ff1493,100:ffb6c1&height=100&section=footer"/>
</div>
