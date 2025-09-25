import sqlalchemy as sa
from alembic import op

revision = "0015"
down_revision = "0014"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "missions_branch",
        sa.Column(
            "start_date",
            sa.DateTime(),
            nullable=False,
        ),
    )
    op.add_column(
        "missions_branch",
        sa.Column(
            "end_date",
            sa.DateTime(),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_column("missions_branch", "end_date")
    op.drop_column("missions_branch", "start_date")
