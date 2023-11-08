"""add task types

Revision ID: 062d640ba334
Revises: 49d0fbb9db73
Create Date: 2023-11-07 16:21:00.749501

"""
from typing import Sequence, Union

from sqlalchemy import orm

from alembic import op
from internal.core.types import PriorityEnum, WorkerGradeEnum
from internal.repositories.db.models import TaskGrade, TaskType


# revision identifiers, used by Alembic.
revision: str = '062d640ba334'
down_revision: Union[str, None] = '49d0fbb9db73'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def get_tasks():
    task_type_1 = TaskType(
        id=1,
        name='Выезд на точку для стимулирования выдач',
        priority=PriorityEnum.HIGH,
        duration=4 * 60,
    )
    task_type_2 = TaskType(
        id=2,
        name='Обучение агента',
        priority=PriorityEnum.MEDIUM,
        duration=2 * 60,
    )
    task_type_3 = TaskType(
        id=3,
        name='Доставка карт и материалов',
        priority=PriorityEnum.LOW,
        duration=90,
    )

    task_type_1_grade = TaskGrade(
        task_type=task_type_1,
        grade=WorkerGradeEnum.SENIOR,
    )

    task_type_2_grade_1 = TaskGrade(
        task_type=task_type_2,
        grade=WorkerGradeEnum.SENIOR,
    )
    task_type_2_grade_2 = TaskGrade(
        task_type=task_type_2,
        grade=WorkerGradeEnum.MIDDLE,
    )

    task_type_3_grade_1 = TaskGrade(
        task_type=task_type_3,
        grade=WorkerGradeEnum.SENIOR,
    )
    task_type_3_grade_2 = TaskGrade(
        task_type=task_type_3,
        grade=WorkerGradeEnum.MIDDLE,
    )
    task_type_3_grade_3 = TaskGrade(
        task_type=task_type_3,
        grade=WorkerGradeEnum.JUNIOR,
    )

    return (
        task_type_1,
        task_type_2,
        task_type_3,
        task_type_1_grade,
        task_type_2_grade_1,
        task_type_2_grade_2,
        task_type_3_grade_1,
        task_type_3_grade_2,
        task_type_3_grade_3,
    )


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
