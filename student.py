import colorful


class Student:
    """For managing student information"""

    def __init__(self, id: int, name: str, age: int) -> None:
        self.id = id  # required for constructor so you can easily get from the row using the pattern below
        self.name = name
        self.age = age

    def __str__(self) -> str:
        return colorful.blue(f"Name: {self.name}, ID: {self.id}, Age: {self.age}")
