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

        self.swap_in_count = 0
        self.swap_out_count = 0

        # Default allocation strategy
        self.strategy = "First Fit"

    # =====================================
    # Allocation Strategy
    # =====================================

    def set_strategy(self, strategy):
        if strategy not in (
            "First Fit",
            "Best Fit",
            "Worst Fit",
        ):
            raise ValueError(
                "Invalid allocation strategy."
            )

        self.strategy = strategy

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

    # =====================================
    # Create Process
    # =====================================

    def create_process(self, size):
        if size <= 0:
            raise ValueError(
                "Process size must be greater than 0 MB."
            )

        if size > self.ram_size and size > self.swap_size:
            raise MemoryError(
                "Process is too large for RAM or Swap."
            )

        process = Process(
            f"P{self.next_pid}",
            size,
        )

        # Try RAM first
        if self.find_free_block(
            self.ram,
            size,
        ) != -1:

            success = self.allocate(
                self.ram,
                process,
            )

            if success:
                process.location = "RAM"

        # If RAM cannot fit, try Swap
        elif self.find_free_block(
            self.swap,
            size,
        ) != -1:

            success = self.allocate(
                self.swap,
                process,
            )

            if success:
                process.location = "SWAP"

        else:
            raise MemoryError(
                "Not enough contiguous RAM or Swap space."
            )

        self.next_pid += 1
        self.processes.append(process)

        return process

    # =====================================
    # Allocate Memory
    # =====================================

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

    # =====================================
    # Free Memory
    # =====================================

    def free_process(self, memory, process):
        for i in range(len(memory)):
            if memory[i] == process:
                memory[i] = None

    # =====================================
    # Free Space
    # =====================================

    def get_free_space(self, memory):
        return sum(
            1
            for block in memory
            if block is None
        )

    # =====================================
    # Fragmentation Analysis
    # =====================================

    def get_free_blocks(self, memory):
        """
        Return sizes of all continuous free blocks.
        Example:
        [P1, None, None, P2, None]
        -> [2, 1]
        """
        blocks = []
        current_size = 0

        for block in memory:
            if block is None:
                current_size += 1
            else:
                if current_size > 0:
                    blocks.append(current_size)
                    current_size = 0

        if current_size > 0:
            blocks.append(current_size)

        return blocks

    def get_free_block_count(self, memory):
        return len(
            self.get_free_blocks(memory)
        )

    def get_largest_free_block(self, memory):
        blocks = self.get_free_blocks(memory)

        if not blocks:
            return 0

        return max(blocks)

    def get_external_fragmentation(self, memory):
        """
        External fragmentation percentage:

        (Total Free Space - Largest Free Block)
        / Total Free Space * 100
        """

        total_free = self.get_free_space(
            memory
        )

        largest_free = self.get_largest_free_block(
            memory
        )

        if total_free == 0:
            return 0.0

        return (
            (total_free - largest_free)
            / total_free
        ) * 100

    def get_ram_fragmentation(self):
        return {
            "free_space": self.get_free_space(
                self.ram
            ),
            "free_blocks": self.get_free_block_count(
                self.ram
            ),
            "largest_block": self.get_largest_free_block(
                self.ram
            ),
            "external_fragmentation":
                self.get_external_fragmentation(
                    self.ram
                ),
        }

    def get_swap_fragmentation(self):
        return {
            "free_space": self.get_free_space(
                self.swap
            ),
            "free_blocks": self.get_free_block_count(
                self.swap
            ),
            "largest_block": self.get_largest_free_block(
                self.swap
            ),
            "external_fragmentation":
                self.get_external_fragmentation(
                    self.swap
                ),
        }

    # =====================================
    # Swap Out
    # =====================================

    def swap_out(self, process):
        if process not in self.processes:
            raise ValueError(
                "Process does not exist."
            )

        if process.location != "RAM":
            raise ValueError(
                "Process is not currently in RAM."
            )

        # Allocate in Swap first
        if not self.allocate(
            self.swap,
            process,
        ):
            raise MemoryError(
                "Not enough contiguous Swap space."
            )

        # Remove from RAM
        self.free_process(
            self.ram,
            process,
        )

        process.location = "SWAP"
        self.swap_out_count += 1

    # =====================================
    # Swap In
    # =====================================

    def swap_in(self, process):
        if process not in self.processes:
            raise ValueError(
                "Process does not exist."
            )

        if process.location != "SWAP":
            raise ValueError(
                "Process is not currently in Swap."
            )

        # Allocate RAM first
        if not self.allocate(
            self.ram,
            process,
        ):
            raise MemoryError(
                "Not enough contiguous RAM space."
            )

        # Remove from Swap
        self.free_process(
            self.swap,
            process,
        )

        process.location = "RAM"
        self.swap_in_count += 1

    # =====================================
    # Terminate Process
    # =====================================

    def terminate_process(self, process):
        if process not in self.processes:
            raise ValueError(
                "Process does not exist."
            )

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

        process.status = "Terminated"

        self.processes.remove(
            process
        )

    # =====================================
    # Find Process
    # =====================================

    def find_process(self, pid):
        for process in self.processes:
            if process.pid == pid:
                return process

        return None

    # =====================================
    # RAM Usage
    # =====================================

    def get_ram_usage(self):
        used = self.ram_size - self.get_free_space(
            self.ram
        )

        percent = (
            used / self.ram_size
        ) * 100

        return used, percent

    # =====================================
    # Swap Usage
    # =====================================

    def get_swap_usage(self):
        used = self.swap_size - self.get_free_space(
            self.swap
        )

        percent = (
            used / self.swap_size
        ) * 100

        return used, percent

    # =====================================
    # Reset
    # =====================================

    def reset(self):
        self.ram = [None] * self.ram_size
        self.swap = [None] * self.swap_size

        self.processes = []
        self.next_pid = 1

        self.swap_in_count = 0
        self.swap_out_count = 0

        self.strategy = "First Fit"