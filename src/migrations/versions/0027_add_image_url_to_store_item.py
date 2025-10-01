import sqlalchemy as sa
from alembic import op

revision = "0027"
down_revision = "0026"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "store_item",
        sa.Column(
            "image_url",
            sa.String(),
            server_default="",
            nullable=True,
        ),
    )
    op.alter_column(
        "store_item",
        "image_url",
        existing_type=sa.String(),
        nullable=False,
        server_default=None,
    )


def downgrade() -> None:
    op.drop_column("store_item", "image_url")
