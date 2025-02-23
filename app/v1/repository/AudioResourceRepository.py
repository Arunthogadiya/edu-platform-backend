from app.config.postgres_orm_config import scoped_session_factory
from app.v1.entity.AudioResource import AudioResource
from app.config.logger_config import LogConfig
import datetime

# Set up a logger for this repository
logger = LogConfig.setup_logger(__name__)

class AudioResourceRepository:
    def __init__(self, scoped_session_factory):
        self.scoped_session_factory = scoped_session_factory

    def create_audio_resource(self, resource_data):
        """Create a new audio resource."""
        session = self.scoped_session_factory()
        try:
            resource = AudioResource(**resource_data)
            session.add(resource)
            session.commit()
            session.refresh(resource)
            logger.info(f"Created audio resource with ID: {resource.id}")
            return resource
        except Exception as e:
            session.rollback()
            logger.error(f"Error creating audio resource: {e}")
            raise e
        finally:
            session.close()

    def get_audio_resources_by_class_and_section(self, class_value, section):
        """Retrieve audio resources filtered by class value and section."""
        session = self.scoped_session_factory()
        try:
            logger.info(f"Fetching audio resources for class: {class_value}, section: {section}")
            return session.query(AudioResource).filter(
                AudioResource.class_value == class_value,
                AudioResource.section == section
            ).all()
        finally:
            session.close()

    def get_audio_resource_by_id(self, resource_id):
        """Retrieve an audio resource by its ID."""
        session = self.scoped_session_factory()
        try:
            logger.info(f"Fetching audio resource with ID: {resource_id}")
            return session.query(AudioResource).filter(AudioResource.id == resource_id).first()
        finally:
            session.close()

    def delete_audio_resource(self, resource_id):
        """Delete an audio resource by its ID."""
        session = self.scoped_session_factory()
        try:
            logger.info(f"Deleting audio resource with ID: {resource_id}")
            resource = session.query(AudioResource).filter(AudioResource.id == resource_id).first()
            if resource:
                session.delete(resource)
                session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Error deleting audio resource: {e}")
            raise e
        finally:
            session.close()
