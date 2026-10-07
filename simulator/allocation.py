class AllocationStrategy:
    """
    Memory allocation strategies for the simulator.
    """

    @staticmethod
    def find_first_fit(memory, size):
        """Find the first available continuous block."""
        start = 0

        while start < len(memory):
            if memory[start] is not None:
                start += 1
                continue

            end = start

            while end < len(memory) and memory[end] is None:
                end += 1

            if end - start >= size:
                return start

            start = end

        return -1

    @staticmethod
    def find_best_fit(memory, size):
        """Find the smallest free block that can fit the process."""
        best_start = -1
        best_size = float("inf")

        start = 0

        while start < len(memory):
            if memory[start] is not None:
                start += 1
                continue

            end = start

            while end < len(memory) and memory[end] is None:
                end += 1

            block_size = end - start

            if block_size >= size and block_size < best_size:
                best_start = start
                best_size = block_size

            start = end

        return best_start

    @staticmethod
    def find_worst_fit(memory, size):
        """Find the largest free block that can fit the process."""
        worst_start = -1
        worst_size = -1

        start = 0

        while start < len(memory):
            if memory[start] is not None:
                start += 1
                continue

            end = start

            while end < len(memory) and memory[end] is None:
                end += 1

            block_size = end - start

            if block_size >= size and block_size > worst_size:
                worst_start = start
                worst_size = block_size

            start = end

        return worst_start