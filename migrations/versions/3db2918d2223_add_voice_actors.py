"""Add voice_actors

Revision ID: 3db2918d2223
Revises: dfb47062816d
Create Date: 2018-08-09 17:19:03.113231

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3db2918d2223"
down_revision = "dfb47062816d"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "voice_actors",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.Column("url", sa.String(length=128), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("voice_actors")
