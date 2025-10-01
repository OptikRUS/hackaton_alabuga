import sqlalchemy as sa
from alembic import op

revision = "0028"
down_revision = "0027"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "ranks_rank",
        sa.Column(
            "image_url",
            sa.String(),
            server_default="",
            nullable=True,
        ),
    )
    op.alter_column(
        "ranks_rank",
        "image_url",
        existing_type=sa.String(),
        nullable=False,
        server_default=None,
    )


def downgrade() -> None:
    op.drop_column("ranks_rank", "image_url")
