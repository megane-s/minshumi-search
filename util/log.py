import time
from typing import TypeAlias

WithLogType: TypeAlias = "WithLog"

_depth = 0


class WithLog:
    """usage
    with WithLog() as logger:
        logger.print()
    """

    def __init__(
        self,
        label: str,
        print_log: bool = True,
        print_time: bool = True,
        start_label: str = "⭐️ start ::",
        end_label: str = "✅ finish ::",
        indent_text: str = "  ",
    ) -> None:
        self.label = label
        self.print_log = print_log
        self.print_time = print_time
        self.start_label = start_label
        self.end_label = end_label
        self.indent_text = indent_text

    def __enter__(self):
        global _depth, _with_logs
        self.depth = _depth
        _depth += 1

        if self.print_log:
            print(
                self.indent_text * (self.get_depth()),
                self.start_label,
                self.label,
            )
        self.start_time = time.time()

        return self

    def __exit__(self, exception_type, exception_value, traceback):
        # TODO error handling

        self.end_time = time.time()

        if self.print_log:
            if self.print_time:
                if self.depth is None:
                    print(f"⚠️ invalid depth {self.depth} . set 1 .")
                    self.depth = 1
                print(
                    self.indent_text * (self.depth),
                    self.end_label,
                    self.label,
                    f"time={self.end_time - self.start_time}s",
                )
            else:
                print(
                    self.end_label,
                    self.label,
                )

        global _depth
        self.depth = None
        _depth -= 1

    def print(self, *args, **kwargs):
        print(
            self.indent_text*self.get_depth(),
            *args,
            **kwargs
        )

    def get_depth(self):
        global _depth
        if self.depth is None:
            print(f"⚠️ invalid depth {self.depth} . set {_depth} .")
            self.depth = _depth
        return self.depth
