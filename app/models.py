from datetime import datetime, timedelta
from app import db

class Attendance(db.Model):
    __tablename__ = 'attendance'

    id = db.Column(db.Integer, primary_key=True)
    person_name = db.Column(db.String(100), nullable=False)
    class_id = db.Column(db.String(20))
    action = db.Column(db.String(10), nullable=False)  # 'enter' or 'exit'
    timestamp = db.Column(db.DateTime, nullable=False)
    entry_time = db.Column(db.DateTime)
    exit_time = db.Column(db.DateTime)
    duty_duration = db.Column(db.Interval)  # Note: use Integer if your DB doesn't support Interval

    @staticmethod
    def get_last_record(class_id):
        return Attendance.query.filter_by(class_id=class_id)\
                               .order_by(Attendance.timestamp.desc())\
                               .first()
