from models.process import Process


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

    # -------------------------
    # Create Process
    # -------------------------

    def create_process(self, size):

        if size <= 0:
            raise ValueError(
                "Process size must be greater than 0."
            )

        if size > self.ram_size:
            raise ValueError(
                "Process cannot be larger than RAM."
            )

        process = Process(
            f"P{self.next_pid}",
            size
        )

        # RAM has enough space
        if self.get_free_space(self.ram) >= size:

            self.allocate(
                self.ram,
                process
            )

            process.location = "RAM"

        # RAM full -> Swap
        elif self.get_free_space(self.swap) >= size:

            self.allocate(
                self.swap,
                process
            )

            process.location = "SWAP"

        else:

            raise MemoryError(
                "Not enough RAM or Swap space."
            )

        self.next_pid += 1
        self.processes.append(process)

        return process

    # -------------------------
    # Allocate Memory
    # -------------------------

    def allocate(self, memory, process):

        remaining = process.size

        for i in range(len(memory)):

            if memory[i] is None:

                memory[i] = process
                remaining -= 1

                if remaining == 0:
                    break

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

        return sum(
            1
            for block in memory
            if block is None
        )

    # -------------------------
    # Swap Out
    # -------------------------

    def swap_out(self, process):

        if process.location != "RAM":

            raise ValueError(
                "Process is not in RAM."
            )

        if self.get_free_space(self.swap) < process.size:

            raise MemoryError(
                "Not enough Swap space."
            )

        self.free_process(
            self.ram,
            process
        )

        self.allocate(
            self.swap,
            process
        )

        process.location = "SWAP"

        self.swap_out_count += 1

    # -------------------------
    # Swap In
    # -------------------------

    def swap_in(self, process):

        if process.location != "SWAP":

            raise ValueError(
                "Process is not in Swap."
            )

        if self.get_free_space(self.ram) < process.size:

            raise MemoryError(
                "Not enough RAM space."
            )

        self.free_process(
            self.swap,
            process
        )

        self.allocate(
            self.ram,
            process
        )

        process.location = "RAM"

        self.swap_in_count += 1

    # -------------------------
    # Terminate
    # -------------------------

    def terminate_process(self, process):

        if process.location == "RAM":

            self.free_process(
                self.ram,
                process
            )

        else:

            self.free_process(
                self.swap,
                process
            )

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

        used = (
            self.ram_size
            - self.get_free_space(self.ram)
        )

        percent = (
            used / self.ram_size
        ) * 100

        return used, percent

    # -------------------------
    # Swap Usage
    # -------------------------

    def get_swap_usage(self):

        used = (
            self.swap_size
            - self.get_free_space(self.swap)
        )

        percent = (
            used / self.swap_size
        ) * 100

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