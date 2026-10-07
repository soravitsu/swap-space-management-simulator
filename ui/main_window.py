import tkinter as tk
from tkinter import ttk, messagebox

from simulator.swap_manager import SwapManager


class MainWindow:

    def __init__(self, root):
        self.root = root

        self.root.title(
            "Swap Space Management Simulator"
        )

        self.root.geometry(
            "1200x800"
        )

        self.root.minsize(
            1000,
            700
        )

        # =====================================
        # Simulation Manager
        # =====================================

        self.manager = SwapManager(
            ram_size=16,
            swap_size=16
        )

        # =====================================
        # Process Colors
        # =====================================

        self.process_colors = [
            "#A8DADC",
            "#BDE0FE",
            "#CDB4DB",
            "#FFC8DD",
            "#FFAFCC",
            "#B7E4C7",
            "#D9ED92",
            "#FFD6A5",
            "#CAFFBF",
            "#9BF6FF"
        ]

        # =====================================
        # Create UI
        # =====================================

        self.setup_style()

        self.create_header()
        self.create_memory_area()
        self.create_controls()
        self.create_process_table()
        self.create_statistics()
        self.create_log()

        self.update_display()

    # =========================================================
    # Style
    # =========================================================

    def setup_style(self):
        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Title.TLabel",
            font=("Arial", 24, "bold")
        )

        style.configure(
            "Subtitle.TLabel",
            font=("Arial", 10)
        )

        style.configure(
            "Section.TLabelframe",
            padding=10
        )

        style.configure(
            "Section.TLabelframe.Label",
            font=("Arial", 10, "bold")
        )

        style.configure(
            "Control.TButton",
            padding=(10, 5)
        )

        style.configure(
            "Treeview",
            rowheight=26,
            font=("Arial", 10)
        )

        style.configure(
            "Treeview.Heading",
            font=("Arial", 10, "bold")
        )

    # =========================================================
    # Header
    # =========================================================

    def create_header(self):
        frame = ttk.Frame(
            self.root,
            padding=(20, 15, 20, 8)
        )

        frame.pack(
            fill="x"
        )

        ttk.Label(
            frame,
            text="Swap Space Management Simulator",
            style="Title.TLabel"
        ).pack()

        ttk.Label(
            frame,
            text="Operating System Memory Management Simulation",
            style="Subtitle.TLabel"
        ).pack(
            pady=(4, 0)
        )

    # =========================================================
    # Memory Area
    # =========================================================

    def create_memory_area(self):
        frame = ttk.Frame(
            self.root,
            padding=(20, 5, 20, 5)
        )

        frame.pack(
            fill="x"
        )

        # -------------------------------------
        # RAM
        # -------------------------------------

        self.ram_frame = ttk.LabelFrame(
            frame,
            text="RAM Memory (16 MB)",
            padding=10,
            style="Section.TLabelframe"
        )

        self.ram_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 8)
        )

        self.ram_canvas = tk.Canvas(
            self.ram_frame,
            height=150,
            bg="#F8F9FA",
            highlightthickness=1,
            highlightbackground="#D0D0D0"
        )

        self.ram_canvas.pack(
            fill="both",
            expand=True
        )

        self.ram_usage = ttk.Label(
            self.ram_frame,
            font=("Arial", 10, "bold")
        )

        self.ram_usage.pack(
            pady=(8, 0)
        )

        # -------------------------------------
        # Swap
        # -------------------------------------

        self.swap_frame = ttk.LabelFrame(
            frame,
            text="Swap Space (16 MB)",
            padding=10,
            style="Section.TLabelframe"
        )

        self.swap_frame.pack(
            side="right",
            fill="both",
            expand=True,
            padx=(8, 0)
        )

        self.swap_canvas = tk.Canvas(
            self.swap_frame,
            height=150,
            bg="#F8F9FA",
            highlightthickness=1,
            highlightbackground="#D0D0D0"
        )

        self.swap_canvas.pack(
            fill="both",
            expand=True
        )

        self.swap_usage = ttk.Label(
            self.swap_frame,
            font=("Arial", 10, "bold")
        )

        self.swap_usage.pack(
            pady=(8, 0)
        )

    # =========================================================
    # Controls
    # =========================================================

    def create_controls(self):
        frame = ttk.LabelFrame(
            self.root,
            text="Simulation Controls",
            padding=10,
            style="Section.TLabelframe"
        )

        frame.pack(
            fill="x",
            padx=20,
            pady=8
        )

        # -------------------------------------
        # RAM Size
        # -------------------------------------

        ttk.Label(
            frame,
            text="RAM Size:"
        ).pack(
            side="left",
            padx=(5, 3)
        )

        self.ram_size_var = tk.StringVar(
            value="16 MB"
        )

        self.ram_size_combo = ttk.Combobox(
            frame,
            textvariable=self.ram_size_var,
            values=[
                "16 MB",
                "32 MB",
                "64 MB"
            ],
            state="readonly",
            width=8
        )

        self.ram_size_combo.pack(
            side="left",
            padx=(0, 12)
        )

        # -------------------------------------
        # Swap Size
        # -------------------------------------

        ttk.Label(
            frame,
            text="Swap Size:"
        ).pack(
            side="left",
            padx=(0, 3)
        )

        self.swap_size_var = tk.StringVar(
            value="16 MB"
        )

        self.swap_size_combo = ttk.Combobox(
            frame,
            textvariable=self.swap_size_var,
            values=[
                "16 MB",
                "32 MB",
                "64 MB"
            ],
            state="readonly",
            width=8
        )

        self.swap_size_combo.pack(
            side="left",
            padx=(0, 12)
        )

        # -------------------------------------
        # Apply Configuration
        # -------------------------------------

        ttk.Button(
            frame,
            text="Apply Configuration",
            command=self.apply_configuration,
            style="Control.TButton"
        ).pack(
            side="left",
            padx=(0, 18)
        )

        # -------------------------------------
        # Allocation Strategy
        # -------------------------------------

        ttk.Label(
            frame,
            text="Allocation Strategy:"
        ).pack(
            side="left",
            padx=(0, 3)
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
            padx=(0, 15)
        )

        self.strategy_combo.bind(
            "<<ComboboxSelected>>",
            self.change_strategy
        )

        # -------------------------------------
        # Create Process
        # -------------------------------------

        ttk.Button(
            frame,
            text="Create Process",
            command=self.create_process,
            style="Control.TButton"
        ).pack(
            side="left",
            padx=3
        )

        # -------------------------------------
        # Swap In
        # -------------------------------------

        ttk.Button(
            frame,
            text="Swap In",
            command=self.swap_in,
            style="Control.TButton"
        ).pack(
            side="left",
            padx=3
        )

        # -------------------------------------
        # Swap Out
        # -------------------------------------

        ttk.Button(
            frame,
            text="Swap Out",
            command=self.swap_out,
            style="Control.TButton"
        ).pack(
            side="left",
            padx=3
        )

        # -------------------------------------
        # Terminate
        # -------------------------------------

        ttk.Button(
            frame,
            text="Terminate Process",
            command=self.terminate_process,
            style="Control.TButton"
        ).pack(
            side="left",
            padx=3
        )

        # -------------------------------------
        # Reset
        # -------------------------------------

        ttk.Button(
            frame,
            text="Reset",
            command=self.reset,
            style="Control.TButton"
        ).pack(
            side="right",
            padx=5
        )

    # =========================================================
    # Apply Configuration
    # =========================================================

    def apply_configuration(self):
        ram_size = int(
            self.ram_size_var.get().replace(
                " MB",
                ""
            )
        )

        swap_size = int(
            self.swap_size_var.get().replace(
                " MB",
                ""
            )
        )

        answer = messagebox.askyesno(
            "Apply Configuration",
            (
                "Changing memory size will reset "
                "the current simulation.\n\n"
                f"RAM: {ram_size} MB\n"
                f"Swap: {swap_size} MB\n\n"
                "Continue?"
            )
        )

        if not answer:
            return

        strategy = self.strategy_var.get()

        try:
            self.manager = SwapManager(
                ram_size=ram_size,
                swap_size=swap_size
            )

            self.manager.set_strategy(
                strategy
            )

            self.add_log(
                f"Configuration → "
                f"RAM {ram_size} MB, "
                f"Swap {swap_size} MB"
            )

            self.update_display()

        except ValueError as error:
            messagebox.showerror(
                "Configuration Error",
                str(error)
            )

    # =========================================================
    # Change Strategy
    # =========================================================

    def change_strategy(self, event=None):
        strategy = self.strategy_var.get()

        try:
            self.manager.set_strategy(
                strategy
            )

            self.add_log(
                f"Allocation Strategy → "
                f"{strategy}"
            )

        except ValueError as error:
            messagebox.showerror(
                "Allocation Strategy",
                str(error)
            )

    # =========================================================
    # Process Table
    # =========================================================

    def create_process_table(self):
        frame = ttk.LabelFrame(
            self.root,
            text="Process Table",
            padding=10,
            style="Section.TLabelframe"
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
            height=6
        )

        self.process_table.heading(
            "PID",
            text="PID"
        )

        self.process_table.heading(
            "Size",
            text="Size"
        )

        self.process_table.heading(
            "Location",
            text="Location"
        )

        self.process_table.heading(
            "Status",
            text="Status"
        )

        self.process_table.column(
            "PID",
            width=100,
            anchor="center"
        )

        self.process_table.column(
            "Size",
            width=150,
            anchor="center"
        )

        self.process_table.column(
            "Location",
            width=180,
            anchor="center"
        )

        self.process_table.column(
            "Status",
            width=180,
            anchor="center"
        )

        self.process_table.pack(
            fill="x"
        )

    # =========================================================
    # Statistics
    # =========================================================

    def create_statistics(self):
        frame = ttk.LabelFrame(
            self.root,
            text="Simulation Statistics",
            padding=10,
            style="Section.TLabelframe"
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

        self.largest_free_label = ttk.Label(
            frame,
            text="Largest Free Block: 16 MB"
        )

        self.largest_free_label.pack(
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

    # =========================================================
    # Event Log
    # =========================================================

    def create_log(self):
        frame = ttk.LabelFrame(
            self.root,
            text="Event Log",
            padding=8,
            style="Section.TLabelframe"
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(5, 15)
        )

        self.log = tk.Text(
            frame,
            height=7,
            state="disabled",
            font=("Consolas", 10),
            bg="#FAFAFA",
            relief="solid",
            borderwidth=1
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

    # =========================================================
    # Create Process
    # =========================================================

    def create_process(self):
        dialog = tk.Toplevel(
            self.root
        )

        dialog.title(
            "Create Process"
        )

        dialog.geometry(
            "340x210"
        )

        dialog.resizable(
            False,
            False
        )

        dialog.transient(
            self.root
        )

        dialog.grab_set()

        ttk.Label(
            dialog,
            text="Create New Process",
            font=("Arial", 13, "bold")
        ).pack(
            pady=(20, 10)
        )

        ttk.Label(
            dialog,
            text="Process Size (MB):"
        ).pack(
            pady=(5, 5)
        )

        entry = ttk.Entry(
            dialog,
            width=20
        )

        entry.pack()

        entry.focus()

        def confirm():
            try:
                size = int(
                    entry.get()
                )

                if size <= 0:
                    raise ValueError(
                        "Process size must be greater than 0."
                    )

                process = (
                    self.manager.create_process(
                        size
                    )
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
                    str(error),
                    parent=dialog
                )

            except MemoryError as error:
                messagebox.showwarning(
                    "Memory Full",
                    str(error),
                    parent=dialog
                )

        ttk.Button(
            dialog,
            text="Create",
            command=confirm
        ).pack(
            pady=20
        )

        dialog.bind(
            "<Return>",
            lambda event: confirm()
        )

    # =========================================================
    # Get Selected Process
    # =========================================================

    def get_selected_process(self):
        selection = (
            self.process_table.selection()
        )

        if not selection:
            messagebox.showinfo(
                "No Process Selected",
                "Please select a process first."
            )

            return None

        values = self.process_table.item(
            selection[0]
        )["values"]

        pid = values[0]

        return self.manager.find_process(
            pid
        )

    # =========================================================
    # Swap Out
    # =========================================================

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

    # =========================================================
    # Swap In
    # =========================================================

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

    # =========================================================
    # Terminate Process
    # =========================================================

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

    # =========================================================
    # Get Process Color
    # =========================================================

    def get_process_color(self, pid):
        try:
            number = int(
                str(pid).replace(
                    "P",
                    ""
                )
            )

            index = (
                number - 1
            ) % len(
                self.process_colors
            )

            return self.process_colors[
                index
            ]

        except (
            ValueError,
            TypeError
        ):
            return "#BDE0FE"

    # =========================================================
    # Get Memory Segments
    # =========================================================

    def get_memory_segments(self, memory):
        segments = []

        if not memory:
            return segments

        start = 0
        current = memory[0]

        for index in range(
            1,
            len(memory)
        ):

            if memory[index] is not current:

                segments.append(
                    (
                        start,
                        index,
                        current
                    )
                )

                start = index
                current = memory[index]

        segments.append(
            (
                start,
                len(memory),
                current
            )
        )

        return segments

    # =========================================================
    # Draw Memory
    # =========================================================

    def draw_memory(
        self,
        canvas,
        memory,
        total_size=None
    ):
        canvas.delete(
            "all"
        )

        if not memory:
            return

        if total_size is None:
            total_size = len(memory)

        width = canvas.winfo_width()
        height = canvas.winfo_height()

        if width <= 1:
            width = 600

        if height <= 1:
            height = 150

        # -------------------------------------
        # Memory Area
        # -------------------------------------

        left = 18
        right = width - 18

        top = 35
        bottom = height - 35

        memory_width = right - left

        # -------------------------------------
        # Background
        # -------------------------------------

        canvas.create_rectangle(
            left,
            top,
            right,
            bottom,
            fill="#F5F6F7",
            outline="#777777",
            width=1
        )

        # -------------------------------------
        # Scale
        # -------------------------------------

        canvas.create_text(
            left,
            18,
            text="0 MB",
            anchor="w",
            font=("Arial", 8),
            fill="#555555"
        )

        canvas.create_text(
            right,
            18,
            text=f"{total_size} MB",
            anchor="e",
            font=("Arial", 8),
            fill="#555555"
        )

        # -------------------------------------
        # Get Segments
        # -------------------------------------

        segments = self.get_memory_segments(
            memory
        )

        # -------------------------------------
        # Draw Segments
        # -------------------------------------

        for (
            start_index,
            end_index,
            process
        ) in segments:

            segment_size = (
                end_index
                - start_index
            )

            x1 = (
                left
                + (
                    start_index
                    / total_size
                )
                * memory_width
            )

            x2 = (
                left
                + (
                    end_index
                    / total_size
                )
                * memory_width
            )

            segment_width = (
                x2 - x1
            )

            # Default values
            fill_color = "#EEF1F4"
            text_label = "Free"
            font_size = 7

            # ---------------------------------
            # Process Segment
            # ---------------------------------

            if process is not None:

                fill_color = (
                    self.get_process_color(
                        process.pid
                    )
                )

                # Large block
                if segment_width >= 45:

                    text_label = (
                        f"{process.pid}\n"
                        f"{segment_size} MB"
                    )

                    font_size = 9

                # Medium block
                elif segment_width >= 18:

                    text_label = (
                        process.pid
                    )

                    font_size = 8

                # Small block
                else:

                    text_label = (
                        process.pid
                    )

                    font_size = 7

            # ---------------------------------
            # Draw Rectangle
            # ---------------------------------

            canvas.create_rectangle(
                x1,
                top,
                x2,
                bottom,
                fill=fill_color,
                outline="#999999",
                width=1
            )

            # ---------------------------------
            # Draw Text
            # ---------------------------------

            if segment_width >= 10:

                canvas.create_text(
                    (x1 + x2) / 2,
                    (top + bottom) / 2,
                    text=text_label,
                    font=(
                        "Arial",
                        font_size,
                        "bold"
                    ),
                    fill="#222222",
                    justify="center"
                )

        # -------------------------------------
        # Bottom Scale
        # -------------------------------------

        canvas.create_text(
            left,
            bottom + 13,
            anchor="w",
            text="Start",
            font=("Arial", 8),
            fill="#777777"
        )

        canvas.create_text(
            right,
            bottom + 13,
            anchor="e",
            text="End",
            font=("Arial", 8),
            fill="#777777"
        )

    # =========================================================
    # Fragmentation
    # =========================================================

    def calculate_fragmentation(
        self,
        memory
    ):
        if not memory:
            return 0, 0, 0

        free_blocks = []

        current_free = 0

        for cell in memory:

            if cell is None:

                current_free += 1

            else:

                if current_free > 0:

                    free_blocks.append(
                        current_free
                    )

                    current_free = 0

        if current_free > 0:

            free_blocks.append(
                current_free
            )

        if not free_blocks:
            return 0, 0, 0

        total_free = sum(
            free_blocks
        )

        largest_free = max(
            free_blocks
        )

        if total_free == 0:

            fragmentation = 0

        else:

            fragmentation = (
                (
                    total_free
                    - largest_free
                )
                / total_free
            ) * 100

        return (
            len(free_blocks),
            largest_free,
            fragmentation
        )

    # =========================================================
    # Update Memory Titles
    # =========================================================

    def update_memory_titles(self):
        self.ram_frame.config(
            text=(
                f"RAM Memory "
                f"({self.manager.ram_size} MB)"
            )
        )

        self.swap_frame.config(
            text=(
                f"Swap Space "
                f"({self.manager.swap_size} MB)"
            )
        )

    # =========================================================
    # Update Display
    # =========================================================

    def update_display(self):

        # -------------------------------------
        # Memory Visualization
        # -------------------------------------

        self.draw_memory(
            self.ram_canvas,
            self.manager.ram,
            self.manager.ram_size
        )

        self.draw_memory(
            self.swap_canvas,
            self.manager.swap,
            self.manager.swap_size
        )

        # -------------------------------------
        # Titles
        # -------------------------------------

        self.update_memory_titles()

        # -------------------------------------
        # RAM Usage
        # -------------------------------------

        ram_used, ram_percent = (
            self.manager.get_ram_usage()
        )

        # -------------------------------------
        # Swap Usage
        # -------------------------------------

        swap_used, swap_percent = (
            self.manager.get_swap_usage()
        )

        # -------------------------------------
        # Available Space
        # -------------------------------------

        ram_available = (
            self.manager.ram_size
            - ram_used
        )

        swap_available = (
            self.manager.swap_size
            - swap_used
        )

        # -------------------------------------
        # Fragmentation
        # -------------------------------------

        (
            free_blocks,
            largest_free,
            fragmentation
        ) = self.calculate_fragmentation(
            self.manager.ram
        )

        # -------------------------------------
        # Usage Labels
        # -------------------------------------

        self.ram_usage.config(
            text=(
                f"RAM Usage: "
                f"{ram_used}/"
                f"{self.manager.ram_size} MB "
                f"({ram_percent:.0f}%)"
            )
        )

        self.swap_usage.config(
            text=(
                f"Swap Usage: "
                f"{swap_used}/"
                f"{self.manager.swap_size} MB "
                f"({swap_percent:.0f}%)"
            )
        )

        # -------------------------------------
        # Statistics
        # -------------------------------------

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

        self.free_blocks_label.config(
            text=(
                f"Free Blocks: "
                f"{free_blocks}"
            )
        )

        self.largest_free_label.config(
            text=(
                f"Largest Free Block: "
                f"{largest_free} MB"
            )
        )

        self.fragmentation_label.config(
            text=(
                f"External Fragmentation: "
                f"{fragmentation:.0f}%"
            )
        )

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

        # -------------------------------------
        # Process Table
        # -------------------------------------

        for item in (
            self.process_table.get_children()
        ):
            self.process_table.delete(
                item
            )

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

    # =========================================================
    # Reset
    # =========================================================

    def reset(self):

        answer = messagebox.askyesno(
            "Reset Simulator",
            "Reset the entire simulation?"
        )

        if not answer:
            return

        current_strategy = (
            self.strategy_var.get()
        )

        current_ram = (
            self.manager.ram_size
        )

        current_swap = (
            self.manager.swap_size
        )

        self.manager = SwapManager(
            ram_size=current_ram,
            swap_size=current_swap
        )

        self.manager.set_strategy(
            current_strategy
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