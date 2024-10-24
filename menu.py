from __future__ import annotations
from typing import Callable

import colorful


class Option:
    def __init__(self, num: int, string: str, callback: Callable) -> None:
        self.num = num
        self.string = string
        self.callback = callback

    def __str__(self) -> str:
        return colorful.green(f"{self.num}: {self.string}")

    def execute(self):
        self.callback()


class Menu:
    def __init__(self, options: list[Option]) -> None:
        self.options = options

    def __str__(self) -> str:
        return "\n".join([option.__str__() for option in self.options])

    def exec_input(self):
        command = input("Enter choice: ")
        for option in self.options:
            if int(command) == option.num:
                option.execute()
                return
        self.exec_input()

    def render(self):
        print(self)
