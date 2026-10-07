from models.process import Process
from simulator.allocation import AllocationStrategy


class SwapManager:
    ALLOWED_SIZES = (16, 32, 64)

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

    def set_strategy(self, strategy):
        if strategy not in (
            "First Fit",
            "Best Fit",
            "Worst Fit",
        ):
            raise ValueError("Invalid allocation strategy.")

        self.strategy = strategy

    def set_memory_size(self, ram_size, swap_size):
        if ram_size not in self.ALLOWED_SIZES:
            raise ValueError("RAM must be 16, 32, or 64 MB.")

        if swap_size not in self.ALLOWED_SIZES:
            raise ValueError("Swap must be 16, 32, or 64 MB.")

        self.ram_size = ram_size
        self.swap_size = swap_size

        self.ram = [None] * ram_size
        self.swap = [None] * swap_size

        self.processes = []
        self.next_pid = 1

        self.swap_in_count = 0
        self.swap_out_count = 0

    def find_free_block(self, memory, size):
        if self.strategy == "First Fit":
            return AllocationStrategy.find_first_fit(
                memory,
                size,
            )

        if self.strategy == "Best Fit":
            return AllocationStrategy.find_best_fit(
                memory,
                size,
            )

        if self.strategy == "Worst Fit":
            return AllocationStrategy.find_worst_fit(
                memory,
                size,
            )

        return -1

    def allocate(self, memory, process):
        start = self.find_free_block(
            memory,
            process.size,
        )

        if start == -1:
            return False

        for i in range(
            start,
            start + process.size,
        ):
            memory[i] = process

        return True

    def create_process(self, size):
        if size <= 0:
            raise ValueError(
                "Process size must be greater than 0 MB."
            )

        if size > max(
            self.ram_size,
            self.swap_size,
        ):
            raise MemoryError(
                "Process is too large for available memory."
            )

        process = Process(
            f"P{self.next_pid}",
            size,
        )

        if self.find_free_block(
            self.ram,
            size,
        ) != -1:
            self.allocate(
                self.ram,
                process,
            )
            process.location = "RAM"

        elif self.find_free_block(
            self.swap,
            size,
        ) != -1:
            self.allocate(
                self.swap,
                process,
            )
            process.location = "SWAP"

        else:
            raise MemoryError(
                "Not enough contiguous RAM or Swap space."
            )

        self.processes.append(process)
        self.next_pid += 1

        return process

    def free_process(self, memory, process):
        for i in range(len(memory)):
            if memory[i] == process:
                memory[i] = None

    def get_free_space(self, memory):
        return sum(
            1
            for block in memory
            if block is None
        )

    def get_free_blocks(self, memory):
        count = 0
        inside = False

        for block in memory:
            if block is None:
                if not inside:
                    count += 1
                    inside = True
            else:
                inside = False

        return count

    def get_largest_free_block(self, memory):
        largest = 0
        current = 0

        for block in memory:
            if block is None:
                current += 1
                largest = max(
                    largest,
                    current,
                )
            else:
                current = 0

        return largest

    def get_external_fragmentation(self, memory):
        total_free = self.get_free_space(memory)

        if total_free == 0:
            return 0

        largest = self.get_largest_free_block(memory)

        return (
            (total_free - largest)
            / total_free
        ) * 100

    def get_ram_usage(self):
        used = (
            self.ram_size
            - self.get_free_space(self.ram)
        )

        percent = (
            used / self.ram_size * 100
        )

        return used, percent

    def get_swap_usage(self):
        used = (
            self.swap_size
            - self.get_free_space(self.swap)
        )

        percent = (
            used / self.swap_size * 100
        )

        return used, percent

    def find_process(self, pid):
        for process in self.processes:
            if process.pid == pid:
                return process

        return None

    def swap_out(self, process):
        if process.location != "RAM":
            raise ValueError(
                "Process is not currently in RAM."
            )

        if self.find_free_block(
            self.swap,
            process.size,
        ) == -1:
            raise MemoryError(
                "Not enough contiguous Swap space."
            )

        self.free_process(
            self.ram,
            process,
        )

        self.allocate(
            self.swap,
            process,
        )

        process.location = "SWAP"
        self.swap_out_count += 1

    def swap_in(self, process):
        if process.location != "SWAP":
            raise ValueError(
                "Process is not currently in Swap."
            )

        if self.find_free_block(
            self.ram,
            process.size,
        ) == -1:
            raise MemoryError(
                "Not enough contiguous RAM space."
            )

        self.free_process(
            self.swap,
            process,
        )

        self.allocate(
            self.ram,
            process,
        )

        process.location = "RAM"
        self.swap_in_count += 1

    def terminate_process(self, process):
        if process.location == "RAM":
            self.free_process(
                self.ram,
                process,
            )

        elif process.location == "SWAP":
            self.free_process(
                self.swap,
                process,
            )

        if process in self.processes:
            self.processes.remove(process)

    def reset(self):
        self.ram = [None] * self.ram_size
        self.swap = [None] * self.swap_size

        self.processes.clear()

        self.next_pid = 1

        self.swap_in_count = 0
        self.swap_out_count = 0