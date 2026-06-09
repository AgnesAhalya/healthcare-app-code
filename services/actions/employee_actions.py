
from core.contracts import ActionResult, ActionService
from db.repositories import EmployeeRepository, UserRepository
from shared.constants import (
    PHONE_RE
)
class EmployeeRecordUpdateAction(ActionService):
    def __init__(self, employees: EmployeeRepository | None = None):
        self.employees = employees or EmployeeRepository()
    def execute(self, form, files, actor):
        emergency_contact = form.get("emergency_contact", "").strip()

        if not PHONE_RE.fullmatch(emergency_contact):
            return ActionResult(
                "Invalid emergency contact. Enter a valid phone number."
            )

        return ActionResult(
            "Employee record updated",
            self.employees.update_record(
                actor.user_id,
                emergency_contact,
                ""
            )
        )

class EmployeeRecordReader:
    def __init__(self, employees: EmployeeRepository | None = None):
        self.employees = employees or EmployeeRepository()
    def read(self, actor):
        return self.employees.find_record(actor.user_id)

class DoctorNoteCreateAction(ActionService):
    def __init__(self, employees: EmployeeRepository | None = None):
        self.employees = employees or EmployeeRepository()
    def execute(self, form, files, actor):
        return ActionResult("Note saved", self.employees.create_note(form.get("patient_user_id", "user_outpatient_1"), actor.user_id, form.get("note_body", "")))

class DoctorNoteReader:
    def __init__(self, employees: EmployeeRepository | None = None):
        self.employees = employees or EmployeeRepository()
    def read(self, actor):
        return self.employees.list_notes()

class PatientListReader:
    def __init__(self, users: UserRepository | None = None):
        self.users = users or UserRepository()
    def read(self, actor):
        return self.users.list_limited_patients()
