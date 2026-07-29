"""crear tabla rooms

Segunda migracion: crea la tabla de habitaciones y la relaciona
con hoteles mediante la llave foranea hotel_id.

Revision ID: 0002_rooms
Revises: 0001_hotels
"""

import sqlalchemy as sa
from alembic import op

revision = "0002_rooms"
down_revision = "0001_hotels"  # se aplica despues de la migracion de hoteles
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Crea la tabla rooms."""
    op.create_table(
        "rooms",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("number", sa.String(), nullable=False),
        sa.Column("room_type", sa.String(), nullable=False),
        sa.Column("capacity", sa.Integer(), nullable=False),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.Column("is_available", sa.Boolean(), nullable=False),
        sa.Column("hotel_id", sa.Integer(), nullable=False),
        # La llave foranea obliga a que el hotel exista antes de crear la habitacion.
        sa.ForeignKeyConstraint(["hotel_id"], ["hotels.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_rooms_id"), "rooms", ["id"], unique=False)


def downgrade() -> None:
    """Deshace la migracion: elimina la tabla rooms."""
    op.drop_index(op.f("ix_rooms_id"), table_name="rooms")
    op.drop_table("rooms")
