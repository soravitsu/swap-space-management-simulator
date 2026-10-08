# Swap Space Management Simulator

A mini project for Operating Systems that simulates memory management,
swap space management, memory allocation strategies, and external fragmentation.

## Project Overview

The Swap Space Management Simulator is a graphical simulation of how an
Operating System manages processes between RAM and Swap Space.

The simulator allows users to create processes, allocate memory,
move processes between RAM and Swap Space, terminate processes,
and observe memory fragmentation.

## Objectives

- Understand how Swap Space works in an Operating System.
- Simulate process allocation in RAM and Swap Space.
- Demonstrate different memory allocation strategies.
- Observe External Fragmentation.
- Visualize memory usage through a graphical interface.
- Track Swap In and Swap Out operations.

## Features

### 1. Process Management

Users can:

- Create a new process with a specified memory size.
- Terminate an existing process.
- View process information in the Process Table.

Each process contains:

- Process ID
- Memory Size
- Location
- Status

### 2. RAM and Swap Space

The simulator provides separate memory areas for:

- RAM
- Swap Space

Supported memory sizes:

- 16 MB
- 32 MB
- 64 MB

Users can change the RAM and Swap Space configuration.

### 3. Memory Allocation Strategies

The simulator supports three allocation strategies.

#### First Fit

First Fit searches from the beginning of memory and selects
the first available block that is large enough for the process.

#### Best Fit

Best Fit searches all available memory blocks and selects
the smallest block that can contain the process.

#### Worst Fit

Worst Fit selects the largest available memory block
that can contain the process.

Users can change the allocation strategy during the simulation.

### 4. Swap In

Swap In moves a process from Swap Space back into RAM.

```text
Swap Space
    |
    | Swap In
    v
   RAM

The operation requires enough available RAM space for the process.
5. Swap Out
Swap Out moves a process from RAM to Swap Space.
   RAM
    |
    | Swap Out
    v
Swap Space

The operation requires enough available Swap Space.
6. External Fragmentation
The simulator calculates External Fragmentation based on
the available free memory blocks.
The following information is displayed:
- Number of Free Blocks
- Largest Free Block
- External Fragmentation Percentage
External fragmentation occurs when free memory is divided
into multiple separated blocks.
Example:
RAM

+------+-------+------+----------+
| P1   | Free  | P2   |   Free   |
| 4 MB |  3 MB | 5 MB |  52 MB   |
+------+-------+------+----------+

There are multiple free blocks even though the total amount
of free memory may be large.
7. Event Log
The simulator records important events such as:
P1 created (4 MB) → RAM
P2 created (3 MB) → RAM
P2 → SWAP OUT
P2 → SWAP IN
P2 → TERMINATED
Allocation Strategy → Best Fit

This allows users to observe the sequence of memory management operations.
Simulation Statistics
The interface displays:
- Total Processes
- Available RAM
- Available Swap
- Free Blocks
- Largest Free Block
- External Fragmentation
- Swap In Count
- Swap Out Count
Project Structure
swap-space-management-simulator/
│
├── models/
│   └── process.py
│
├── simulator/
│   ├── allocation.py
│   └── swap_manager.py
│
├── ui/
│   └── main_window.py
│
├── main.py
├── .gitignore
└── README.md

File Description
File	Description
models/process.py	Defines the Process model
simulator/allocation.py	Implements First Fit, Best Fit, and Worst Fit
simulator/swap_manager.py	Manages RAM, Swap Space, and processes
ui/main_window.py	Provides the Tkinter graphical interface
main.py	Starts the simulator
.gitignore	Prevents unnecessary files from being committed
README.md	Project documentation


Technologies
- Python
- Tkinter
- Object-Oriented Programming
- Git
- GitHub
Requirements
- Python 3.x
- Windows / Linux / macOS
- Tkinter
How to Run
Clone the repository:
git clone https://github.com/soravitsu/swap-space-management-simulator.git

Open the project directory:
cd swap-space-management-simulator

Run the application:
python main.py

On Windows, the project can also be run using:
.venv\Scripts\python.exe main.py

How to Use
Step 1: Configure Memory
Select:
- RAM Size
- Swap Size
- Allocation Strategy
Then click:
Apply Configuration

Step 2: Create Processes
Click:
Create Process

Enter the process size in MB.
The simulator will attempt to allocate the process in RAM.
If RAM does not have a suitable free block, the process may be
allocated to Swap Space if enough space is available.
Step 3: Swap Processes
Select a process from the Process Table.
Use:
Swap Out

to move a process from RAM to Swap Space.
Use:
Swap In

to move a process from Swap Space back to RAM.
Step 4: Terminate Processes
Select a process and click:
Terminate Process

The process will be removed and its allocated memory will become free.
Step 5: Observe Fragmentation
After terminating processes, observe:
- Free Blocks
- Largest Free Block
- External Fragmentation
These values demonstrate how memory can become fragmented.
Example
Example memory configuration:
RAM: 64 MB
Swap: 16 MB
Allocation Strategy: Worst Fit

Example RAM:
+------+-------+-----------------------------+
| P6   | Free  |            Free             |
| 4 MB | 1 MB  |           59 MB            |
+------+-------+-----------------------------+

Example Swap:
+------+------+--------+-------+------+
| P4   | P5   | P1     | P3    | Free |
| 2 MB | 2 MB | 4 MB   | 5 MB  | 3 MB |
+------+------+--------+-------+------+

The simulator updates the memory visualization and statistics
after every operation.
Educational Purpose
This project demonstrates fundamental Operating System concepts
related to memory management, including:
- Memory Allocation
- Swap Space
- Process Management
- First Fit
- Best Fit
- Worst Fit
- External Fragmentation
- Swapping
The project is intended for educational and simulation purposes
and does not modify the actual operating system memory or swap space.