"""crear tabla bookings

Tercera migracion: crea la tabla de reservas y la relaciona
con habitaciones mediante la llave foranea room_id.

Revision ID: 0003_bookings
Revises: 0002_rooms
"""

import sqlalchemy as sa
from alembic import op

revision = "0003_bookings"
down_revision = "0002_rooms"  # se aplica despues de la migracion de habitaciones
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Crea la tabla bookings."""
    op.create_table(
        "bookings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("guest_name", sa.String(), nullable=False),
        sa.Column("guest_email", sa.String(), nullable=False),
        sa.Column("check_in", sa.Date(), nullable=False),
        sa.Column("check_out", sa.Date(), nullable=False),
        sa.Column("total_price", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("room_id", sa.Integer(), nullable=False),
        # La llave foranea obliga a que la habitacion exista antes de reservarla.
        sa.ForeignKeyConstraint(["room_id"], ["rooms.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_bookings_id"), "bookings", ["id"], unique=False)


def downgrade() -> None:
    """Deshace la migracion: elimina la tabla bookings."""
    op.drop_index(op.f("ix_bookings_id"), table_name="bookings")
    op.drop_table("bookings")
