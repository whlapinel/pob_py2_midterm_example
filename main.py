from student_repo import StudentRepo
from handler import InputHandler


def main():
    repo = StudentRepo()
    interface = InputHandler(repo)

    while True:
        interface.render()
        interface.handle_input()


if __name__ == "__main__":
    main()
