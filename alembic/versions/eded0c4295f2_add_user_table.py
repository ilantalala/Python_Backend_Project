"""add_user_table

Revision ID: eded0c4295f2
Revises: cb9ff9ad586b
Create Date: 2025-10-30 20:57:32.308489

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eded0c4295f2'
down_revision: Union[str, Sequence[str], None] = 'cb9ff9ad586b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
    'users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column(
        'created_at',
        sa.TIMESTAMP(timezone=True),
        server_default=sa.text('now()'),
        nullable=False
    ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
)
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
    pass
