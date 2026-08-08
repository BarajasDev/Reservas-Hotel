"""crear tabla users

Cuarta migracion: crea la tabla de usuarios para el login con JWT.

Revision ID: 0004_users
Revises: 0003_bookings
"""

import sqlalchemy as sa
from alembic import op

revision = "0004_users"
down_revision = "0003_bookings"  # se aplica despues de la migracion de reservas
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Crea la tabla users."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password_hash", sa.String(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)


def downgrade() -> None:
    """Deshace la migracion: elimina la tabla users."""
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_table("users")
