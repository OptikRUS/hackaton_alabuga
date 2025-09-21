import sqlalchemy as sa
from alembic import op

revision = "0006"
down_revision = "0005"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "ranks_rank",
        sa.Column("id", sa.Integer(), nullable=False, autoincrement=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("required_xp", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk_ranks_rank"),
    )
    op.create_unique_constraint("uq_ranks_name", "ranks_rank", ["name"])


def downgrade() -> None:
    op.drop_constraint("uq_ranks_name", "ranks_rank", type_="unique")
    op.drop_table("ranks_rank")



