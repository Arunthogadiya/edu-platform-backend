from app.config.postgres_orm_config import scoped_session_factory
from app.v1.entity.TalentProfiles import TalentProfiles
from app.config.logger_config import LogConfig

# Set up a logger for this repository
logger = LogConfig.setup_logger(__name__)

class TalentProfilesRepository:
    def __init__(self, scoped_session_factory):
        self.scoped_session_factory = scoped_session_factory

    def get_profile_by_id(self, profile_id):
        """Retrieve a talent profile by its ID."""
        session = self.scoped_session_factory()
        try:
            logger.info(f"Fetching talent profile with ID: {profile_id}")
            return session.query(TalentProfiles).filter(TalentProfiles.id == profile_id).one_or_none()
        finally:
            session.close()

    def get_profiles_by_student_id(self, student_id):
        """Retrieve talent profiles by student ID."""
        session = self.scoped_session_factory()
        try:
            logger.info(f"Fetching talent profiles for student ID: {student_id}")
            return session.query(TalentProfiles).filter(TalentProfiles.student_id == student_id).all()
        finally:
            session.close()

    def create_profile(self, profile_data):
        """Create a new talent profile."""
        session = self.scoped_session_factory()
        try:
            profile = TalentProfiles(**profile_data)
            session.add(profile)
            session.commit()
            logger.info(f"Created talent profile for student ID: {profile.student_id}")
            return profile
        except Exception as e:
            session.rollback()
            logger.error(f"Error creating talent profile: {e}")
            raise e
        finally:
            session.close()

    def update_profile(self, profile_id, profile_data):
        """Update an existing talent profile."""
        session = self.scoped_session_factory()
        try:
            profile = session.query(TalentProfiles).filter(TalentProfiles.id == profile_id).one_or_none()
            if profile:
                for key, value in profile_data.items():
                    setattr(profile, key, value)
                session.commit()
                logger.info(f"Updated talent profile with ID: {profile_id}")
                return profile
            logger.warning(f"Talent profile with ID: {profile_id} not found")
            return None
        except Exception as e:
            session.rollback()
            logger.error(f"Error updating talent profile: {e}")
            raise e
        finally:
            session.close()

    def delete_profile(self, profile_id):
        """Delete a talent profile by its ID."""
        session = self.scoped_session_factory()
        try:
            profile = session.query(TalentProfiles).filter(TalentProfiles.id == profile_id).one_or_none()
            if profile:
                session.delete(profile)
                session.commit()
                logger.info(f"Deleted talent profile with ID: {profile_id}")
                return True
            logger.warning(f"Talent profile with ID: {profile_id} not found")
            return False
        except Exception as e:
            session.rollback()
            logger.error(f"Error deleting talent profile: {e}")
            raise e
        finally:
            session.close()
