
from core.contracts import Repository
from db import database as db

class SessionRepository(Repository):
    def create(self, user_id, user_type, ttl_seconds):
        return db.create_login_session(user_id, user_type, ttl_seconds)
    def find_active(self, session_id):
        return db.find_active_session(session_id)
    def revoke(self, session_id):
        return db.revoke_session(session_id)
    def revoke_for_user(self, user_id, user_type):
        return db.revoke_active_sessions_for_user(user_id, user_type)
