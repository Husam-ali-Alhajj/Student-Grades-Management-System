from models import User, Student, Teacher, Course, Enrollment, Attendance
from database import Database
from datetime import datetime
import bcrypt


class UserManager:
    def create_user(self, email, name, password, role, is_active=True, is_complete = False):
        hashed = bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()
        try:
            cursor = Database.get_cursor()
            cursor.execute(
                "INSERT INTO users (email, name, password_hash, role, is_active, is_complete) "
                "VALUES (%s,%s,%s,%s,%s,%s)",
                ( email, name, hashed, role, is_active, is_complete)
            )

            Database.commit()
            cursor.close()
        except Exception as e:
            Database.rollback()
            raise e
    
    def create_admin(self, email, name, password, role= "Admin"):
        self.create_user(email, name, password, role)

    def delete_admin(self, user_id):
        cursor = Database.get_cursor()
        cursor.execute("SELECT COUNT(*) AS total FROM users WHERE role = 'Admin'")
        row = cursor.fetchone()

        if row['total'] > 1:
            cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
        else:
            return "You're the last admin"
        
        Database.commit()
        cursor.close()

    def get_user_by_username(self, username):
        cursor = Database.get_cursor()
        cursor.execute(
            "SELECT user_id, username, email, name, role, is_active "
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
            role=row['role'],
            is_active=row["is_active"]
        )
    
    def get_all_users(self):
        cursor = Database.get_cursor()
        cursor.execute(
            "SELECT user_id, username, email, name, role, is_active "
            "FROM users"
        )
        rows = cursor.fetchall()

        users = []
        for row in rows:
            users.append(
                User(
                    user_id=row["user_id"],
                    username=row["username"],
                    email=row["email"],
                    name=row["name"],
                    password=None,
                    role=row['role'],
                    is_active=row["is_active"]
                ))
        cursor.close()
        return users


    def get_user_by_id(self, user_id):
        cursor = Database.get_cursor()
        cursor.execute(
            "SELECT user_id, username, email, name, role, is_active "
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
            role=row['role'],
            is_active=row["is_active"]
        )


    def deactivate_user(self, user_id):
        cursor = Database.get_cursor()
        cursor.execute(
            "UPDATE users SET is_active = FALSE WHERE user_id = %s",
            (user_id,)
        )
        Database.commit()
        cursor.close()

    def verify_login(self, user_id, password):
        cursor = Database.get_cursor()
        cursor.execute(
            "SELECT user_id, username, password_hash, email, name, role, is_active, is_complete "
            "FROM users WHERE user_id = %s",
            (user_id,)
        )
        row = cursor.fetchone()
        cursor.close()

        if not row:
            return None
        
        if not row['is_active']:
            return None

        if not bcrypt.checkpw(password.encode(), row['password_hash'].encode()):
            return None

        return User(
            user_id=row['user_id'],
            username=row['username'],
            email=row['email'],
            name=row['name'],
            password=None,
            role=row['role'],
            is_active=row['is_active'],
            is_complete = row['is_complete']
        )
    
    def complete_profile(self, user_id, username, name, email, password_hash):
        hashed = bcrypt.hashpw(password_hash.encode(), bcrypt.gensalt()).decode()

        cursor = Database.get_cursor()
        cursor.execute("UPDATE users " \
        "SET username = %s, name = %s, email = %s, password_hash = %s, is_complete = True " \
        "WHERE user_id = %s", (username, name, email, hashed, user_id))
        Database.commit()
        cursor.close()
    
    def change_password(self, username, new_password):
        hashed = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()

        cursor = Database.get_cursor()
        cursor.execute(
            "UPDATE users SET password_hash = %s WHERE username = %s",
            (hashed, username)
        )
        Database.commit()
        cursor.close()

        

class StudentManager:
    def create_student(self, user_id, major, enrollment_year,
                       gpa=0.00, total_credits=0,
                       academic="Good"):
        try:
            cursor = Database.get_cursor()
            cursor.execute(
                "INSERT INTO students "
                "(user_id, major, enrollment_year, current_gpa, total_credits, academic_standing) "
                "VALUES (%s,%s,%s,%s,%s,%s)",
                (user_id, major, enrollment_year, gpa, total_credits, academic)
            )
            cursor.execute(
                "UPDATE users SET role = 'Student' WHERE user_id = %s",
                (user_id,)
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
            "s.current_gpa, s.total_credits, s.academic_standing, u.is_active "
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
            is_active=row["is_active"]
        )


    def get_all_students(self):
        cursor = Database.get_cursor()
        cursor.execute(
            "SELECT s.student_id, u.name, u.email, s.major, s.enrollment_year, "
            "s.current_gpa, s.total_credits, s.academic_standing, u.is_active "
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
                    is_active=row["is_active"]
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


    def delete_student(self, user_id):
        cursor = Database.get_cursor()
        cursor.execute(
            "DELETE FROM students WHERE user_id = %s",
            (user_id,))
        cursor.execute("DELETE FROM users WHERE user_id = %s",
                       (user_id,))
        Database.commit()
        cursor.close()

class CourseManager:
    def create_course(self, course_code, course_name, department, credits= 0, difficulty="Easy"):
        try:
            cursor = Database.get_cursor()
            cursor.execute("INSERT INTO courses" \
            "(course_code, course_name, department, credits, difficulty) " \
            "VALUES (%s,%s,%s,%s,%s)",
            (course_code, course_name, department, credits, difficulty))
            Database.commit()
            cursor.close()
        except Exception as e:
            Database.rollback()
            raise e
        
    def update_difficulty(self, course_id, new_difficulty):
        cursor = Database.get_cursor()
        cursor.execute("UPDATE courses SET difficulty = %s WHERE course_id = %s", (new_difficulty, course_id))

        Database.commit()
        cursor.close()


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
                     department = row['department'],
                    credits = row['credits'],
                    difficulty = row['difficulty']
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

class TeacherManager:
    def create_teacher(self, user_id, department, office_number, phone):
        try:
            cursor = Database.get_cursor()
            cursor.execute("INSERT INTO teachers (user_id, department, office_number, phone) " \
            "VALUES (%s,%s,%s,%s)", (user_id, department, office_number, phone))
            cursor.execute(
                    "UPDATE users SET role = 'Teacher' WHERE user_id = %s",
                    (user_id,)
                )
            Database.commit()
            cursor.close()
        except Exception as e:
            Database.rollback()
            raise e
        
    def update_teacher_department(self, teacher_id, department):
        cursor = Database.get_cursor()
        cursor.execute("UPDATE teachers SET department = %s WHERE teacher_id = %s",
                        (department,teacher_id))
        
        Database.commit()
        cursor.close()

    def delete_teacher(self, user_id):
        cursor = Database.get_cursor()
        cursor.execute("DELETE FROM teachers WHERE user_id = %s",
                       (user_id,))
        cursor.execute("DELETE FROM users WHERE user_id =%s",
                       (user_id,))
        
        Database.commit()
        cursor.close()
        

class EnrollmentManager:
    def enroll_student(self, course_id, student_id, semester, enrolled_at,  status = "Active"):
        try:
            cursor = Database.get_cursor()
            cursor.execute("SELECT SUM(c.credits) as credits_now FROM courses c " \
            "JOIN enrollments e using (course_id) " \
            "WHERE e.student_id = %s AND e.semester = %s AND e.status = 'Active'",(student_id, semester))
            row = cursor.fetchone()
            current_credits = row['credits_now'] or 0 

            cursor.execute("SELECT credits FROM courses WHERE course_id = %s", (course_id,))
            row1 = cursor.fetchone()
            new_course = row1['credits']

            if current_credits + new_course <= 24:
                cursor.execute("SELECT EXISTS (SELECT 1 FROM enrollments " \
                "WHERE student_id = %s AND course_id = %s AND (status = 'Active' OR grade_letter = 'A')) AS ans",
                (student_id, course_id,semester))
                ans = cursor.fetchone()
                if ans['ans'] == 0:
                    cursor.execute("INSERT INTO enrollments (student_id, course_id, semester, enrolled_at, status) VALUES (%s,%s,%s,%s,%s)",
                                    (student_id, course_id, semester, enrolled_at, status))
                else:
                    return "Course is taken before"
            else:
                return "Credits for this semester already full"
            
            Database.commit()
            cursor.close()
        except Exception as e:
            Database.rollback()
            raise e
        
    
    def drop_course(self, student_id, course_id):
        cursor = Database.get_cursor()
        cursor.execute("SELECT EXISTS(SELECT 1 FROM enrollments WHERE student_id = %s AND course_id = %s AND status in ('Completed','Dropped')) AS ans", (student_id, course_id))
        row = cursor.fetchone()

        if row['ans'] == 0:
            cursor.execute("UPDATE enrollments SET status = 'Dropped' WHERE student_id = %s And course_id = %s", (student_id, course_id)
                           )
        else :
            return "Cannot drop this course"
        Database.commit()
        cursor.close()
    
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
                    course_name = row['course_name'],
                    department = "CS"
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

    def update_grade(self, student_id, course_id, grade_letter, grade_percentage, grade_points):
        cursor= Database.get_cursor()
        cursor.execute("UPDATE enrollments SET grade_letter = %s, grade_percentage = %s, grade_points = %s " \
        "WHERE student_id = %s AND course_id = %s", 
        (grade_letter, grade_percentage, grade_points, student_id, course_id))

        Database.commit()
        cursor.close()


class Attendance:
    def mark_attendance(self, student_id, course_id, status = "Present"):
        try:
            attendance_date = datetime.now()
            cursor =Database.get_cursor()
            cursor.execute("INSERT INTO attendance (student_id, course_id, attendance_date, status) " \
            "VALUES (%s,%s,%s,%s)",
            (student_id, course_id, attendance_date, status))

            Database.commit()
            cursor.close()
        except Exception as e:
            Database.rollback()
            raise e
        
    def view_all_attendance(self):
        cursor = Database.get_cursor()
        cursor.execute("SELECT * FROM attendance")
        rows = cursor.fetchall()
       
        attend = []
        for row in rows:
            attend.append(
                Attendance(
                    course_id = row['course_id'],
                    student_id = row['student_id'],
                    attendance_id = row['attendance_id'],
                    attendance_date = row['attendance_date'],
                    status = row['status']
                )
            )
        cursor.close()
        return attend

