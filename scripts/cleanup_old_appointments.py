import sys
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE_DIR))

from db.database import delete_old_appointments


def main():
    deleted_count = delete_old_appointments(hours_old=24)
    print(f"Deleted {deleted_count} old appointment(s).")


if __name__ == "__main__":
    main()