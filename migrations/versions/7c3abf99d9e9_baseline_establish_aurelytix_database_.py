"""baseline: establish Aurelytix database schema

Revision ID: 7c3abf99d9e9
Revises:
Create Date: 2026-09-07
"""

from alembic import op


# revision identifiers, used by Alembic.
revision = "7c3abf99d9e9"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """Mark the existing Aurelytix database schema as the baseline."""
    pass


def downgrade():
    """Baseline migration intentionally performs no destructive operation."""
    pass
