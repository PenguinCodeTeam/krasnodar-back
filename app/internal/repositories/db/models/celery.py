import uuid

from sqlalchemy.orm import Mapped, mapped_column

from internal.repositories.db.models.base import Base


class CeleryTask(Base):
    __tablename__ = 'celery_tasks'

    id: Mapped[uuid.UUID]
    task_name: Mapped[str] = mapped_column(primary_key=True)
