import time


class WithLog:
    def __init__(self, label: str, print_log: bool = True) -> None:
        self.label = label
        self.print_log = print

    def __enter__(self):
        if self.print_log:
            print("start", self.label)
        self.start_time = time.time()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.end_time = time.time()
        # TODO error handling
        if self.print_log:
            print("finish", self.label)

    def print(self, *args):
        print(self.label, *args)
