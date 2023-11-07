"""add tasks

Revision ID: 062d640ba334
Revises: 49d0fbb9db73
Create Date: 2023-11-07 16:21:00.749501

"""
from typing import Sequence, Union

from sqlalchemy import orm

from alembic import op
from internal.core.types import PriorityEnum
from internal.repositories.db.models import Task


# revision identifiers, used by Alembic.
revision: str = '062d640ba334'
down_revision: Union[str, None] = '49d0fbb9db73'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def get_tasks():
    task_1 = Task(
        name='Выезд на точку для стимулирования выдач',
        priority=PriorityEnum.HIGH,
        duration=4 * 60,
        for_junior=False,
        for_middle=False,
        for_senior=True,
    )
    task_2 = Task(
        name='Обучение агента',
        priority=PriorityEnum.MEDIUM,
        duration=2 * 60,
        for_junior=False,
        for_middle=True,
        for_senior=True,
    )
    task_3 = Task(
        name='Доставка карт и материалов',
        priority=PriorityEnum.LOW,
        duration=90,
        for_junior=True,
        for_middle=True,
        for_senior=True,
    )
    return task_1, task_2, task_3


def upgrade() -> None:
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    session.add_all(get_tasks())
    session.commit()


def downgrade() -> None:
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    for task in get_tasks():
        session.delete(task)
    session.commit()
