"""crear tabla hotels

Primera migracion del proyecto: crea la tabla de hoteles.

Revision ID: 0001_hotels
Revises: (ninguna, es la primera)
"""

import sqlalchemy as sa
from alembic import op

# Identificadores que Alembic usa para ordenar las migraciones.
revision = "0001_hotels"
down_revision = None  # None significa que es la primera migracion
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Crea la tabla hotels."""
    op.create_table(
        "hotels",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("city", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),  # no se repiten nombres de hotel
    )
    op.create_index(op.f("ix_hotels_id"), "hotels", ["id"], unique=False)


def downgrade() -> None:
    """Deshace la migracion: elimina la tabla hotels."""
    op.drop_index(op.f("ix_hotels_id"), table_name="hotels")
    op.drop_table("hotels")
