"""add manager

Revision ID: 49d0fbb9db73
Revises: 099acb689f76
Create Date: 2023-11-06 19:01:10.765963

"""
from typing import Sequence, Union

from sqlalchemy import orm

from alembic import op
from internal.core.types import RoleEnum
from internal.core.utils import hash_password
from internal.repositories.db.models import User


# revision identifiers, used by Alembic.
revision: str = '49d0fbb9db73'
down_revision: Union[str, None] = '099acb689f76'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def get_superuser() -> User:
    return User(
        login='manager',
        password_hash=hash_password('pass'),
        name='Иван',
        surname='Иванов',
        patronymic='Иванович',
        role=RoleEnum.MANAGER,
    )


def upgrade() -> None:
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    session.add(get_superuser())
    session.commit()


def downgrade() -> None:
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    session.delete(get_superuser())
    session.commit()
