from models.process import Process
from simulator.allocation import AllocationStrategy


class SwapManager:

    def __init__(self, ram_size=16, swap_size=16):
        self.ram_size = ram_size
        self.swap_size = swap_size

        self.ram = [None] * ram_size
        self.swap = [None] * swap_size

        self.processes = []
        self.next_pid = 1
        self.strategy = "First Fit"

        self.swap_in_count = 0
        self.swap_out_count = 0

    # -------------------------
    # Allocation Strategy
    # -------------------------

    def set_strategy(self, strategy):
        if strategy not in ("First Fit", "Best Fit", "Worst Fit"):
            raise ValueError("Invalid allocation strategy.")

        self.strategy = strategy

    def find_free_block(self, memory, size):
        if self.strategy == "First Fit":
            return AllocationStrategy.find_first_fit(memory, size)

        if self.strategy == "Best Fit":
            return AllocationStrategy.find_best_fit(memory, size)

        if self.strategy == "Worst Fit":
            return AllocationStrategy.find_worst_fit(memory, size)

        return -1

    # -------------------------
    # Create Process
    # -------------------------

    def create_process(self, size):
        process = Process(f"P{self.next_pid}", size)

        if self.find_free_block(self.ram, size) != -1:
            self.allocate(self.ram, process)

            process.location = "RAM"

        elif self.find_free_block(self.swap, size) != -1:
            self.allocate(self.swap, process)

            process.location = "SWAP"

        else:
            raise MemoryError("Not enough contiguous RAM or Swap space.")

        self.next_pid += 1
        self.processes.append(process)

        return process

    # -------------------------
    # Allocate Memory
    # -------------------------

    def allocate(self, memory, process):
        start = self.find_free_block(memory, process.size)

        if start == -1:
            return False

        for i in range(start, start + process.size):
            memory[i] = process

        return True

    # -------------------------
    # Free Memory
    # -------------------------

    def free_process(self, memory, process):

        for i in range(len(memory)):

            if memory[i] == process:
                memory[i] = None

    # -------------------------
    # Free Space
    # -------------------------

    def get_free_space(self, memory):

        return sum(1 for block in memory if block is None)

    # -------------------------
    # Swap Out
    # -------------------------

    def swap_out(self, process):

        if process.location != "RAM":

            raise ValueError("Process is not in RAM.")

        if self.get_free_space(self.swap) < process.size:

            raise MemoryError("Not enough Swap space.")

        self.free_process(self.ram, process)

        self.allocate(self.swap, process)

        process.location = "SWAP"

        self.swap_out_count += 1

    # -------------------------
    # Swap In
    # -------------------------

    def swap_in(self, process):

        if process.location != "SWAP":

            raise ValueError("Process is not in Swap.")

        if self.get_free_space(self.ram) < process.size:

            raise MemoryError("Not enough RAM space.")

        self.free_process(self.swap, process)

        self.allocate(self.ram, process)

        process.location = "RAM"

        self.swap_in_count += 1

    # -------------------------
    # Terminate
    # -------------------------

    def terminate_process(self, process):

        if process.location == "RAM":

            self.free_process(self.ram, process)

        else:

            self.free_process(self.swap, process)

        process.status = "Terminated"

        self.processes.remove(process)

    # -------------------------
    # Find Process
    # -------------------------

    def find_process(self, pid):

        for process in self.processes:

            if process.pid == pid:
                return process

        return None

    # -------------------------
    # RAM Usage
    # -------------------------

    def get_ram_usage(self):

        used = self.ram_size - self.get_free_space(self.ram)

        percent = (used / self.ram_size) * 100

        return used, percent

    # -------------------------
    # Swap Usage
    # -------------------------

    def get_swap_usage(self):

        used = self.swap_size - self.get_free_space(self.swap)

        percent = (used / self.swap_size) * 100

        return used, percent

    # -------------------------
    # Reset
    # -------------------------

    def reset(self):

        self.ram = [None] * self.ram_size
        self.swap = [None] * self.swap_size

        self.processes.clear()

        self.next_pid = 1

        self.swap_in_count = 0
        self.swap_out_count = 0
