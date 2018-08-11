"""Add characters_voice_actors association table.

Revision ID: 43d723a00edc
Revises: 4c243a0ea70a
Create Date: 2018-08-11 12:00:56.086048

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "43d723a00edc"
down_revision = "4c243a0ea70a"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "characters_voice_actors",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("character_id", sa.String(length=32), nullable=False),
        sa.Column("voice_actor_id", sa.String(length=32), nullable=False),
        sa.ForeignKeyConstraint(["character_id"], ["characters.id"]),
        sa.ForeignKeyConstraint(["voice_actor_id"], ["voice_actors.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("characters_voice_actors")
