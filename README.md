<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:ff007f,100:ff85a2&height=200&section=header&text=OS%20Scheduler%20Simulator&fontSize=42&fontColor=ffffff&animation=fadeIn&fontAlignY=38&desc=Priority%20Scheduling%20%7C%20Deadlock%20Recovery%20%7C%20Aging%20%7C%20Birzeit%20University&descAlignY=60&descSize=18&descColor=ffffff"/>

[![Typing SVG](https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=20&duration=3000&pause=1000&color=FF1493&center=true&vCenter=true&width=800&lines=Preemptive+Priority+Scheduling;Round+Robin+Fair+Sharing;Banker's+Algorithm+Deadlock+Engine;Starvation+Prevention+via+Aging;Pink-Themed+Interactive+Simulation)](https://git.io/typing-svg)

![Python](https://img.shields.io/badge/Python-3.x-FF69B4?style=for-the-badge&logo=python&logoColor=white)
![Scheduling](https://img.shields.io/badge/Mode-Preemptive-e91e63?style=for-the-badge)
![Deadlock](https://img.shields.io/badge/Deadlock-Detection%20%26%20Recovery-9c27b0?style=for-the-badge)
![University](https://img.shields.io/badge/Birzeit%20University-ENCS3390-1a1a2e?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Verified-success?style=for-the-badge)

</div>

---

## 📋 Abstract

This repository contains a high-fidelity **Process Scheduler & Deadlock Management Simulator** developed in Python. It models a single-core CPU environment where processes compete for computational time and multi-instance resource types. The simulator features a custom **Pink-Themed Interactive CLI** that allows users to step through time ticks and observe real-time transitions in process states, queue management, and resource allocation.

> **Final CPI/Performance Metric:** Optimized for low average waiting time while ensuring zero deadlock-induced system crashes through automated victim selection and resource preemption.

---

## ⚙️ Interactive Dashboard Features

The simulator isn't just a static log; it's a **live experience**. 

- **Step-by-Step Mode:** Press `Enter` to advance time by 1 tick and see exactly how the CPU choices are made.
- **Auto-Run Mode:** Type `a` to let the simulation finish at high speed.
- **Pink Aesthetics:** ANSI-color-coded terminal output for high readability and a unique visual style.

```text
Time: 76
Resources Available: {1: 0, 2: 0}
CPU Running: P0
Ready Queue: [2, 4]
Waiting (Res): [1]
>>> 🚨 DEADLOCK! Killing P1 to save the system! 🚨
