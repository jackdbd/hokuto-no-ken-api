"""Add unique constraint character_id_voice_actor_id.

Revision ID: f3ac86abb948
Revises: ff7b1174a2c4
Create Date: 2018-08-11 15:00:03.537058

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f3ac86abb948"
down_revision = "ff7b1174a2c4"
branch_labels = None
depends_on = None


def upgrade():
    op.create_unique_constraint(
        "character_id_voice_actor_id",
        "characters_voice_actors",
        ["character_id", "voice_actor_id"],
    )


def downgrade():
    op.drop_constraint(
        "character_id_voice_actor_id", "characters_voice_actors", type_="unique"
    )
