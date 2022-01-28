"""init

Revision ID: 1cf97648ad02
Revises:
Create Date: 2022-01-28 15:19:17.921346

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1cf97648ad02"
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
    op.create_table(
        "exercises",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("title", sa.String, nullable=False),
        sa.Column("description", sa.String),
        sa.Column("rest_time", sa.Integer),
        sa.Column("owner_id", sa.Integer, nullable=False),
        sa.Column("owner", sa.String),
    )


def downgrade():
    pass
