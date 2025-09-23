import sqlalchemy as sa
from alembic import op

revision = "0011"
down_revision = "0010"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "ranks_competitions_requirements",
        sa.Column("rank_id", sa.Integer(), nullable=False),
        sa.Column("competition_id", sa.Integer(), nullable=False),
        sa.Column("min_level", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["rank_id"], ["ranks_rank.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["competition_id"], ["competitions_competition.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint(
            "rank_id",
            "competition_id",
            name="pk_ranks_competitions_requirements",
        ),
    )


def downgrade() -> None:
    op.drop_table("ranks_competitions_requirements")
