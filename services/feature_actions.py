from __future__ import annotations

from core.contracts import ActionService

from services.actions.appointment_actions import AppointmentCreateAction
from services.actions.audit_actions import AuditCreateAction
from services.actions.backup_actions import BackupRestoreAction, BackupSaveAction
from services.actions.billing_actions import (
    PatientBillPayAction,
    ClientAmountPaymentAction,
)
from services.actions.config_actions import (
    ConfigFileReadAction,
    ConfigFileAppendAction,
)
from services.actions.content_actions import (
    BannerCreateAction,
    BannerPreviewAction,
)
from services.actions.employee_actions import (
    EmployeeRecordUpdateAction,
    DoctorNoteCreateAction,
)
from services.actions.export_actions import (
    UserExportAction,
    SessionLookupAction,
)
from services.actions.record_actions import (
    PatientRecordUploadAction,
    ExternalInsuranceStatusAction,
)
from services.actions.report_actions import ReportQueryAction
from services.actions.role_actions import RoleSyncAction
from services.actions.template_actions import TemplatePreviewAction, RulePreviewAction
from services.actions.xml_actions import InvoiceParseAction

from services.actions.extended_actions import (
    RecordDownloadAction,
    SRecordDownloadAction,
    DSearchAction,
    C2ePaymentAction,
    ExternalPaymentAction,
    I2yPaymentAction,
    C2fPaymentAction,
    InvoiceB2nAction,
    XmlReportAction,
    M2gAuditAction,
    ApiKeyStorageAction,
    LogWriteAction,
    BackupMetadataAction,
    SupportSessionAction,
    DoctorAppointmentAction,
)


def get_patient_001_action() -> ActionService:
    return AppointmentCreateAction()


def get_patient_012_action() -> ActionService:
    return PatientRecordUploadAction()


def get_patient_010_action() -> ActionService:
    return RecordDownloadAction()


def get_patient_011_action() -> ActionService:
    return SRecordDownloadAction()


def get_patient_009_action() -> ActionService:
    return DSearchAction()


def get_patient_006_action() -> ActionService:
    return PatientBillPayAction()


def get_patient_003_action() -> ActionService:
    return ClientAmountPaymentAction()


def get_patient_005_action() -> ActionService:
    return I2yPaymentAction()


def get_patient_004_action() -> ActionService:
    return C2fPaymentAction()


def get_billing_004_action() -> ActionService:
    return C2ePaymentAction()


def get_billing_005_action() -> ActionService:
    return ExternalPaymentAction()


def get_billing_002_action() -> ActionService:
    return InvoiceParseAction()


def get_billing_001_action() -> ActionService:
    return InvoiceB2nAction()


def get_billing_006_action() -> ActionService:
    return ReportQueryAction()


def get_billing_007_action() -> ActionService:
    return XmlReportAction()


def get_doctor_002_action() -> ActionService:
    return EmployeeRecordUpdateAction()


def get_doctor_001_action() -> ActionService:
    return DoctorAppointmentAction()


def get_doctor_004_action() -> ActionService:
    return DoctorNoteCreateAction()


def get_doctor_003_action() -> ActionService:
    return DoctorNoteCreateAction()


def get_role_manager_001_action() -> ActionService:
    return RoleSyncAction()


def get_role_manager_003_action(action_key: str = "default") -> ActionService | None:
    if action_key == "default":
        return ConfigFileReadAction()

    if action_key == "append":
        return ConfigFileAppendAction()

    return None


def get_role_manager_004_action() -> ActionService:
    return UserExportAction()


def get_role_manager_005_action(action_key: str = "default") -> ActionService | None:
    if action_key == "default":
        return SupportSessionAction()

    if action_key == "lookup":
        return SessionLookupAction()

    return None


def get_maintainer_006_action() -> ActionService:
    return TemplatePreviewAction()


def get_maintainer_005_action() -> ActionService:
    return RulePreviewAction()


def get_maintainer_004_action() -> ActionService:
    return BannerCreateAction()


def get_maintainer_003_action() -> ActionService:
    return BannerPreviewAction()


def get_maintainer_001_action() -> ActionService:
    return BackupRestoreAction()


def get_maintainer_002_action(action_key: str = "default") -> ActionService | None:
    if action_key == "default":
        return BackupMetadataAction()

    if action_key == "save":
        return BackupSaveAction()

    return None


def get_auditor_003_action() -> ActionService:
    return AuditCreateAction()


def get_auditor_004_action() -> ActionService:
    return LogWriteAction()


def get_auditor_005_action() -> ActionService:
    return M2gAuditAction()

def get_auditor_002_action() -> ActionService:
    return ApiKeyStorageAction()


def get_external_001_action() -> ActionService:
    return ExternalInsuranceStatusAction()