"""Modify length of name column from 16 to 32.

Some names are longer than 16 characters, e.g. Kenshir%C5%8D_Kasumi is 20.

Revision ID: 3c0feabaedb5
Revises: f3ac86abb948
Create Date: 2018-08-11 22:24:26.006433

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3c0feabaedb5"
down_revision = "f3ac86abb948"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        "characters",
        "name",
        existing_type=sa.VARCHAR(length=16),
        type_=sa.String(length=32),
        existing_nullable=False,
    )


def downgrade():
    op.alter_column(
        "characters",
        "name",
        existing_type=sa.String(length=32),
        type_=sa.VARCHAR(length=16),
        existing_nullable=False,
    )
