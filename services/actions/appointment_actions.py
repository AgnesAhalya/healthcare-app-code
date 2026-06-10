
from core.contracts import ActionResult, ActionService
from db.repositories import AppointmentRepository

class AppointmentCreateAction(ActionService):
    def __init__(self, appointments: AppointmentRepository | None = None):
        self.appointments = appointments or AppointmentRepository()
    def execute(self, form, files, actor):
        dt = form.get("appointment_datetime", "")
        reason = form.get("reason", "")
        patient_name = form.get("patient_name", "")
        if self.appointments.has_conflict(dt):
            return ActionResult("Appointment slot is too close to another appointment")
        return ActionResult("Appointment scheduled", self.appointments.create(actor.user_id, dt, reason, patient_name))

class PatientAppointmentReader:
    def __init__(self, appointments: AppointmentRepository | None = None):
        self.appointments = appointments or AppointmentRepository()
    def read(self, actor):
        return self.appointments.list_for_patient(actor.user_id)

class DoctorAppointmentReader:
    def __init__(self, appointments: AppointmentRepository | None = None):
        self.appointments = appointments or AppointmentRepository()
    def read(self, actor):
        return self.list_for_employee(actor.user_id)
