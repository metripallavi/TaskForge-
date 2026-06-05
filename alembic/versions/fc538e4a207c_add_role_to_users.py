"""add role to users

Revision ID: fc538e4a207c
Revises: 9fbb9ee994ac
Create Date: 2026-06-05 12:20:01.019178

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fc538e4a207c'
down_revision: Union[str, Sequence[str], None] = '9fbb9ee994ac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Step 1: add column with default (safe for existing rows)
    op.add_column(
        'users',
        sa.Column(
            'role',
            sa.String(),
            nullable=False,
            server_default='user'
        )
    )

    # Step 2: remove server default (clean schema)
    op.alter_column(
        'users',
        'role',
        server_default=None
    )


def downgrade() -> None:
    op.drop_column('users', 'role')