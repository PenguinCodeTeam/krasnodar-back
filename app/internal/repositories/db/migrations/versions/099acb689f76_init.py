"""init

Revision ID: 099acb689f76
Revises:
Create Date: 2023-11-06 18:49:31.039449

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '099acb689f76'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'points',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('address', sa.String(), nullable=False),
        sa.Column('latitude', sa.Float(), nullable=False),
        sa.Column('longitude', sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('address'),
        sa.UniqueConstraint('id'),
    )
    op.create_table(
        'points_distance',
        sa.Column('from_point_id', sa.Uuid(), nullable=False),
        sa.Column('to_point_id', sa.Uuid(), nullable=False),
        sa.Column('duration', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('from_point_id', 'to_point_id'),
    )
    op.create_table(
        'tasks',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('priority', sa.Enum('HIGH', 'MEDIUM', 'LOW', name='priorityenum'), nullable=False),
        sa.Column('duration', sa.Integer(), nullable=False),
        sa.Column('for_junior', sa.Boolean(), nullable=False),
        sa.Column('for_middle', sa.Boolean(), nullable=False),
        sa.Column('for_senior', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
    )
    op.create_table(
        'users',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('login', sa.String(), nullable=False),
        sa.Column('password_hash', sa.LargeBinary(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('surname', sa.String(), nullable=False),
        sa.Column('patronymic', sa.String(), nullable=False),
        sa.Column('role', sa.Enum('MANAGER', 'EMPLOYEE', name='roleenum'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('id'),
        sa.UniqueConstraint('login'),
    )
    op.create_table(
        'destinations',
        sa.Column('point_id', sa.Uuid(), nullable=False),
        sa.Column('created_at', sa.Date(), nullable=False),
        sa.Column('is_delivered', sa.Boolean(), nullable=False),
        sa.Column('days_after_delivery', sa.Integer(), nullable=False),
        sa.Column('accepted_requests', sa.Integer(), nullable=False),
        sa.Column('completed_requests', sa.Integer(), nullable=False),
        sa.Column('point_completed', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ['point_id'],
            ['points.id'],
        ),
        sa.PrimaryKeyConstraint('point_id'),
    )
    op.create_table(
        'workplaces',
        sa.Column('point_id', sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(
            ['point_id'],
            ['points.id'],
        ),
        sa.PrimaryKeyConstraint('point_id'),
    )
    op.create_table(
        'workers',
        sa.Column('user_id', sa.Uuid(), nullable=False),
        sa.Column('workplace_id', sa.Uuid(), nullable=False),
        sa.Column('grade', sa.Enum('SENIOR', 'MIDDLE', 'JUNIOR', name='workergradeenum'), nullable=False),
        sa.ForeignKeyConstraint(
            ['user_id'],
            ['users.id'],
        ),
        sa.ForeignKeyConstraint(
            ['workplace_id'],
            ['workplaces.point_id'],
        ),
        sa.PrimaryKeyConstraint('user_id'),
    )
    op.create_table(
        'schedule_tasks',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('worker_id', sa.Uuid(), nullable=False),
        sa.Column('task_id', sa.Uuid(), nullable=False),
        sa.Column('working_date', sa.Date(), nullable=False),
        sa.Column('number_task', sa.Integer(), nullable=False),
        sa.Column('point_id', sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(
            ['point_id'],
            ['points.id'],
        ),
        sa.ForeignKeyConstraint(
            ['task_id'],
            ['tasks.id'],
        ),
        sa.ForeignKeyConstraint(
            ['worker_id'],
            ['workers.user_id'],
        ),
        sa.PrimaryKeyConstraint('id'),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('schedule_tasks')
    op.drop_table('workers')
    op.drop_table('workplaces')
    op.drop_table('destinations')
    op.drop_table('users')
    op.drop_table('tasks')
    op.drop_table('points_distance')
    op.drop_table('points')
    # ### end Alembic commands ###
