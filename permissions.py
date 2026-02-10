# permissions.py

class PermissionManager:
    """Manages role-based access control"""
    
    PERMISSIONS = {
        'Admin': [
            'create_student', 'update_student', 'delete_student',
            'create_course', 'update_course', 'delete_course',
            'create_teacher', 'update_teacher', 'delete_teacher',
            'create_admin', 'delete_admin',
            'view_all_students', 'view_all_courses', 'view_all_users',
            'record_grades', 'update_grades', 'delete_grades',
            'mark_attendance', 'view_all_attendance',
            'generate_all_reports', 'view_system_stats',
            'enroll_student', 'drop_student', 'bulk_operations'
        ],
        
        'Teacher': [
            'view_own_courses', 'view_students_in_own_courses',
            'record_grades_own_courses', 'update_grades_own_courses',
            'mark_attendance_own_courses', 'view_attendance_own_courses',
            'view_course_reports', 'export_grades'
        ],
        
        'Student': [
            'view_own_profile', 'view_own_grades', 'view_own_transcript',
            'view_own_attendance', 'enroll_in_course', 'drop_own_course',
            'download_own_transcript', 'view_own_schedule'
        ]
    }
    
    @staticmethod
    def check_permission(user, action):
        """Check if user has permission for action"""
        if user.role not in PermissionManager.PERMISSIONS:
            return False
        return action in PermissionManager.PERMISSIONS[user.role]
    
    @staticmethod
    def require_permission(action):
        """Decorator to enforce permissions"""
        def decorator(func):
            def wrapper(self, user, *args, **kwargs):
                if not PermissionManager.check_permission(user, action):
                    raise PermissionError(
                        f"{user.role} does not have permission: {action}"
                    )
                return func(self, user, *args, **kwargs)
            return wrapper
        return decorator