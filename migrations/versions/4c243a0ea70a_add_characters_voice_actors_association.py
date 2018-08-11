"""Add characters_voice_actors association

Revision ID: 4c243a0ea70a
Revises: 34784a7a1f52
Create Date: 2018-08-11 08:28:56.086048

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "4c243a0ea70a"
down_revision = "34784a7a1f52"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "characters_voice_actors",
        sa.Column("character_id", sa.Integer(), nullable=True),
        sa.Column("voice_actor_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["character_id"], ["characters.id"]),
        sa.ForeignKeyConstraint(["voice_actor_id"], ["voice_actors.id"]),
    )


# ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("characters_voice_actors")


# ### end Alembic commands ###
