"""Create the healthcare SQLite schema.

This script is intentionally separate from the Flask app. Docker runs it before
starting the server so app startup stays clean and predictable.
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


from db.connection import ConnectionFactory
from db.schema import create_schema
from shared.constants import RECORDS_DIR


def main():
    RECORDS_DIR.mkdir(parents=True, exist_ok=True)
    with ConnectionFactory().connect() as conn:
        create_schema(conn)
    print("[db-init] schema ready")


if __name__ == "__main__":
    main()
