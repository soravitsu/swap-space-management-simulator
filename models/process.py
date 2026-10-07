class Process:
    def __init__(self, pid, size):
        self.pid = pid
        self.size = size
        self.location = "RAM"
        self.status = "Running"

    def __str__(self):
        return f"{self.pid} ({self.size} MB) - {self.location}"