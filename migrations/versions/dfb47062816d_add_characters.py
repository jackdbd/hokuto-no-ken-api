"""Add characters

Revision ID: dfb47062816d
Revises: 
Create Date: 2018-08-09 17:17:09.014348

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "dfb47062816d"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "characters",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name_kanji", sa.String(length=16), nullable=False),
        sa.Column("name_romaji", sa.String(length=64), nullable=False),
        sa.Column("avatar", sa.String(length=128), nullable=True),
        sa.Column("url", sa.String(length=128), nullable=True),
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


def downgrade():
    op.drop_index(op.f("ix_characters_name_romaji"), table_name="characters")
    op.drop_index(op.f("ix_characters_name_kanji"), table_name="characters")
    op.drop_table("characters")
