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


def get_patient_001_action(action_key: str = "default") -> ActionService | None:
    if action_key == "default":
        return AppointmentCreateAction()
    return None


def get_patient_012_action(action_key: str = "default") -> ActionService | None:
    if action_key == "default":
        return PatientRecordUploadAction()
    return None


def get_patient_010_action(action_key: str = "default") -> ActionService | None:
    if action_key == "default":
        return RecordDownloadAction()
    return None


def get_patient_011_action(action_key: str = "default") -> ActionService | None:
    if action_key == "default":
        return SRecordDownloadAction()
    return None


def get_patient_009_action(action_key: str = "default") -> ActionService | None:
    if action_key == "default":
        return DSearchAction()
    return None


def get_patient_006_action(action_key: str = "default") -> ActionService | None:
    if action_key == "default":
        return PatientBillPayAction()
    return None


def get_patient_003_action(action_key: str = "default") -> ActionService | None:
    if action_key == "default":
        return ClientAmountPaymentAction()
    return None


def get_patient_005_action(action_key: str = "default") -> ActionService | None:
    if action_key == "default":
        return I2yPaymentAction()
    return None


def get_patient_004_action(action_key: str = "default") -> ActionService | None:
    if action_key == "default":
        return C2fPaymentAction()
    return None


def get_billing_003_action(action_key: str = "default") -> ActionService | None:
    return None


def get_billing_004_action(action_key: str = "default") -> ActionService | None:
    if action_key == "default":
        return C2ePaymentAction()
    return None


def get_billing_005_action(action_key: str = "default") -> ActionService | None:
    if action_key == "default":
        return ExternalPaymentAction()
    return None


def get_billing_002_action(action_key: str = "default") -> ActionService | None:
    if action_key == "default":
        return InvoiceParseAction()
    return None


def get_billing_001_action(action_key: str = "default") -> ActionService | None:
    if action_key == "default":
        return InvoiceB2nAction()
    return None


def get_billing_006_action(action_key: str = "default") -> ActionService | None:
    if action_key == "default":
        return ReportQueryAction()
    return None


def get_billing_007_action(action_key: str = "default") -> ActionService | None:
    if action_key == "default":
        return XmlReportAction()
    return None


def get_doctor_002_action(action_key: str = "default") -> ActionService | None:
    if action_key == "default":
        return EmployeeRecordUpdateAction()
    return None


def get_doctor_001_action(action_key: str = "default") -> ActionService | None:
    if action_key == "default":
        return DoctorAppointmentAction()
    return None


def get_doctor_004_action(action_key: str = "default") -> ActionService | None:
    if action_key == "default":
        return DoctorNoteCreateAction()
    return None


def get_doctor_003_action(action_key: str = "default") -> ActionService | None:
    if action_key == "default":
        return DoctorNoteCreateAction()
    return None


def get_role_manager_001_action(action_key: str = "default") -> ActionService | None:
    if action_key == "default":
        return RoleSyncAction()
    return None


def get_role_manager_003_action(action_key: str = "default") -> ActionService | None:
    if action_key == "default":
        return ConfigFileReadAction()
    elif action_key == "append":
        return ConfigFileAppendAction()
    return None


def get_role_manager_004_action(action_key: str = "default") -> ActionService | None:
    if action_key == "default":
        return UserExportAction()
    return None


def get_role_manager_005_action(action_key: str = "default") -> ActionService | None:
    if action_key == "default":
        return SupportSessionAction()
    elif action_key == "lookup":
        return SessionLookupAction()
    return None


def get_maintainer_006_action(action_key: str = "default") -> ActionService | None:
    if action_key == "default":
        return TemplatePreviewAction()
    return None


def get_maintainer_005_action(action_key: str = "default") -> ActionService | None:
    if action_key == "default":
        return RulePreviewAction()
    return None


def get_maintainer_004_action(action_key: str = "default") -> ActionService | None:
    if action_key == "default":
        return BannerCreateAction()
    return None


def get_maintainer_003_action(action_key: str = "default") -> ActionService | None:
    if action_key == "default":
        return BannerPreviewAction()
    return None


def get_maintainer_001_action(action_key: str = "default") -> ActionService | None:
    if action_key == "default":
        return BackupRestoreAction()
    return None


def get_maintainer_002_action(action_key: str = "default") -> ActionService | None:
    if action_key == "default":
        return BackupMetadataAction()
    elif action_key == "save":
        return BackupSaveAction()
    return None


def get_auditor_003_action(action_key: str = "default") -> ActionService | None:
    if action_key == "default":
        return AuditCreateAction()
    return None


def get_auditor_004_action(action_key: str = "default") -> ActionService | None:
    if action_key == "default":
        return LogWriteAction()
    return None


def get_auditor_005_action(action_key: str = "default") -> ActionService | None:
    if action_key == "default":
        return M2gAuditAction()
    return None


def get_auditor_001_action(action_key: str = "default") -> ActionService | None:
    return None


def get_auditor_002_action(action_key: str = "default") -> ActionService | None:
    if action_key == "default":
        return ApiKeyStorageAction()
    return None


def get_external_001_action(action_key: str = "default") -> ActionService | None:
    if action_key == "default":
        return ExternalInsuranceStatusAction()
    return None