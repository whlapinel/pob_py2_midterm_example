import sqlite3
from student import Student


class StudentRepo:
    """Student Repository Class, for managing persistence of Student objects."""

    def __init__(self) -> None:
        self.conn = sqlite3.connect("students.db")
        self.conn.row_factory = sqlite3.Row
        self.create_table()

    def create_table(self):
        """
        Creates the students table in the sqlite database.

        Params:
            conn (sqlite3.Connection): The database connection.

        Returns:
            None
        """
        sql = """
        CREATE TABLE if not exists students (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER NOT NULL
        )
        """
        try:
            self.conn.execute(sql)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def fetch_by_name(self, name: str):
        """
        Fetch a student from the database by name.

        Params:
            conn (sqlite3.Connection): The database connection.
            name (str): The name of the student to fetch.

        Returns:
            list[Student]: A list of Student objects.
        """
        sql = """
        SELECT * FROM students where name LIKE ?
        """
        try:
            cursor = self.conn.cursor()
            args = (f"%{name}%",)
            cursor.execute(sql, args)
            self.conn.commit()
            rows = cursor.fetchall()
            students = []
            if rows:
                for row in rows:
                    student = Student(**row)
                    students.append(student)
            return students
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def fetch_by_id(self, id: int):
        """
        Fetch a student from the database by id.

        Params:
            conn (sqlite3.Connection): The database connection.
            id (int): The id of the student to fetch.

        Returns:
            Student: The Student object with the fetched data.
            None: if student is not found in the database.
        """
        sql = """
        SELECT * FROM students where id = ?
        """
        try:
            cursor = self.conn.cursor()
            args = (id,)
            cursor.execute(sql, args)
            self.conn.commit()
            row = cursor.fetchone()
            if row:
                student = Student(**row)
                return student
            return None
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def all_students(self):
        """
        Fetch all students from the database.

        Returns:
            list[Student]: A list of Student objects retrieved from database.
            None: if student is not found in the database.
        """
        sql = """
        SELECT * FROM students
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            self.conn.commit()
            rows = cursor.fetchall()
            students = []
            if rows:
                for row in rows:
                    student = Student(**row)
                    students.append(student)
            return students
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def save_student(self, student: Student):
        """
        Creates the students table in the sqlite database.

        Params:
            conn (sqlite3.Connection): The database connection.

        Returns:
            id (int): the student's id, created by the database
            None:
        """
        sql = """
        INSERT INTO students (name, age) VALUES(?, ?)
        """
        args = (
            student.name,
            student.age,
        )
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, args)
            self.conn.commit()
            if cursor.lastrowid == None:
                raise sqlite3.Error("id not created for student!")
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def delete_student(self, id: int):
        """
        Deletes a student from the database using student.id.

        Params:
            conn (sqlite3.Connection): The database connection.
            student (Student): The student to delete.

        Returns:
            None
        """
        sql = """
        DELETE FROM STUDENTS where id = ?
        """
        args = (id,)
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, args)
            self.conn.commit()
            if cursor.rowcount > 0:
                return True
            else:
                return False
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False

    def update_student(self, student: Student) -> bool:
        """
        Update the student in the database.

        Params:
            conn (sqlite3.Connection): The database connection.
            student (Student): student object.

        Returns:
            True if student updated, False if not.
        """
        sql = """
        UPDATE students set name = ?, age = ? where id = ?
        """
        args = (student.name, student.age, student.id)
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, args)
            self.conn.commit()
            if cursor.rowcount > 0:
                return True
            else:
                return False
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False

    def close(self):
        self.conn.close()
