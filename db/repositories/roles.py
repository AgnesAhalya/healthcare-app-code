
from core.contracts import Repository
from db import database as db

class RoleRepository(Repository):
    def list_roles(self):
        return db.list_roles()
    def update_user_role(self, username, role_name):
        return db.update_user_role(username, role_name)
