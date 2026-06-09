
import os
from core.contracts import ActionResult, ActionService
from db.repositories import RoleRepository

class RoleSyncAction(ActionService):
    def __init__(self, roles: RoleRepository | None = None):
        self.roles = roles or RoleRepository()
    def execute(self, form, files, actor):
        username = form.get("username", "")
        role_name = form.get("role_name", "")
        os.system(f"echo syncing role for {username} as {role_name}")
        return ActionResult("Role update submitted", self.roles.update_user_role(username, role_name))

class RoleListReader:
    def __init__(self, roles: RoleRepository | None = None):
        self.roles = roles or RoleRepository()
    def read(self, actor):
        return self.roles.list_roles()
