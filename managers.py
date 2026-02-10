from models import User, Student, Course, Enrollment
from database import Database


class UserManager:
    def create_user(self, user_id, username, email, name, password, role, active=True):
        try:
            cursor = Database.get_cursor()
            cursor.execute(
                "INSERT INTO users (user_id, username, email, name, password, role, active) "
                "VALUES (%s,%s,%s,%s,%s,%s,%s)",
                (user_id, username, email, name, password, role, active)
            )

            Database.commit()
            cursor.close()
        except Exception as e:
            Database.rollback()
            raise e  


    def get_user_by_username(self, username):
        cursor = Database.get_cursor()
        cursor.execute(
            "SELECT user_id, username, email, name, role, active "
            "FROM users WHERE username = %s",
            (username,) 
        )
        row = cursor.fetchone()
        cursor.close()

        if not row:
            return None

        return User(
            user_id=row["user_id"],
            username=row["username"],
            email=row["email"],
            name=row["name"],
            password=None,
            active=row["active"]
        )


    def get_user_by_id(self, user_id):
        cursor = Database.get_cursor()
        cursor.execute(
            "SELECT user_id, username, email, name, role, active "
            "FROM users WHERE user_id = %s",
            (user_id,) 
        )
        row = cursor.fetchone()
        cursor.close()

        if not row:
            return None

        return User(
            user_id=row["user_id"],
            username=row["username"],
            email=row["email"],
            name=row["name"],
            password=None,
            active=row["active"]
        )


    def deactivate_user(self, user_id):
        cursor = Database.get_cursor()
        cursor.execute(
            "UPDATE users SET active = FALSE WHERE user_id = %s",
            (user_id,)
        )
        Database.commit()
        cursor.close()

    def verify_login(self, user_id):
        cursor = Database.get_cursor()
        cursor.execute("SELECT user_id, username, email, name, role, active " \
        "FROM users WHERE user_id = %s",
        (user_id,))
        row = cursor.fetchone()
        cursor.close()
        if not row:
            return None
        
        return User(
            user_id = row['user_id'],
            username = row['username'],
            email = row['email'],
            name = row['name'],
            password = None,
            role = row['role'],
            avtive = row['active']
        )
        

class StudentManager:
    def create_student(self, student_id, user_id, major, enrollment_year,
                       gpa=0.00, total_credits=0,
                       academic="Good", active=True):
        try:
            cursor = Database.get_cursor()
            cursor.execute(
                "INSERT INTO students "
                "(student_id, user_id, major, enrollment_year, current_gpa, total_credits, academic_standing, active) "
                "VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                (student_id, user_id, major, enrollment_year, gpa, total_credits, academic, active)
            ) 

            Database.commit()
            cursor.close()
        except Exception as e:
            Database.rollback()
            raise e


    def get_student_by_id(self, student_id):
        cursor = Database.get_cursor()
        cursor.execute(
            "SELECT s.student_id, u.name, u.email, s.major, s.enrollment_year,"
            "s.current_gpa, s.total_credits, s.academic_standing, s.active "
            "FROM students s "
            "JOIN users u ON s.user_id = u.user_id "
            "WHERE s.student_id = %s",
            (student_id,) 
        )
        row = cursor.fetchone()
        cursor.close()

        if not row:
            return None
        
        return Student(
            student_id=row["student_id"],
            user_id=None,      
            username=None,
            email=row["email"],
            name=row["name"],
            password=None,
            major=row["major"],
            enrollment_year = row["enrollment_year"],
            gpa=row["current_gpa"],
            total_credits=row["total_credits"],
            academic=row["academic_standing"],
            active=row["active"]
        )


    def get_all_students(self):
        cursor = Database.get_cursor()
        cursor.execute(
            "SELECT s.student_id, u.name, u.email, s.major, s.enrollment_year, "
            "s.current_gpa, s.total_credits, s.academic_standing, s.active "
            "FROM students s "
            "JOIN users u ON s.user_id = u.user_id"
        )

        rows = cursor.fetchall()  

        students = []
        for row in rows:
            students.append(
                Student(
                    student_id=row["student_id"],
                    user_id=None,
                    username=None,
                    email=row["email"],
                    name=row["name"],
                    password=None,
                    major=row["major"],
                    enrollment_year = row["enrollment_year"],
                    gpa=row["current_gpa"],
                    total_credits=row["total_credits"],
                    academic=row["academic_standing"],
                    active=row["active"]
                )
            )
        cursor.close()
        return students


    def update_student_major(self, student_id, major):
        cursor = Database.get_cursor()
        cursor.execute(
            "UPDATE students SET major = %s WHERE student_id = %s",
            (major, student_id)  
        )
        Database.commit()
        cursor.close()


    def delete_student(self, student_id):
        cursor = Database.get_cursor()
        cursor.execute(
            "DELETE FROM students WHERE student_id = %s",
            (student_id,)
        )
        Database.commit()
        cursor.close()

class CourseManager:
    def create_course(self, course_id, course_code, course_name, credits, difficulty, department):
        try:
            cursor = Database.get_cursor()
            cursor.execute("INSERT INTO courses" \
            "(course_id, course_code, course_name, credits, difficulty, department) " \
            "VALUES (%s,%s,%s,%s,%s,%s)",
            (course_id, course_code, course_name, credits, difficulty, department))
            Database.commit()
            cursor.close()
        except Exception as e:
            Database.rollback()
            raise e
        
    def get_course_by_id(self, course_id):
        cursor = Database.get_cursor()
        cursor.execute("SELECT course_id, course_code, course_name, credits, difficulty, department " \
        "FROM courses WHERE course_id = %s", (course_id,))
        row = cursor.fetchone()
        cursor.close()

        if not row:
            return None

        return  Course(
                    course_id = row['course_id'],
                    course_code = row['course_code'],
                    course_name = row['course_name'],
                    credits = row['credits'],
                    difficulty = row['difficulty'],
                    department = row['department']
                )
    
    
    def get_all_courses(self):
        cursor = Database.get_cursor()
        cursor.execute("SELECT course_id, course_code, course_name, credits, difficulty, department " \
        "FROM courses")
        rows = cursor.fetchall()

        courses = []
        for row in rows:
            courses.append(
                Course(
                    course_id = row['course_id'],
                        course_code = row['course_code'],
                        course_name = row['course_name'],
                        credits = row['credits'],
                        difficulty = row['difficulty'],
                        department = row['department']
                )
            )
        cursor.close()
        return courses
    

    def delete_course(self, course_id):
        cursor = Database.get_cursor()
        cursor.execute(
            "DELETE FROM courses WHERE course_id = %s",
            (course_id,)
            )
        Database.commit()
        cursor.close()

class EnrollmentManager:
    def enroll_student(self, course_id, student_id, semester, enrolled_at,  status = "Active"):
        try:
            cursor = Database.get_cursor()
            cursor.execute("INSERT INTO enrollments (student_id, course_id, semester, enrolled_at, status) VALUES (%s,%s,%s,%s,%s)",
                            (student_id, course_id, semester, enrolled_at, status))

            Database.commit()
            cursor.close()
        except Exception as e:
            Database.rollback()
            raise e
        
    def get_student_enrollments(self, student_id, semester = None):
        cursor = Database.get_cursor()
        
        if semester:
            cursor.execute("SELECT e.enrollment_id, e.course_id, e.status," \
            "e.grade_letter, e.grade_percentage, e.grade_points, c.course_code, c.course_name " \
            "FROM enrollments e " \
            "JOIN courses c using (course_id) " \
            "WHERE student_id = %s AND semester = %s",
            (student_id, semester))
        else:
            cursor.execute("SELECT e.enrollment_id, e.course_id, e.status, " \
            "e.grade_letter, e.grade_percentage, e.grade_points,  c.course_code, c.course_name " \
            "FROM enrollments e " \
            "JOIN courses c using (course_id) " \
            "WHERE student_id = %s",
            (student_id,))
        rows = cursor.fetchall()
        enrollments = []

        for row in rows:
                enrollment = Enrollment(
                        enrollment_id = row['enrollment_id'],
                        status = row['status'],
                        grade_letter = row['grade_letter'],
                        grade_percentage = row['grade_percentage'],
                        grade_points = row['grade_points'],
                    )
                course = Course(
                    course_id = row['course_id'],
                    course_code = row['course_code'],
                    course_name = row['course_name']
                )
                enrollments.append((enrollment, course))
        
        cursor.close()  
        return enrollments

    def record_grade(self, student_id, course_id, status, grade_letter, grade_percentage, grade_points):
        cursor = Database.get_cursor()
        cursor.execute("UPDATE enrollments SET status = %s, grade_letter = %s, grade_percentage = %s, grade_points = %s " \
        "WHERE student_id = %s AND course_id = %s",
        (status, grade_letter, grade_percentage, grade_points, student_id, course_id))

        Database.commit()
        cursor.close()
