import sqlite3
from menu import Menu, Option
from student import Student
from student_repo import StudentRepo
import colorful

CONTINUE = "Press any key to continue..."


def counter():
    i = 1
    while True:
        yield i
        i += 1


class InputHandler:
    def __init__(self, repo: StudentRepo) -> None:
        self.count = counter()
        self.menu = Menu(
            [
                Option(
                    next(self.count), "Display all students", self.display_all_students
                ),
                Option(next(self.count), "Add Student", self.add_student),
                Option(next(self.count), "Find Student", self.query_student),
                Option(next(self.count), "Update Student", self.update_student),
                Option(next(self.count), "Delete Student", self.delete_student),
                Option(next(self.count), "Quit", self.quit),
            ]
        )
        self.repo = repo

    def add_student(self):
        name = input("What's the student's name?")
        age = int(input("What's the student's age?"))
        student = Student(0, name, age)
        id = self.repo.save_student(student)
        if id != None:
            student.id = id
            print("Student added!")
            print(student)
            input(CONTINUE)
        else:
            raise Exception("id is None, this is a big problem!")

    def query_student(self):
        print("Query student by name: ")
        name = input("Enter name to search for: ")
        students = self.repo.fetch_by_name(name)
        if students == None:
            raise Exception("This should not happen!")
        else:
            for student in students:
                print(student)
        input(CONTINUE)

    def display_all_students(self):
        print("All students: ")
        students = self.repo.all_students()
        if students != None:
            for student in students:
                print(student)
        input(CONTINUE)

    def update_student(self):
        print("Update student: ")
        id = input("Enter student id: ")
        student = None
        student = self.repo.fetch_by_id(int(id))
        if student == None:
            print(f"Student with id: {id} not found in database. Please try again.")
        assert student != None
        print(student)
        name = input("Enter new student name (leave blank to skip): ") or student.name
        age = input("Enter new student age (leave blank to skip): ") or student.age
        try:
            student = Student(int(id), name, int(age))
            print("Updating student with new data: ", student)
            result = self.repo.update_student(student)
            if result == False:
                print("Student not found!")
            else:
                print("Student updated!")
        except ValueError as e:
            print(colorful.red("Be sure to enter a number for id and age!"))
        finally:
            input(CONTINUE)

    def delete_student(self):
        id = input("Enter id of student to delete: ")
        try:
            id = int(id)
            result = self.repo.delete_student(id)
            if result:
                print(f"Student with id: {id} deleted!")
            else:
                print("Student not found!")
        except ValueError as e:
            print(colorful.red(f"Invalid input: {e}"))
            print("Please try again.")
            self.delete_student()
        except sqlite3.Error as e:
            print(colorful.red(f"Database error; student not deleted: {e}"))
        finally:
            input(CONTINUE)

    def quit(self):
        print("Bye!")
        self.repo.close()
        exit()

    def render(self):
        self.menu.render()

    def handle_input(self):
        self.menu.exec_input()
