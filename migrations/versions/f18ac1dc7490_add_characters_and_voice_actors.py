"""Add characters and voice actors

Revision ID: f18ac1dc7490
Revises: 
Create Date: 2018-08-07 22:34:31.880640

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f18ac1dc7490"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "characters",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name_kanji", sa.String(length=16), nullable=False),
        sa.Column("name_romaji", sa.String(length=32), nullable=False),
        sa.Column("avatar", sa.String(length=128), nullable=True),
        sa.Column("url", sa.String(length=32), nullable=True),
        sa.Column("is_not_in_manga", sa.Boolean(), nullable=False),
        sa.Column("first_anime_episode", sa.Integer(), nullable=True),
        sa.Column("first_manga_chapter", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_characters_name_kanji"), "characters", ["name_kanji"], unique=False
    )
    op.create_index(
        op.f("ix_characters_name_romaji"), "characters", ["name_romaji"], unique=False
    )
    op.create_table(
        "voice_actors",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.Column("url", sa.String(length=32), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )


# ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("voice_actors")
    op.drop_index(op.f("ix_characters_name_romaji"), table_name="characters")
    op.drop_index(op.f("ix_characters_name_kanji"), table_name="characters")
    op.drop_table("characters")


# ### end Alembic commands ###