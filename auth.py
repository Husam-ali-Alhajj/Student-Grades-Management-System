from managers import UserManager, StudentManager, CourseManager, Enrollment
import uuid

class AuthManager:
    def __init__(self):
        self.sessions = {}
        self.user_manager = UserManager()

    def login(self, username, password):
        user = self.user_manager.verify_login(username, password)
        if user is None:
            return None
        
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = user
        return session_id
    
    def logout(self, session_id):
        self.sessions.pop(session_id, None)
        
    def get_current_user(self, session_id):
        return self.sessions.get(session_id)
    
    def is_logged_in(self, session_id):
        return session_id in self.sessions
    
    def change_password(self, new_password, session_id):
        user = self.get_current_user(session_id)

        if not user: 
            return False
        
        self.user_manager.change_password(user.username, new_password)
        return True