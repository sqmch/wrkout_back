"""init

Revision ID: 993c5acc5689
Revises:
Create Date: 2022-01-28 12:50:39.874844

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
#revision = '993c5acc5689'
revision = "538456863f8e"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("email", sa.String, nullable=False),
        sa.Column("hashed_password", sa.String, nullable=False),
        sa.Column("is_active", sa.Boolean, nullable=False),
        sa.Column("routines", sa.String),
    )

    op.create_table(
        "routines",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("title", sa.String, nullable=False),
        sa.Column("description", sa.String),
        sa.Column("owner_id", sa.Integer, nullable=False),
        sa.Column("owner", sa.String),
        sa.Column("exercises", sa.String),
    )


def downgrade():
    op.drop_table("users")
    op.drop_table("routines")
