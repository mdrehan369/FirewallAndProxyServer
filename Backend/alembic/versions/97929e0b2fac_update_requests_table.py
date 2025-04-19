"""Update Requests Table

Revision ID: 97929e0b2fac
Revises: 
Create Date: 2025-04-19 14:06:38.990161

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '97929e0b2fac'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column("requests", "cookies", schema=sa.Column(sa.String(10000)))
    op.alter_column("requests", "headers", schema=sa.Column(sa.String(10000)))


def downgrade() -> None:
    """Downgrade schema."""
    pass
