RED = "\033[31m"
GREEN = "\033[32m"
NORMAL = "\033[0m"
BLUE = "\033[34m"


def green(text: str):
    return GREEN + text + NORMAL


def red(text: str):
    return RED + text + NORMAL


def blue(text: str):
    return BLUE + text + NORMAL
