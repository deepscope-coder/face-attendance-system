from datetime import datetime
import pytz
from app.models import Attendance
from app import db

IST = pytz.timezone('Asia/Kolkata')

class AttendanceLogger:
    @staticmethod
    def log_attendance(person_name, class_id, action):
        now = datetime.now(IST)
        last_record = Attendance.get_last_record(class_id)

        if action == 'enter':
            if last_record and last_record.action == 'enter':
                return False, "Person has already entered without exiting"
            attendance = Attendance(
                person_name=person_name,
                class_id=class_id,
                action='enter',
                timestamp=now,
                entry_time=now
            )
        elif action == 'exit':
            if not last_record or last_record.action == 'exit':
                return False, "Person hasn't entered yet"
            duration = now - last_record.entry_time if last_record.entry_time else None
            attendance = Attendance(
                person_name=person_name,
                class_id=class_id,
                action='exit',
                timestamp=now,
                exit_time=now,
                duty_duration=duration
            )
        else:
            return False, "Invalid action"

        db.session.add(attendance)
        db.session.commit()
        return True, "Attendance logged successfully"
