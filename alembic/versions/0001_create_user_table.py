
"""create user table

Revision ID: 0001_create_user_table
Revises: 
Create Date: 2025-10-21
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_create_user_table'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        "user",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("username", sa.String, unique=True, nullable=False),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("email", sa.String, nullable=False),
    )

def downgrade():
    op.drop_table("user")
