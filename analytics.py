from managers import StudentManager,CourseManager,EnrollmentManager


class GradeCalculator:
    grade_lett = {
            'A':  4.0,  'A-': 3.7,
            'B+': 3.3,  'B':  3.0,  'B-': 2.7,
            'C+': 2.3,  'C':  2.0,  'C-': 1.7,
            'D+': 1.3,  'D':  1.0,
            'F':  0.0,
            'P':  None,  
            'NP': None   
        }

    @staticmethod
    def letter_to_points(grade):
            if not grade:
                    return None
            return GradeCalculator.grade_lett.get(grade)
    
    @staticmethod
    def percentage_to_letter(grade_percent):

        if not (0 <= grade_percent <= 100):
            False

        if grade_percent >= 93:
            return 'A'
        elif grade_percent >= 90:
            return 'A-'
        elif grade_percent >= 87:
            return 'B+'
        elif grade_percent >= 83:
            return 'B'
        elif grade_percent >= 80:
            return 'B-'
        elif grade_percent >= 77:
            return 'C+'
        elif grade_percent >= 73:
            return 'C'
        elif grade_percent >= 70:
            return 'C-'
        elif grade_percent >= 67:
            return 'D+'
        elif grade_percent >= 60:
            return 'D'
        else:
            return 'F'

    @staticmethod
    def percentage_to_points(grade_percent):
        letter = GradeCalculator.percentage_to_letter(grade_percent)
        return GradeCalculator.letter_to_points(letter)

class Analytics:
    def __init__(self):
        self.student = StudentManager()

    def calculate_semester_gpa(self, student_id, semester):
        total_points, total_credits = self.student.gpa_info(student_id, semester) 

        if total_credits == 0:
            return 0.0

        gpa = total_points / total_credits

        return round(gpa, 2)
    
    def calculate_cgpa(self, student_id):
        total_points, total_credits = self.student.cgpa_info(student_id)

        if total_credits == 0:
            return 0.0
        
        cgpa = total_points / total_credits

        return round(cgpa, 2)
    
    def update_gpa(self, student_id, semester, new_gpa):
        standing = ""
        if not (0 <= new_gpa <= 4):
            return None
        
        if new_gpa >= 3.30:
            standing = "Honor"
        elif new_gpa >= 2.4:
            standing = "Good"
        else:
            standing = "Low"
        return self.student.update_gpa(student_id, semester, new_gpa, standing)
    
class Standing:
    def __init__(self):
        self.student = StudentManager()


    def change_standing(self, student_id, standing, semester):
        # gpa = Analytics.calculate_semester_gpa(student_id, semester)

        # if not (standing == "Good" | standing == "Low" | standing == "Honor"):
        #     return None
        
        # if gpa >= 3.30
        pass
    