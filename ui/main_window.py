import tkinter as tk
from tkinter import ttk, messagebox

from simulator.swap_manager import SwapManager


class MainWindow:
    def __init__(self, root):
        self.root = root

        self.root.title(
            "Swap Space Management Simulator"
        )

        self.root.geometry("1100x720")
        self.root.minsize(900, 600)

        # Simulation logic
        self.manager = SwapManager(
            ram_size=16,
            swap_size=16
        )

        # Create UI
        self.create_header()
        self.create_memory_area()
        self.create_controls()
        self.create_process_table()
        self.create_statistics()
        self.create_log()

        self.update_display()

    # =====================================
    # Header
    # =====================================

    def create_header(self):
        frame = ttk.Frame(
            self.root,
            padding=15
        )

        frame.pack(
            fill="x"
        )

        ttk.Label(
            frame,
            text="Swap Space Management Simulator",
            font=("Arial", 22, "bold")
        ).pack()

        ttk.Label(
            frame,
            text="Operating System Memory Management Simulation"
        ).pack(
            pady=(5, 0)
        )

    # =====================================
    # RAM / Swap
    # =====================================

    def create_memory_area(self):
        frame = ttk.Frame(
            self.root,
            padding=10
        )

        frame.pack(
            fill="x",
            padx=20
        )

        # RAM
        ram_frame = ttk.LabelFrame(
            frame,
            text="RAM Memory (16 MB)",
            padding=15
        )

        ram_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        self.ram_canvas = tk.Canvas(
            ram_frame,
            height=180,
            bg="white"
        )

        self.ram_canvas.pack(
            fill="both",
            expand=True
        )

        self.ram_usage = ttk.Label(
            ram_frame
        )

        self.ram_usage.pack(
            pady=(10, 0)
        )

        # Swap
        swap_frame = ttk.LabelFrame(
            frame,
            text="Swap Space (16 MB)",
            padding=15
        )

        swap_frame.pack(
            side="right",
            fill="both",
            expand=True,
            padx=(10, 0)
        )

        self.swap_canvas = tk.Canvas(
            swap_frame,
            height=180,
            bg="white"
        )

        self.swap_canvas.pack(
            fill="both",
            expand=True
        )

        self.swap_usage = ttk.Label(
            swap_frame
        )

        self.swap_usage.pack(
            pady=(10, 0)
        )

    # =====================================
    # Controls
    # =====================================

    def create_controls(self):
        frame = ttk.LabelFrame(
            self.root,
            text="Simulation Controls",
            padding=15
        )

        frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        # Allocation Strategy
        ttk.Label(
            frame,
            text="Allocation Strategy:"
        ).pack(
            side="left",
            padx=(5, 2)
        )

        self.strategy_var = tk.StringVar(
            value=self.manager.strategy
        )

        self.strategy_combo = ttk.Combobox(
            frame,
            textvariable=self.strategy_var,
            values=[
                "First Fit",
                "Best Fit",
                "Worst Fit"
            ],
            state="readonly",
            width=12
        )

        self.strategy_combo.pack(
            side="left",
            padx=5
        )

        self.strategy_combo.bind(
            "<<ComboboxSelected>>",
            self.change_strategy
        )

        # Create Process
        ttk.Button(
            frame,
            text="Create Process",
            command=self.create_process
        ).pack(
            side="left",
            padx=5
        )

        # Swap In
        ttk.Button(
            frame,
            text="Swap In",
            command=self.swap_in
        ).pack(
            side="left",
            padx=5
        )

        # Swap Out
        ttk.Button(
            frame,
            text="Swap Out",
            command=self.swap_out
        ).pack(
            side="left",
            padx=5
        )

        # Terminate
        ttk.Button(
            frame,
            text="Terminate Process",
            command=self.terminate_process
        ).pack(
            side="left",
            padx=5
        )

        # Reset
        ttk.Button(
            frame,
            text="Reset",
            command=self.reset
        ).pack(
            side="right",
            padx=5
        )

    # =====================================
    # Process Table
    # =====================================

    def create_process_table(self):
        frame = ttk.LabelFrame(
            self.root,
            text="Process Table",
            padding=10
        )

        frame.pack(
            fill="x",
            padx=20,
            pady=5
        )

        columns = (
            "PID",
            "Size",
            "Location",
            "Status"
        )

        self.process_table = ttk.Treeview(
            frame,
            columns=columns,
            show="headings",
            height=5
        )

        for column in columns:
            self.process_table.heading(
                column,
                text=column
            )

            self.process_table.column(
                column,
                anchor="center"
            )

        self.process_table.pack(
            fill="x"
        )

    # =====================================
    # Statistics
    # =====================================

    def create_statistics(self):
        frame = ttk.LabelFrame(
            self.root,
            text="Simulation Statistics",
            padding=10
        )

        frame.pack(
            fill="x",
            padx=20,
            pady=5
        )

        self.total_processes_label = ttk.Label(
            frame,
            text="Total Processes: 0"
        )

        self.total_processes_label.pack(
            side="left",
            padx=10
        )

        self.ram_available_label = ttk.Label(
            frame,
            text="Available RAM: 16 MB"
        )

        self.ram_available_label.pack(
            side="left",
            padx=10
        )

        self.swap_available_label = ttk.Label(
            frame,
            text="Available Swap: 16 MB"
        )

        self.swap_available_label.pack(
            side="left",
            padx=10
        )

        self.free_blocks_label = ttk.Label(
            frame,
            text="Free Blocks: 1"
        )

        self.free_blocks_label.pack(
            side="left",
            padx=10
        )

        self.largest_block_label = ttk.Label(
            frame,
            text="Largest Free Block: 16 MB"
        )

        self.largest_block_label.pack(
            side="left",
            padx=10
        )

        self.fragmentation_label = ttk.Label(
            frame,
            text="External Fragmentation: 0%"
        )

        self.fragmentation_label.pack(
            side="left",
            padx=10
        )

        self.swap_in_label = ttk.Label(
            frame,
            text="Swap In: 0"
        )

        self.swap_in_label.pack(
            side="left",
            padx=10
        )

        self.swap_out_label = ttk.Label(
            frame,
            text="Swap Out: 0"
        )

        self.swap_out_label.pack(
            side="left",
            padx=10
        )

    # =====================================
    # Event Log
    # =====================================

    def create_log(self):
        frame = ttk.LabelFrame(
            self.root,
            text="Event Log",
            padding=10
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(5, 15)
        )

        self.log = tk.Text(
            frame,
            height=6,
            state="disabled"
        )

        self.log.pack(
            fill="both",
            expand=True
        )

    def add_log(self, message):
        self.log.config(
            state="normal"
        )

        self.log.insert(
            "end",
            message + "\n"
        )

        self.log.see(
            "end"
        )

        self.log.config(
            state="disabled"
        )

    # =====================================
    # Allocation Strategy
    # =====================================

    def change_strategy(self, event=None):
        strategy = self.strategy_var.get()

        try:
            self.manager.set_strategy(
                strategy
            )

            self.add_log(
                f"Allocation Strategy → {strategy}"
            )

        except ValueError as error:
            messagebox.showerror(
                "Allocation Strategy",
                str(error)
            )

    # =====================================
    # Create Process
    # =====================================

    def create_process(self):
        dialog = tk.Toplevel(
            self.root
        )

        dialog.title(
            "Create Process"
        )

        dialog.geometry(
            "300x180"
        )

        dialog.resizable(
            False,
            False
        )

        ttk.Label(
            dialog,
            text="Process Size (MB):"
        ).pack(
            pady=(25, 5)
        )

        entry = ttk.Entry(
            dialog
        )

        entry.pack()
        entry.focus()

        def confirm():
            try:
                size = int(
                    entry.get()
                )

                process = (
                    self.manager
                    .create_process(size)
                )

                self.add_log(
                    f"{process.pid} created "
                    f"({process.size} MB) "
                    f"→ {process.location}"
                )

                self.update_display()

                dialog.destroy()

            except ValueError as error:
                messagebox.showerror(
                    "Invalid Process",
                    str(error)
                )

            except MemoryError as error:
                messagebox.showwarning(
                    "Memory Full",
                    str(error)
                )

                self.add_log(
                    f"Allocation failed: {error}"
                )

        ttk.Button(
            dialog,
            text="Create",
            command=confirm
        ).pack(
            pady=20
        )

    # =====================================
    # Selected Process
    # =====================================

    def get_selected_process(self):
        selection = (
            self.process_table
            .selection()
        )

        if not selection:
            messagebox.showinfo(
                "No Process Selected",
                "Please select a process first."
            )

            return None

        values = (
            self.process_table
            .item(selection[0])["values"]
        )

        pid = values[0]

        return (
            self.manager
            .find_process(pid)
        )

    # =====================================
    # Swap Out
    # =====================================

    def swap_out(self):
        process = (
            self.get_selected_process()
        )

        if process is None:
            return

        try:
            self.manager.swap_out(
                process
            )

            self.add_log(
                f"{process.pid} → SWAP OUT"
            )

            self.update_display()

        except (
            ValueError,
            MemoryError
        ) as error:
            messagebox.showwarning(
                "Swap Out",
                str(error)
            )

            self.add_log(
                f"Swap Out failed: {error}"
            )

    # =====================================
    # Swap In
    # =====================================

    def swap_in(self):
        process = (
            self.get_selected_process()
        )

        if process is None:
            return

        try:
            self.manager.swap_in(
                process
            )

            self.add_log(
                f"{process.pid} → SWAP IN"
            )

            self.update_display()

        except (
            ValueError,
            MemoryError
        ) as error:
            messagebox.showwarning(
                "Swap In",
                str(error)
            )

            self.add_log(
                f"Swap In failed: {error}"
            )

    # =====================================
    # Terminate
    # =====================================

    def terminate_process(self):
        process = (
            self.get_selected_process()
        )

        if process is None:
            return

        self.manager.terminate_process(
            process
        )

        self.add_log(
            f"{process.pid} → TERMINATED"
        )

        self.update_display()

    # =====================================
    # Draw Memory
    # =====================================

    def draw_memory(
        self,
        canvas,
        memory
    ):
        canvas.delete(
            "all"
        )

        width = (
            canvas.winfo_width()
        )

        if width < 100:
            width = 400

        block_width = (
            width / len(memory)
        )

        for index, process in enumerate(
            memory
        ):
            x1 = (
                index * block_width
            )

            x2 = (
                (index + 1)
                * block_width
            )

            if process is None:
                text = "Free"
                fill = "white"

            else:
                text = process.pid
                fill = "lightblue"

            canvas.create_rectangle(
                x1 + 2,
                30,
                x2 - 2,
                140,
                fill=fill,
                outline="gray"
            )

            canvas.create_text(
                (x1 + x2) / 2,
                85,
                text=text
            )

    # =====================================
    # Update UI
    # =====================================

    def update_display(self):
        self.draw_memory(
            self.ram_canvas,
            self.manager.ram
        )

        self.draw_memory(
            self.swap_canvas,
            self.manager.swap
        )

        ram_used, ram_percent = (
            self.manager.get_ram_usage()
        )

        swap_used, swap_percent = (
            self.manager.get_swap_usage()
        )

        # Available space
        ram_available = (
            self.manager.ram_size
            - ram_used
        )

        swap_available = (
            self.manager.swap_size
            - swap_used
        )

        # RAM fragmentation
        fragmentation = (
            self.manager.get_ram_fragmentation()
        )

        free_blocks = (
            fragmentation["free_blocks"]
        )

        largest_block = (
            fragmentation["largest_block"]
        )

        external_fragmentation = (
            fragmentation[
                "external_fragmentation"
            ]
        )

        # Basic statistics
        self.total_processes_label.config(
            text=(
                f"Total Processes: "
                f"{len(self.manager.processes)}"
            )
        )

        self.ram_available_label.config(
            text=(
                f"Available RAM: "
                f"{ram_available} MB"
            )
        )

        self.swap_available_label.config(
            text=(
                f"Available Swap: "
                f"{swap_available} MB"
            )
        )

        # Fragmentation statistics
        self.free_blocks_label.config(
            text=(
                f"Free Blocks: "
                f"{free_blocks}"
            )
        )

        self.largest_block_label.config(
            text=(
                f"Largest Free Block: "
                f"{largest_block} MB"
            )
        )

        self.fragmentation_label.config(
            text=(
                f"External Fragmentation: "
                f"{external_fragmentation:.0f}%"
            )
        )

        # Swap statistics
        self.swap_in_label.config(
            text=(
                f"Swap In: "
                f"{self.manager.swap_in_count}"
            )
        )

        self.swap_out_label.config(
            text=(
                f"Swap Out: "
                f"{self.manager.swap_out_count}"
            )
        )

        # RAM usage
        self.ram_usage.config(
            text=(
                f"RAM Usage: "
                f"{ram_used}/"
                f"{self.manager.ram_size} MB "
                f"({ram_percent:.0f}%)"
            )
        )

        # Swap usage
        self.swap_usage.config(
            text=(
                f"Swap Usage: "
                f"{swap_used}/"
                f"{self.manager.swap_size} MB "
                f"({swap_percent:.0f}%)"
            )
        )

        # Clear process table
        for item in (
            self.process_table
            .get_children()
        ):
            self.process_table.delete(
                item
            )

        # Add processes
        for process in (
            self.manager.processes
        ):
            self.process_table.insert(
                "",
                "end",
                values=(
                    process.pid,
                    f"{process.size} MB",
                    process.location,
                    process.status
                )
            )

    # =====================================
    # Reset
    # =====================================

    def reset(self):
        answer = messagebox.askyesno(
            "Reset Simulator",
            "Reset the entire simulation?"
        )

        if not answer:
            return

        self.manager.reset()

        self.strategy_var.set(
            self.manager.strategy
        )

        self.log.config(
            state="normal"
        )

        self.log.delete(
            "1.0",
            "end"
        )

        self.log.config(
            state="disabled"
        )

        self.add_log(
            "Simulation reset."
        )

        self.update_display()