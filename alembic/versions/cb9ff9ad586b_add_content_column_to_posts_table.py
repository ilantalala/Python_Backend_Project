"""add content column to posts table

Revision ID: cb9ff9ad586b
Revises: ff667ab1af26
Create Date: 2025-10-30 20:29:14.706799

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cb9ff9ad586b'
down_revision: Union[str, Sequence[str], None] = 'ff667ab1af26'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts','content')
    pass
