import os

from flask import Flask, redirect, url_for
from shared.extensions import csrf
from shared.rate_limiter import limiter
from features.auditor_001.routes import auditor_001_bp
from features.auditor_002.routes import auditor_002_bp
from features.auditor_003.routes import auditor_003_bp
from features.auditor_004.routes import auditor_004_bp
from features.auditor_005.routes import auditor_005_bp
from features.billing_001.routes import billing_001_bp
from features.billing_002.routes import billing_002_bp
from features.billing_003.routes import billing_003_bp
from features.billing_004.routes import billing_004_bp
from features.billing_005.routes import billing_005_bp
from features.billing_006.routes import billing_006_bp
from features.billing_007.routes import billing_007_bp
from features.doctor_001.routes import doctor_001_bp
from features.doctor_002.routes import doctor_002_bp
from features.doctor_003.routes import doctor_003_bp
from features.doctor_004.routes import doctor_004_bp
from features.external_001.routes import external_001_bp
from features.maintainer_001.routes import maintainer_001_bp
from features.maintainer_002.routes import  maintainer_002_bp
from features.maintainer_003.routes import  maintainer_003_bp
from features.maintainer_004.routes import  maintainer_004_bp
from features.maintainer_005.routes import  maintainer_005_bp
from features.maintainer_006.routes import  maintainer_006_bp
from features.patient_001.routes import patient_001_bp
from features.patient_002.routes import patient_002_bp
from features.patient_003.routes import patient_003_bp
from features.patient_004.routes import patient_004_bp
from features.patient_005.routes import patient_005_bp
from features.patient_006.routes import patient_006_bp
from features.patient_007.routes import patient_007_bp
from features.patient_009.routes import patient_009_bp
from features.patient_010.routes import patient_010_bp
from features.patient_011.routes import patient_011_bp
from features.patient_012.routes import patient_012_bp
from features.patient_013.routes import patient_013_bp
from features.role_manager_001.routes import role_manager_001_bp
from features.role_manager_003.routes import role_manager_003_bp
from features.role_manager_004.routes import role_manager_004_bp
from features.role_manager_005.routes import role_manager_005_bp


def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret")
    app.config.update(
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=False,
        MAX_CONTENT_LENGTH=2 * 1024 * 1024,
    )
    limiter.init_app(app)
    csrf.init_app(app)
    app.register_blueprint(auditor_001_bp)
    app.register_blueprint(auditor_002_bp)
    app.register_blueprint(auditor_003_bp)
    app.register_blueprint(auditor_004_bp)
    app.register_blueprint(auditor_005_bp)
    app.register_blueprint(billing_001_bp)
    app.register_blueprint(billing_002_bp)
    app.register_blueprint(billing_003_bp)
    app.register_blueprint(billing_004_bp)
    app.register_blueprint(billing_005_bp)
    app.register_blueprint(billing_006_bp)
    app.register_blueprint(billing_007_bp)
    app.register_blueprint(doctor_001_bp)
    app.register_blueprint(doctor_002_bp)
    app.register_blueprint(doctor_003_bp)
    app.register_blueprint(doctor_004_bp)
    app.register_blueprint(external_001_bp)
    app.register_blueprint(maintainer_001_bp)
    app.register_blueprint(maintainer_002_bp)
    app.register_blueprint(maintainer_003_bp)
    app.register_blueprint(maintainer_004_bp)
    app.register_blueprint(maintainer_005_bp)
    app.register_blueprint(maintainer_006_bp)
    app.register_blueprint(patient_001_bp)
    app.register_blueprint(patient_002_bp)
    app.register_blueprint(patient_003_bp)
    app.register_blueprint(patient_004_bp)
    app.register_blueprint(patient_005_bp)
    app.register_blueprint(patient_006_bp)
    app.register_blueprint(patient_007_bp)
    app.register_blueprint(patient_009_bp)
    app.register_blueprint(patient_010_bp)
    app.register_blueprint(patient_011_bp)
    app.register_blueprint(patient_012_bp)
    app.register_blueprint(patient_013_bp)
    app.register_blueprint(role_manager_001_bp)
    app.register_blueprint(role_manager_003_bp)
    app.register_blueprint(role_manager_004_bp)
    app.register_blueprint(role_manager_005_bp)


    @app.context_processor
    def inject_role_navigation():
        nav_by_role = {
            "outpatient": [
                ("Profile", "/outpatient/profile"),
                ("Appointments", "/outpatient/appointments/schedule"),
                ("Upload", "/outpatient/records"),
                ("Download", "/outpatient/records/download"),
                ("Viewer", "/outpatient/records/s2e"),
                ("Summary", "/outpatient/records/dsce"),
                ("Bills", "/outpatient/bills"),
                ("Amount", "/outpatient/payment-amount"),
                ("Proof", "/outpatient/payments/i2y"),
                ("Confirm", "/maintainer/c2f"),
            ],
            "inpatient": [("Profile", "/inpatient/profile")],
            "doctor_nurse": [
                ("Employee", "/doctor/employee-record"),
                ("Appointments", "/doctor/appointments"),
                ("Notes", "/doctor/notes"),
                ("Shared Notes", "/doctor/notes/c2f"),
            ],
            "billing_staff": [
                ("Patients", "/billing-patient-view"),
                ("Payments", "/billing-payments"),
                ("External", "/billing-payments-external"),
                ("Invoice", "/billing-invoices-sec"),
                ("Parser", "/billing-invoices"),
                ("Report", "/billing-reports"),
                ("Report Alternative", "/billing-reports-xpf"),
            ],
            "role_manager": [
                ("Roles", "/role-manager/roles"),
                ("Config", "/role-manager/config"),
                ("Export", "/role-manager/export"),
                ("Session", "/role-manager/session"),
            ],
            "maintainer": [
                ("Awareness", "/maintainer/awareness"),
                ("Rules", "/maintainer/c2l"),
                ("Banner", "/maintainer/banner"),
                ("Preview", "/maintainer/banner-e2g"),
                ("Restore", "/maintainer/backup"),
                ("Metadata", "/maintainer/backup-mass"),
            ],
            "security_auditor": [
                ("Audit", "/auditor-audit"),
                ("Review", "/auditor/logs"),
                ("Logs", "/auditor-logs-write"),
                ("API View", "/auditor-api-keys"),
                ("API Store", "/auditor-api-keys-store"),
            ],
            "external_user": [("Records", "/external/records")],
        }
        from flask import session
        return {"role_nav_links": nav_by_role.get(session.get("usertype"), [])}

    @app.route("/")
    def index():
        return redirect(url_for("patient_002.login_page"))

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
