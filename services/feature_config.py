from __future__ import annotations

from services.feature_models import FeatureConfig, Field, FormSpec, TableSpec
from services.feature_helpers import f, form, table

from services.actions.api_key_actions import (
    ApiKeyPreviewReader,
    HARDCODED_MONITORING_KEY,
)

from services.actions.appointment_actions import (
    AppointmentCreateAction,
    PatientAppointmentReader,
    DoctorAppointmentReader,
)

from services.actions.audit_actions import (
    AuditCreateAction,
    AuditListReader,
)

from services.actions.backup_actions import (
    BackupRestoreAction,
    BackupSaveAction,
)

from services.actions.billing_actions import (
    PatientBillPayAction,
    ClientAmountPaymentAction,
    PatientBillReader,
    AllBillReader,
)

from services.actions.config_actions import (
    ConfigFileReadAction,
    ConfigListReader,
    ConfigFileAppendAction,
)

from services.actions.content_actions import (
    BannerCreateAction,
    BannerListReader,
    BannerPreviewAction,
)

from services.actions.employee_actions import (
    EmployeeRecordUpdateAction,
    EmployeeRecordReader,
    DoctorNoteCreateAction,
    DoctorNoteReader,
    PatientListReader,
)

from services.actions.export_actions import (
    UserExportAction,
    SessionLookupAction,
)

from services.actions.record_actions import (
    PatientRecordUploadAction,
    PatientRecordReader,
    ExternalRecordWideReader,
    ExternalInsuranceStatusAction,
)

from services.actions.report_actions import ReportQueryAction
from services.actions.role_actions import RoleSyncAction, RoleListReader
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

from services.readers import (
    StaticReader,
    LimitedRecordsReader,
    PaymentEntryReader,
    PaymentHistoryReader,
    UserListReader,
    ConfigFileReader,
)



def get_feature_config(feature_key: str = "") -> FeatureConfig | None:
    if feature_key == "patient_001":
        return FeatureConfig(
            "patient_001",
            "Appointment Schedule",
            "outpatient",
            "Schedule outpatient appointments and view submitted requests.",
            readers={"appointments": PatientAppointmentReader()},
            forms=[
                form(
                    "Schedule appointment",
                    [
                        f("appointment_datetime", "Date and time", "datetime-local", required=True),
                        f("patient_name", "Patient name", value="Outpatient User", required=True),
                        f("reason", "Reason", "textarea", example="Follow-up consultation", required=True),
                    ],
                    submit="Schedule",
                )
            ],
            tables=[
                table(
                    "My appointments",
                    "appointments",
                    [
                        ("appointment_id", "ID"),
                        ("appointment_datetime", "Date"),
                        ("patient_name", "Patient"),
                        ("reason", "Reason"),
                    ],
                )
            ],
        )

    elif feature_key == "patient_012":
        return FeatureConfig(
            "patient_012",
            "Record Upload",
            "outpatient",
            "Upload a medical record and see the stored record list.",
            readers={"records": PatientRecordReader()},
            forms=[
                form(
                    "Upload medical record",
                    [f("record_file", "Record file", "file", required=True)],
                    submit="Upload",
                    enctype="multipart/form-data",
                )
            ],
            tables=[
                table(
                    "My records",
                    "records",
                    [
                        ("record_id", "ID"),
                        ("original_name", "File"),
                        ("stored_name", "Stored name"),
                        ("content_type", "Type"),
                    ],
                )
            ],
        )

    elif feature_key == "patient_010":
        return FeatureConfig(
            "patient_010",
            "Record Download",
            "outpatient",
            "Download a record by stored file name.",
            readers={"records": PatientRecordReader()},
            forms=[
                form(
                    "Load stored record",
                    [
                        f(
                            "record_name",
                            "Stored file name",
                            example="user_outpatient_1_lab.txt",
                            required=True,
                        )
                    ],
                    submit="Load record",
                )
            ],
            tables=[
                table(
                    "Available stored names",
                    "records",
                    [
                        ("original_name", "File"),
                        ("stored_name", "Stored name"),
                        ("content_type", "Type"),
                    ],
                )
            ],
        )

    elif feature_key == "patient_011":
        return FeatureConfig(
            "patient_011",
            "Record Viewer",
            "outpatient",
            "View records owned by the current outpatient user.",
            readers={"records": PatientRecordReader()},
            forms=[
                form(
                    "Preview own record",
                    [f("record_id", "Record ID", example="record id", required=True)],
                    submit="Preview",
                )
            ],
            tables=[
                table(
                    "My records",
                    "records",
                    [
                        ("record_id", "ID"),
                        ("original_name", "File"),
                        ("content_type", "Type"),
                    ],
                )
            ],
        )

    elif feature_key == "patient_009":
        return FeatureConfig(
            "patient_009",
            "Record Summary",
            "outpatient",
            "Search medical record summaries across the portal.",
            readers={"records": LimitedRecordsReader()},
            forms=[
                form(
                    "Search record summaries",
                    [f("patient_query", "Patient or file", example="Outpatient")],
                    submit="Search",
                )
            ],
            tables=[
                table(
                    "Record summaries",
                    "records",
                    [
                        ("record_id", "ID"),
                        ("display_name", "Patient"),
                        ("original_name", "File"),
                        ("content_type", "Type"),
                    ],
                )
            ],
        )

    elif feature_key == "patient_006":
        return FeatureConfig(
            "patient_006",
            "Bill Payment",
            "outpatient",
            "Pay outstanding bills and return to a destination after payment.",
            readers={"bills": PatientBillReader()},
            forms=[
                form(
                    "Pay bill",
                    [
                        f(
                            "bill_id",
                            "Bill",
                            "select",
                            options_from="bills",
                            option_value="bill_id",
                            option_label="description",
                        ),
                        f("return_to", "", value="/outpatient/bills", kind="hidden"),
                    ],
                    submit="Pay",
                )
            ],
            tables=[
                table(
                    "My bills",
                    "bills",
                    [
                        ("bill_id", "Bill"),
                        ("description", "Description"),
                        ("amount_cents", "Amount cents"),
                        ("status", "Status"),
                    ],
                )
            ],
        )

    elif feature_key == "patient_003":
        return FeatureConfig(
            "patient_003",
            "Payment Amount",
            "outpatient",
            "Submit the amount displayed by the patient-side payment page.",
            readers={"bills": PatientBillReader(), "payments": PaymentHistoryReader()},
            forms=[
                form(
                    "Submit payment amount",
                    [
                        f(
                            "bill_id",
                            "Bill",
                            "select",
                            options_from="bills",
                            option_value="bill_id",
                            option_label="description",
                        ),
                        f("amount", "", value="10.00", kind="hidden"),
                        f("signature", "Client signature", example="browser-generated"),
                    ],
                    submit="Submit amount",
                )
            ],
            tables=[
                table(
                    "Bills",
                    "bills",
                    [
                        ("bill_id", "Bill"),
                        ("description", "Description"),
                        ("amount_cents", "Amount cents"),
                        ("status", "Status"),
                    ],
                ),
                table(
                    "Payments",
                    "payments",
                    [
                        ("payment_id", "Payment"),
                        ("bill_id", "Bill"),
                        ("amount_cents", "Amount cents"),
                        ("note", "Note"),
                    ],
                ),
            ],
        )

    elif feature_key == "patient_005":
        return FeatureConfig(
            "patient_005",
            "Payment Proof",
            "outpatient",
            "Attach proof metadata to a payment confirmation.",
            readers={"bills": PatientBillReader(), "payments": PaymentHistoryReader()},
            forms=[
                form(
                    "Submit payment proof",
                    [
                        f(
                            "bill_id",
                            "Bill",
                            "select",
                            options_from="bills",
                            option_value="bill_id",
                            option_label="description",
                        ),
                        f("amount", "Amount", value="75.00"),
                        f("signature", "Proof signature", example="proof-token"),
                    ],
                    submit="Submit proof",
                )
            ],
            tables=[
                table(
                    "Payment history",
                    "payments",
                    [
                        ("payment_id", "Payment"),
                        ("bill_id", "Bill"),
                        ("amount_cents", "Amount cents"),
                        ("note", "Note"),
                    ],
                )
            ],
        )

    elif feature_key == "patient_004":
        return FeatureConfig(
            "patient_004",
            "Payment Confirm",
            "outpatient",
            "Confirm an open patient bill from a compact payment form.",
            readers={"bills": PatientBillReader()},
            forms=[
                form(
                    "Confirm bill",
                    [
                        f(
                            "bill_id",
                            "Bill",
                            "select",
                            options_from="bills",
                            option_value="bill_id",
                            option_label="description",
                        )
                    ],
                    submit="Confirm",
                    c2f=False,
                )
            ],
            tables=[
                table(
                    "My bills",
                    "bills",
                    [
                        ("bill_id", "Bill"),
                        ("description", "Description"),
                        ("status", "Status"),
                    ],
                )
            ],
        )

    elif feature_key == "billing_003":
        return FeatureConfig(
            "billing_003",
            "Patient View",
            "billing_staff",
            "Billing staff can view limited patient details before handling payments.",
            readers={"patients": PatientListReader()},
            tables=[
                table(
                    "Limited patients",
                    "patients",
                    [
                        ("user_id", "User"),
                        ("display_name", "Name"),
                        ("masked_phone", "Masked phone"),
                    ],
                )
            ],
        )

    elif feature_key == "billing_004":
        return FeatureConfig(
            "billing_004",
            "Payment Entry",
            "billing_staff",
            "Create a payment entry for a patient bill.",
            readers={"bills": AllBillReader(), "payments": PaymentEntryReader()},
            forms=[
                form(
                    "Create payment entry",
                    [
                        f(
                            "bill_id",
                            "Bill",
                            "select",
                            options_from="bills",
                            option_value="bill_id",
                            option_label="description",
                        ),
                        f("user_id", "Patient user ID", value="user_outpatient_1", required=True),
                        f("amount_cents", "Amount cents", value="7500", required=True),
                        f("note", "Note", example="Counter payment"),
                    ],
                    submit="Create entry",
                )
            ],
            tables=[
                table(
                    "Bills",
                    "bills",
                    [
                        ("bill_id", "Bill"),
                        ("display_name", "Patient"),
                        ("amount_cents", "Amount cents"),
                        ("status", "Status"),
                    ],
                ),
                table(
                    "Payments",
                    "payments",
                    [
                        ("payment_id", "Payment"),
                        ("bill_id", "Bill"),
                        ("display_name", "Patient"),
                        ("amount_cents", "Amount cents"),
                        ("note", "Note"),
                    ],
                ),
            ],
        )

    elif feature_key == "billing_005":
        return FeatureConfig(
            "billing_005",
            "External Payment",
            "billing_staff",
            "Prepare a payment processor URL for an external billing partner.",
            readers={"bills": AllBillReader()},
            forms=[
                form(
                    "Prepare processor link",
                    [
                        f(
                            "bill_id",
                            "Bill",
                            "select",
                            options_from="bills",
                            option_value="bill_id",
                            option_label="description",
                        ),
                        f("processor_host", "Processor host", value="processor.health.local"),
                    ],
                    submit="Prepare link",
                )
            ],
            tables=[
                table(
                    "Bills",
                    "bills",
                    [
                        ("bill_id", "Bill"),
                        ("display_name", "Patient"),
                        ("description", "Description"),
                        ("status", "Status"),
                    ],
                )
            ],
        )

    elif feature_key == "billing_002":
        return FeatureConfig(
            "billing_002",
            "Invoice",
            "billing_staff",
            "Parse an uploaded invoice document and show its root element.",
            forms=[
                form(
                    "Parse invoice",
                    [
                        f(
                            "xml_text",
                            "Invoice",
                            "textarea",
                            value="<invoice><id>bill_outpatient_1</id></invoice>",
                        ),
                        f("t_s", "Use legacy parser", "checkbox", value="yes"),
                    ],
                    submit="Parse",
                )
            ],
        )

    elif feature_key == "billing_001":
        return FeatureConfig(
            "billing_001",
            "Invoice Parser",
            "billing_staff",
            "Parse a full invoice payload for export validation.",
            forms=[
                form(
                    "Parse invoice document",
                    [
                        f(
                            "xml_text",
                            "Invoice",
                            "textarea",
                            value="<invoice><id>bill_outpatient_1</id><amount>7500</amount></invoice>",
                        )
                    ],
                    submit="Parse",
                )
            ],
        )

    elif feature_key == "billing_006":
        return FeatureConfig(
            "billing_006",
            "Billing Report",
            "billing_staff",
            "Run billing status reports over invoices and patients.",
            readers={"bills": AllBillReader()},
            forms=[
                form(
                    "Run report",
                    [
                        f(
                            "where_clause",
                            "SQL where clause",
                            value="b.status = 'open'",
                            required=True,
                        )
                    ],
                    submit="Run",
                )
            ],
            tables=[
                table(
                    "Current bills",
                    "bills",
                    [
                        ("bill_id", "Bill"),
                        ("display_name", "Patient"),
                        ("amount_cents", "Amount cents"),
                        ("status", "Status"),
                    ],
                )
            ],
        )

    elif feature_key == "billing_007":
        return FeatureConfig(
            "billing_007",
            "Alternate Report",
            "billing_staff",
            "Run an XML path filter over billing export data.",
            forms=[
                form(
                    "Run path",
                    [f("xpath", "XML path", value=".//bill", required=True)],
                    submit="Run XML report",
                )
            ],
        )

    elif feature_key == "doctor_002":
        return FeatureConfig(
            "doctor_002",
            "Employee Record",
            "doctor_nurse",
            "View and update the logged-in clinician employee record.",
            readers={"record": EmployeeRecordReader()},
            forms=[
                form(
                    "Update employee record",
                    [f("emergency_contact", "Emergency contact", value="999999", required=True)],
                    submit="Update record",
                )
            ],
            tables=[
                table(
                    "My employee record",
                    "record",
                    [
                        ("department", "Department"),
                        ("emergency_contact", "Emergency contact"),
                        ("notes", "Notes"),
                    ],
                )
            ],
        )

    elif feature_key == "doctor_001":
        return FeatureConfig(
            "doctor_001",
            "Appointment Viewer",
            "doctor_nurse",
            "View patient appointments assigned to the clinical team.",
            readers={
                "appointments": DoctorAppointmentReader(),
                "patients": PatientListReader(),
            },
            forms=[
                form(
                    "Filter appointments",
                    [f("appointment_id", "Appointment", value="")],
                    submit="Load",
                )
            ],
            tables=[
                table(
                    "Appointments",
                    "appointments",
                    [
                        ("appointment_id", "ID"),
                        ("user_id", "User"),
                        ("display_name", "Patient"),
                        ("appointment_datetime", "Date"),
                        ("reason", "Reason"),
                    ],
                )
            ],
        )

    elif feature_key == "doctor_004":
        return FeatureConfig(
            "doctor_004",
            "Doctor Notes",
            "doctor_nurse",
            "Create and review clinical notes for patient care.",
            readers={"patients": PatientListReader(), "notes": DoctorNoteReader()},
            forms=[
                form(
                    "Create note",
                    [
                        f(
                            "patient_user_id",
                            "Patient",
                            "select",
                            options_from="patients",
                            option_value="user_id",
                            option_label="display_name",
                        ),
                        f("note_body", "Note", "textarea", example="Patient reports improvement"),
                    ],
                    submit="Save note",
                )
            ],
            tables=[
                table(
                    "Notes",
                    "notes",
                    [
                        ("note_id", "ID"),
                        ("display_name", "Patient"),
                        ("note_body", "Note"),
                    ],
                )
            ],
        )

    elif feature_key == "doctor_003":
        return FeatureConfig(
            "doctor_003",
            "Shared Notes",
            "doctor_nurse",
            "Add a shared note for a patient through a lightweight clinical form.",
            readers={"patients": PatientListReader(), "notes": DoctorNoteReader()},
            forms=[
                form(
                    "Create shared note",
                    [
                        f(
                            "patient_user_id",
                            "Patient",
                            "select",
                            options_from="patients",
                            option_value="user_id",
                            option_label="display_name",
                        ),
                        f("note_body", "Note", "textarea"),
                    ],
                    submit="Save shared note",
                    c2f=False,
                )
            ],
            tables=[
                table(
                    "Notes",
                    "notes",
                    [
                        ("note_id", "ID"),
                        ("display_name", "Patient"),
                        ("note_body", "Note"),
                    ],
                )
            ],
        )

    elif feature_key == "role_manager_001":
        return FeatureConfig(
            "role_manager_001",
            "Role Management",
            "role_manager",
            "View and update employee role assignments.",
            readers={"roles": RoleListReader()},
            forms=[
                form(
                    "Update user role",
                    [
                        f("username", "Username", value="billing", required=True),
                        f("role_name", "Role", value="billing_staff", required=True),
                    ],
                    submit="Update role",
                )
            ],
            tables=[
                table(
                    "Current roles",
                    "roles",
                    [
                        ("username", "Username"),
                        ("user_type", "Base role"),
                        ("role_name", "Assigned role"),
                    ],
                )
            ],
        )

    elif feature_key == "role_manager_003":
        return FeatureConfig(
            "role_manager_003",
            "Config Files",
            "role_manager",
            "Read and update hospital configuration files.",
            readers={"files": ConfigFileReader()},
            forms=[
                form(
                    "Read config file",
                    [f("name", "File name", value="public.txt")],
                    submit="Read file",
                ),
                form(
                    "Append config file",
                    [
                        f("action", "Action", value="append", kind="hidden"),
                        f("name", "File name", value="public.txt"),
                        f("content", "Content", value="new setting line"),
                    ],
                    submit="Append file",
                ),
            ],
            tables=[
                table(
                    "Config files",
                    "files",
                    [
                        ("file", "File"),
                        ("preview", "Preview"),
                    ],
                )
            ],
        )

    elif feature_key == "role_manager_004":
        return FeatureConfig(
            "role_manager_004",
            "User Export",
            "role_manager",
            "Export user and role records for administrative review.",
            readers={"users": UserListReader(), "roles": RoleListReader()},
            forms=[form("Generate export", [], submit="Generate export")],
            tables=[
                table(
                    "Users",
                    "users",
                    [
                        ("user_id", "User"),
                        ("username", "Username"),
                        ("user_type", "Type"),
                        ("display_name", "Name"),
                        ("phone", "Phone"),
                    ],
                ),
                table(
                    "Roles",
                    "roles",
                    [
                        ("username", "Username"),
                        ("role_name", "Role"),
                    ],
                ),
            ],
        )

    elif feature_key == "role_manager_005":
        return FeatureConfig(
            "role_manager_005",
            "Support Session",
            "role_manager",
            "Attach a support session identifier before completing role support.",
            readers={"roles": RoleListReader()},
            forms=[
                form(
                    "Set support session",
                    [f("support_sid", "Support session ID", example="session id")],
                    submit="Set session",
                ),
                form(
                    "Lookup active session",
                    [f("session_id", "Session ID", example="session id")],
                    action="lookup",
                    submit="Lookup",
                ),
            ],
            tables=[
                table(
                    "Current roles",
                    "roles",
                    [
                        ("username", "Username"),
                        ("role_name", "Role"),
                    ],
                )
            ],
        )

    elif feature_key == "maintainer_006":
        return FeatureConfig(
            "maintainer_006",
            "Awareness Page",
            "maintainer",
            "Preview a health awareness page before publishing.",
            readers={"banners": BannerListReader()},
            forms=[
                form(
                    "Preview awareness template",
                    [
                        f(
                            "content",
                            "Template HTML",
                            "textarea",
                            value="<h2>{{ site_name }}</h2><p>Book your annual checkup.</p>",
                        )
                    ],
                    submit="Preview",
                )
            ],
            tables=[
                table(
                    "Published banners",
                    "banners",
                    [
                        ("title", "Title"),
                        ("banner_text", "Body"),
                    ],
                )
            ],
        )

    elif feature_key == "maintainer_005":
        return FeatureConfig(
            "maintainer_005",
            "Rule Tester",
            "maintainer",
            "Evaluate a small health promotion rule before it goes live.",
            forms=[
                form(
                    "Evaluate rule",
                    [f("expression", "Rule expression", value="risk + visits")],
                    submit="Evaluate",
                )
            ],
        )

    elif feature_key == "maintainer_004":
        return FeatureConfig(
            "maintainer_004",
            "Banner Publish",
            "maintainer",
            "Publish hospital awareness banners shown on the site.",
            readers={"banners": BannerListReader()},
            forms=[
                form(
                    "Publish banner",
                    [
                        f("title", "Title", value="Checkup Reminder"),
                        f(
                            "banner_text",
                            "Banner text",
                            "textarea",
                            value="Annual checkups are available this month.",
                        ),
                    ],
                    submit="Publish",
                )
            ],
        )

    elif feature_key == "maintainer_003":
        return FeatureConfig(
            "maintainer_003",
            "Banner Preview",
            "maintainer",
            "Preview banner content with output encoding before publishing.",
            readers={"banners": BannerListReader()},
            forms=[
                form(
                    "Preview banner",
                    [
                        f(
                            "banner_text",
                            "Body",
                            "textarea",
                            value="<strong>Vaccination drive</strong>",
                        )
                    ],
                    submit="Preview",
                )
            ],
            tables=[
                table(
                    "Banners",
                    "banners",
                    [
                        ("title", "Title"),
                        ("banner_text", "Body"),
                    ],
                )
            ],
        )

    elif feature_key == "maintainer_001":
        return FeatureConfig(
            "maintainer_001",
            "Backup Restore",
            "maintainer",
            "Restore a maintenance backup file into the content store.",
            forms=[
                form(
                    "Restore backup",
                    [f("backup_file", "Backup file", "file", required=True)],
                    submit="Restore",
                    enctype="multipart/form-data",
                )
            ],
        )

    elif feature_key == "maintainer_002":
        return FeatureConfig(
            "maintainer_002",
            "Backup Metadata",
            "maintainer",
            "Apply metadata from a backup manifest to the site configuration.",
            readers={"entries": ConfigListReader()},
            forms=[
                form(
                    "Apply metadata",
                    [
                        f("site_name", "Site name", value="Healthcare Portal"),
                        f("support_level", "Support level", value="standard"),
                        f("role_override", "Role override", value="none"),
                    ],
                    submit="Apply metadata",
                ),
                form(
                    "Save backup",
                    [
                        f("name", "Backup name", value="daily.txt"),
                        f("body", "Backup body", "textarea", value="site backup"),
                    ],
                    action="save",
                    submit="Save backup",
                ),
            ],
            tables=[
                table(
                    "Config entries",
                    "entries",
                    [
                        ("config_key", "Key"),
                        ("config_value", "Value"),
                    ],
                )
            ],
        )

    elif feature_key == "auditor_003":
        return FeatureConfig(
            "auditor_003",
            "Audit Collection",
            "security_auditor",
            "Collect anonymized audit subjects for privacy-preserving review.",
            readers={"events": AuditListReader()},
            forms=[
                form(
                    "Add audit event",
                    [
                        f("event_type", "Event type", value="profile_view"),
                        f("subject", "Anonymized subject", value="patient-8e3f"),
                    ],
                    submit="Add event",
                )
            ],
            tables=[
                table(
                    "Audit events",
                    "events",
                    [
                        ("event_id", "ID"),
                        ("event_type", "Type"),
                        ("anonymized_subject", "Subject"),
                    ],
                )
            ],
        )

    elif feature_key == "auditor_004":
        return FeatureConfig(
            "auditor_004",
            "Log Monitor",
            "security_auditor",
            "Record raw monitoring notes for audit follow-up.",
            readers={"events": AuditListReader()},
            forms=[
                form(
                    "Record log event",
                    [f("event", "Event", "textarea", value="billing review completed")],
                    submit="Record event",
                )
            ],
            tables=[
                table(
                    "Audit events",
                    "events",
                    [
                        ("event_type", "Type"),
                        ("anonymized_subject", "Subject"),
                    ],
                )
            ],
        )

    elif feature_key == "auditor_005":
        return FeatureConfig(
            "auditor_005",
            "Audit Review",
            "security_auditor",
            "Review a sensitive event and compare it with existing audit entries.",
            readers={"events": AuditListReader()},
            forms=[
                form(
                    "Review subject",
                    [f("subject", "Subject", value="patient-8e3f")],
                    submit="Review",
                )
            ],
            tables=[
                table(
                    "Existing audit events",
                    "events",
                    [
                        ("event_type", "Type"),
                        ("anonymized_subject", "Subject"),
                    ],
                )
            ],
        )

    elif feature_key == "auditor_001":
        return FeatureConfig(
            "auditor_001",
            "API Key View",
            "security_auditor",
            "View the monitoring API key used by the audit connector.",
            readers={"api_key": ApiKeyPreviewReader()},
            tables=[
                table(
                    "API key",
                    "api_key",
                    [("value", "Value")],
                )
            ],
        )

    elif feature_key == "auditor_002":
        return FeatureConfig(
            "auditor_002",
            "API Key Storage",
            "security_auditor",
            "Store a monitoring API key for the audit connector.",
            readers={"entries": ConfigListReader()},
            forms=[
                form(
                    "Store API key",
                    [f("api_key", "API key", value=HARDCODED_MONITORING_KEY)],
                    submit="Store key",
                )
            ],
            tables=[
                table(
                    "Config entries",
                    "entries",
                    [
                        ("config_key", "Key"),
                        ("config_value", "Value"),
                    ],
                )
            ],
        )

    elif feature_key == "external_001":
        return FeatureConfig(
            "external_001",
            "Insurance Payment Status",
            "external_user",
            "Update customer insurance payment status from the insurance portal.",

            readers={"records": ExternalRecordWideReader()},
            forms=[
                form(
                    "Update insurance status",
                    [
                        f(
                            "bill_id",
                            "Bill ID",
                            "select",
                            options_from="records",
                            option_value="bill_id",
                            option_label="description",
                            required=True,
                        ),
                        f(
                            "status",
                            "Insurance status",
                            value="insurance_approved",
                            required=True,
                        ),
                    ],
                    submit="Update status",
                )
            ],
            tables=[
                table(
                    "Customer records",
                    "records",
                    [
                        ("bill_id", "Bill"),
                        ("display_name", "Customer"),
                        ("description", "Payment"),
                        ("status", "Status"),
                        ("amount_cents", "Amount cents"),
                    ],
                )
            ],
        )

    return None