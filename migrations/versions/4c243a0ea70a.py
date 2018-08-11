"""Alter id datatype in characters, voice_actors and fighting_styles.

A previous run of `flask db migrate` didn't detect changes in such tables.
If you want Alembic (via Flask-Migrate) to detect datatype changes, instantiate
the Flask-Migrate extension with `Migrate(compare_type=True)`.

Revision ID: 4c243a0ea70a
Revises: 34784a7a1f52
Create Date: 2018-08-11 11:33:23.001294

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "4c243a0ea70a"
down_revision = "34784a7a1f52"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        "characters",
        "id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=32),
        autoincrement=False,
    )
    op.alter_column(
        "fighting_styles",
        "id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=32),
        autoincrement=False,
    )
    op.alter_column(
        "voice_actors",
        "id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=32),
        autoincrement=False,
    )


def downgrade():
    op.alter_column(
        "voice_actors",
        "id",
        existing_type=sa.String(length=32),
        type_=sa.INTEGER(),
        autoincrement=False,
    )
    op.alter_column(
        "fighting_styles",
        "id",
        existing_type=sa.String(length=32),
        type_=sa.INTEGER(),
        autoincrement=False,
    )
    op.alter_column(
        "characters",
        "id",
        existing_type=sa.String(length=32),
        type_=sa.INTEGER(),
        autoincrement=False,
    )
