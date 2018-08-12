"""Add allegiances table (self-referential relationship between characters).

Revision ID: e21116bbbb6c
Revises: 0cf1f7e1225d
Create Date: 2018-08-12 14:45:16.020525

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e21116bbbb6c"
down_revision = "0cf1f7e1225d"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "allegiances",
        sa.Column("ally_left_id", sa.String(length=32), nullable=False),
        sa.Column("ally_right_id", sa.String(length=32), nullable=False),
        sa.ForeignKeyConstraint(["ally_left_id"], ["characters.id"]),
        sa.ForeignKeyConstraint(["ally_right_id"], ["characters.id"]),
        sa.PrimaryKeyConstraint("ally_left_id", "ally_right_id"),
    )


def downgrade():
    op.drop_table("allegiances")
