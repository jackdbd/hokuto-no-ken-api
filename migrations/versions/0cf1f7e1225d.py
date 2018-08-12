"""Add family_members table (self-referential relationship between characters).

Revision ID: 0cf1f7e1225d
Revises: d162daa1f162
Create Date: 2018-08-12 13:01:49.676811

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0cf1f7e1225d"
down_revision = "d162daa1f162"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "family_members",
        sa.Column("relative_left_id", sa.String(length=32), nullable=False),
        sa.Column("relative_right_id", sa.String(length=32), nullable=False),
        sa.ForeignKeyConstraint(["relative_left_id"], ["characters.id"]),
        sa.ForeignKeyConstraint(["relative_right_id"], ["characters.id"]),
        sa.PrimaryKeyConstraint("relative_left_id", "relative_right_id"),
    )


def downgrade():
    op.drop_table("family_members")
