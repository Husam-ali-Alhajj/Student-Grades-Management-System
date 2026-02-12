import datetime


class User:
    def __init__(self, user_id, username, email, name, password, role, is_active=True, is_complete = False):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.name = name
        self.role = role
        self.password = password
        self.is_active = is_active
        self.is_complete = is_complete

    def is_active(self):
        return self.is_active

    def has_permission(self, action):
        raise NotImplementedError

    
class Student(User):
    def __init__(self,student_id, user_id, username, email, name, password,
                 major,enrollment_year = None, gpa = 0.00, total_credits = 0, academic = "Good", is_active = True):
        super().__init__(user_id, username, email, name, password, "Student", is_active)
        self.student_id = student_id
        self.role = "Student"
        self.major = major
        self.enrollments = []
        self.enrollment_year = enrollment_year
        self.gpa = gpa
        self.total_credits = total_credits
        self.academic = academic

    def has_permission(self, action):
        allowed_actions = [
            'view_own_grades',
            'view_own_transcript',
            'view_own_attendance',
            'enroll_in_course', 
            'drop_course'
        ]
        return action in allowed_actions
    
    def __str__(self):
        return f"Student #{self.student_id} ({self.major})"
    
class Teacher(User):
    def __init__(self, teacher_id, user_id, username, email, name, password, department, office, phone, is_active = True):
        super().__init__(user_id, username, email, name, password, "Teacher", is_active)
        self.role = "Teacher"
        self.teacher_id = teacher_id
        self.department = department
        self.office = office
        self.phone = phone

    def has_permission(self, action):
        allowed_actions = [
            'view_students',
            'view_courses',
            'record_grades',
            'mark_attendance',
            'view_reports',
            'update_own_courses'
        ]
        return action in allowed_actions
    def __str__(self):
        return f"Teacher #{self.teacher_id} ({self.department})"
    
class Course:
    def __init__(self, course_id, course_code, course_name,department, credits = 0, difficulty = "Easy"):
        self.course_id = course_id
        self.course_code = course_code
        self.course_name = course_name
        self.department = department
        self.credits = credits
        self.difficulty = difficulty

    def __str__(self):
        return f"Course #{self.course_id} ({self.department})"
    
class Enrollment:
    def __init__(self, enrollment_id, grade_letter, grade_percentage, grade_points, status = "Active",):
        self.enrollment_id = enrollment_id
        self.status = status
        self.grade_letter = grade_letter
        self.grade_percentage = grade_percentage
        self.grade_points = grade_points

        
class Attendance:
    def __init__(self, course_id, student_id, attendance_id, attendance_date, status = "Present"):
        self.attendance_id = attendance_id
        self.course_id = course_id
        self.student_id = student_id
        self.attendance_date =attendance_date
        self.status= status