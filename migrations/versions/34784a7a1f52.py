"""Add fighting_styles

Revision ID: 34784a7a1f52
Revises: 3db2918d2223
Create Date: 2018-08-09 17:21:15.596769

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "34784a7a1f52"
down_revision = "3db2918d2223"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "fighting_styles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.Column("url", sa.String(length=128), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("fighting_styles")
