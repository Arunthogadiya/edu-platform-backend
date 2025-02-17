from app.config.postgres_orm_config import scoped_session_factory
from app.v1.entity.Attendance import Attendance
from app.config.logger_config import LogConfig

# Set up a logger for this repository
logger = LogConfig.setup_logger(__name__)

class AttendanceRepository:
    def __init__(self, scoped_session_factory):
        self.scoped_session_factory = scoped_session_factory

    def get_attendance_by_id(self, attendance_id):
        """Retrieve an attendance record by its ID."""
        session = self.scoped_session_factory()
        try:
            logger.info(f"Fetching attendance record with ID: {attendance_id}")
            return session.query(Attendance).filter(Attendance.id == attendance_id).one_or_none()
        finally:
            session.close()

    def get_attendance_by_student_id(self, student_id):
        """Retrieve attendance records by student ID."""
        session = self.scoped_session_factory()
        try:
            logger.info(f"Fetching attendance records for student ID: {student_id}")
            return session.query(Attendance).filter(Attendance.student_id == student_id).all()
        finally:
            session.close()

    def create_attendance(self, attendance_data):
        """Create a new attendance record."""
        session = self.scoped_session_factory()
        try:
            attendance = Attendance(**attendance_data)
            session.add(attendance)
            session.commit()
            logger.info(f"Created attendance record for student ID: {attendance.student_id}")
            return attendance
        except Exception as e:
            session.rollback()
            logger.error(f"Error creating attendance record: {e}")
            raise e
        finally:
            session.close()

    def update_attendance(self, attendance_id, attendance_data):
        """Update an existing attendance record."""
        session = self.scoped_session_factory()
        try:
            attendance = session.query(Attendance).filter(Attendance.id == attendance_id).one_or_none()
            if attendance:
                for key, value in attendance_data.items():
                    setattr(attendance, key, value)
                session.commit()
                logger.info(f"Updated attendance record with ID: {attendance_id}")
                return attendance
            logger.warning(f"Attendance record with ID: {attendance_id} not found")
            return None
        except Exception as e:
            session.rollback()
            logger.error(f"Error updating attendance record: {e}")
            raise e
        finally:
            session.close()

    def delete_attendance(self, attendance_id):
        """Delete an attendance record by its ID."""
        session = self.scoped_session_factory()
        try:
            attendance = session.query(Attendance).filter(Attendance.id == attendance_id).one_or_none()
            if attendance:
                session.delete(attendance)
                session.commit()
                logger.info(f"Deleted attendance record with ID: {attendance_id}")
                return True
            logger.warning(f"Attendance record with ID: {attendance_id} not found")
            return False
        except Exception as e:
            session.rollback()
            logger.error(f"Error deleting attendance record: {e}")
            raise e
        finally:
            session.close()
