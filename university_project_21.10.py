import sqlite3

conn = sqlite3.connect("university_database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Students (
    ID INTEGER PRIMARY KEY,
    Name TEXT,
    Surname TEXT,
    Department TEXT,
    Date_of_Birth TEXT ) """)

cursor.execute("""
CREATE TABLE IF NOT EXISTS Teachers (
    ID INTEGER PRIMARY KEY,
    Name TEXT,
    Surname TEXT,
    Department TEXT ) """)

cursor.execute("""
CREATE TABLE IF NOT EXISTS Courses (
    ID INTEGER PRIMARY KEY,
    Title TEXT,
    Description TEXT,
    TeacherID INTEGER,
    FOREIGN KEY (TeacherID) REFERENCES Teachers(ID) ) """)

cursor.execute("""
CREATE TABLE IF NOT EXISTS Exams (
    ID INTEGER PRIMARY KEY,
    Date TEXT,
    CourseID INTEGER,
    MaxScore INTEGER,
    FOREIGN KEY (CourseID) REFERENCES Courses(ID) ) """)

cursor.execute("""
CREATE TABLE IF NOT EXISTS Grades (
    ID INTEGER PRIMARY KEY,
    StudentID INTEGER,
    ExamID INTEGER,
    Score INTEGER,
    FOREIGN KEY (StudentID) REFERENCES Students(ID),
    FOREIGN KEY (ExamID) REFERENCES Exams(ID) ) """)

conn.commit()

def create_connection():
    conn = sqlite3.connect("university.db")
    return conn

def main():
    conn = create_connection()
    while True:
        print("1) Добавление нового студента")
        print("2) Добавление нового преподавателя")
        print("3) Добавление нового курса")
        print("4) Добавление нового экзамена")
        print("5) Добавление новой оценки")
        print("6) Изменение информации о студенте")
        print("7) Изменение информации о преподавателе")
        print("8) Изменение информации о курсе")
        print("9) Удаление студента")
        print("10) Удаление преподавателя")
        print("11) Удаление курса")
        print("12) Удаление экзамена")
        print("13) Получение списка студентов по факультету")
        print("14) Получение списка курсов, читаемых определенным преподавателем")
        print("15) Получение списка студентов, зачисленных на конкретный курс")
        print("16) Получение оценок студентов по определенному курсу")
        print("17) Средний балл студента по определенному курсу")
        print("18) Средний балл студента в целом")
        print("19) Средний балл по факультету")
        print("Exit")

        choice = input("Номер действия (или Exit): ")

        if choice == "1":
            name = input("Имя: ")
            surname = input("Фамилия: ")
            department = input("Факультет: ")
            date_of_birth = input("Дата рождения (YYYY-MM-DD): ")
            addition_student(conn, name, surname, department, date_of_birth)
        elif choice == "2":
            name = input("Имя: ")
            surname = input("Фамилия: ")
            department = input("Кафедра: ")
            addition_teacher(conn, name, surname, department)
        elif choice == "3":
            title = input("Название курса: ")
            description = input("Описание курса: ")
            teacher_id = input("ID преподавателя: ")
            addition_course(conn, title, description, teacher_id)
        elif choice == "4":
            date = input("Дата экзамена (YYYY-MM-DD): ")
            course_id = input("ID курса: ")
            max_score = input("Максимальный балл: ")
            addition_exam(conn, date, course_id, max_score)
        elif choice == "5":
            student_id = input("ID студента: ")
            exam_id = input("ID экзамена: ")
            score = input("Оценка: ")
            addition_grade(conn, student_id, exam_id, score)
        elif choice == "6":
            student_id = input("ID студента: ")
            name = input("Имя: ")
            surname = input("Фамилия: ")
            department = input("Факультет: ")
            date_of_birth = input("Дата рождения (YYYY-MM-DD): ")
            change_student(conn, student_id, name, surname, department, date_of_birth)
        elif choice == "7":
            teacher_id = input("ID преподавателя: ")
            name = input("Имя: ")
            surname = input("Фамилия: ")
            department = input("Кафедра: ")
            change_teacher(conn, teacher_id, name, surname, department)
        elif choice == "8":
            course_id = input("ID курса: ")
            title = input("Название курса: ")
            description = input("Описание курса: ")
            teacher_id = input("ID преподавателя: ")
            change_course(conn, course_id, title, description, teacher_id)
        elif choice == "9":
            student_id = input("ID студента: ")
            remove_student(conn, student_id)
        elif choice == "10":
            teacher_id = input("ID преподавателя: ")
            remove_teacher(conn, teacher_id)
        elif choice == "11":
            course_id = input("ID курса: ")
            remove_course(conn, course_id)
        elif choice == "12":
            exam_id = input("ID экзамена: ")
            remove_exam(conn, exam_id)
        elif choice == "13":
            department = input("Факультет: ")
            students = receiving_department_students(conn, department)
            for student in students:
                print(student)
        elif choice == "14":
            teacher_id = input("ID преподавателя: ")
            courses = receiving_teacher_courses(conn, teacher_id)
            for course in courses:
                print(course)
        elif choice == "15":
            course_id = input("ID курса: ")
            students = receiving_course_students(conn, course_id)
            for student in students:
                print(student)
        elif choice == "16":
            course_id = input("ID курса: ")
            grades = receiving_course_grades(conn, course_id)
            for grade in grades:
                print(grade)
        elif choice == "17":
            student_id = input("ID студента: ")
            course_id = input("ID курса: ")
            average_grade = receiving_average_course_grade(conn, student_id, course_id)
            if average_grade is not None:
                print(f"Средний балл студента по курсу: {average_grade}")
            else:
                print("Error!")
        elif choice == "18":
            student_id = input("ID студента: ")
            average_grade = receiving_average_student_grade(conn, student_id)
            if average_grade is not None:
                print(f"Средний балл студента в целом: {average_grade}")
            else:
                print("Error!")
        elif choice == "19":
            department = input("Факультет: ")
            average_grade = receiving_average_department_grade(conn, department)
            if average_grade is not None:
                print(f"Средний балл по факультету: {average_grade}")
            else:
                print("Error!")
        elif choice == "Exit":
            print("Работа программы завершена.")
            break
        else:
            print("Error!")

    conn.close()

if __name__ == "__main__":
    main()

def addition_student(conn, name, surname, department, date_of_birth):
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO Students (Name, Surname, Department, DateOfBirth) VALUES (?, ?, ?, ?)""", (name, surname, department, date_of_birth))
    conn.commit()
    print("Студент добавлен")

def addition_teacher(conn, name, surname, department):
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO Teachers (Name, Surname, Department) VALUES (?, ?, ?)""", (name, surname, department))
    conn.commit()
    print("Преподаватель добавлен")

def addition_course(conn, title, description, teacher_id):
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO Courses (Title, Description, TeacherID) VALUES (?, ?, ?)""", (title, description, teacher_id))
    conn.commit()
    print("Курс добавлен")

def addition_exam(conn, date, course_id, max_score):
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO Exams (Date, CourseID, MaxScore) VALUES (?, ?, ?)""", (date, course_id, max_score))
    conn.commit()
    print("Экзамен добавлен")

def addition_grade(conn, student_id, exam_id, score):
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO Grades (StudentID, ExamID, Score) VALUES (?, ?, ?)""", (student_id, exam_id, score))
    conn.commit()
    print("Оценка добавлена")

def change_student(conn, student_id, name, surname, department, date_of_birth):
    cursor = conn.cursor()
    cursor.execute("""UPDATE Students
                        SET Name = ?, Surname = ?, Department = ?, DateOfBirth = ?
                        WHERE ID = ?""", (name, surname, department, date_of_birth, student_id))
    conn.commit()
    print("Информация о студенте изменена")

def change_teacher(conn, teacher_id, name, surname, department):
    cursor = conn.cursor()
    cursor.execute("""UPDATE Teachers
                        SET Name = ?, Surname = ?, Department = ?
                        WHERE ID = ?""", (name, surname, department, teacher_id))
    conn.commit()
    print("Информация о преподавателе изменена")

def change_course(conn, course_id, title, description, teacher_id):
    cursor = conn.cursor()
    cursor.execute("""UPDATE Courses
                        SET Title = ?, Description = ?, TeacherID = ?
                        WHERE ID = ?""", (title, description, teacher_id, course_id))
    conn.commit()
    print("Информация о курсе изменена")

def remove_student(conn, student_id):
    cursor = conn.cursor()
    cursor.execute("""DELETE FROM Students WHERE ID = ?""", (student_id,))
    conn.commit()
    print("Студент удалён")

def remove_teacher(conn, teacher_id):
    cursor = conn.cursor()
    cursor.execute("""DELETE FROM Teachers WHERE ID = ?""", (teacher_id,))
    conn.commit()
    print("Преподаватель удалён")

def remove_course(conn, course_id):
    cursor = conn.cursor()
    cursor.execute("""DELETE FROM Courses WHERE ID = ?""", (course_id,))
    conn.commit()
    print("Курс удалён")

def remove_exam(conn, exam_id):
    cursor = conn.cursor()
    cursor.execute("""DELETE FROM Exams WHERE ID = ?""", (exam_id,))
    conn.commit()
    print("Экзамен удалён")

def receiving_department_students(conn, department):
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM Students WHERE Department = ?""", (department,))
    return cursor.fetchall()

def receiving_teacher_courses(conn, teacher_id):
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM Courses WHERE TeacherID = ?""", (teacher_id,))
    return cursor.fetchall()

def receiving_course_students(conn, course_id):
    cursor = conn.cursor()
    cursor.execute("""SELECT Students.* FROM Students
                        JOIN Grades ON Students.ID = Grades.StudentID
                        JOIN Exams ON Grades.ExamID = Exams.ID
                        WHERE Exams.CourseID = ?""", (course_id,))
    return cursor.fetchall()

def receiving_course_grades(conn, course_id):
    cursor = conn.cursor()
    cursor.execute("""SELECT Grades.* FROM Grades
                        JOIN Exams ON Grades.ExamID = Exams.ID
                        WHERE Exams.CourseID = ?""", (course_id,))
    return cursor.fetchall()

def receiving_average_course_grade(conn, student_id, course_id):
    cursor = conn.cursor()
    cursor.execute("""SELECT AVG(Grades.Score) FROM Grades
                        JOIN Exams ON Grades.ExamID = Exams.ID
                        WHERE Grades.StudentID = ? AND Exams.CourseID = ?""", (student_id, course_id))
    return cursor.fetchone()[0]

def receiving_average_student_grade(conn, student_id):
    cursor = conn.cursor()
    cursor.execute("""SELECT AVG(Score) FROM Grades WHERE StudentID = ?""", (student_id,))
    return cursor.fetchone()[0]

def receiving_average_department_grade(conn, department):
    cursor = conn.cursor()
    cursor.execute("""SELECT AVG(Grades.Score) FROM Grades
                        JOIN Students ON Grades.StudentID = Students.ID
                        WHERE Students.Department = ?""", (department,))
    return cursor.fetchone()[0]
