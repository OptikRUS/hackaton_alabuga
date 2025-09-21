import sqlalchemy as sa
from alembic import op

revision = "0009"
down_revision = "0008"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "rank_required_mission",
        sa.Column("rank_id", sa.Integer(), nullable=False),
        sa.Column("mission_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["rank_id"], ["ranks_rank.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["mission_id"], ["missions_mission.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("rank_id", "mission_id", name="pk_rank_required_mission"),
    )


def downgrade() -> None:
    op.drop_table("rank_required_mission")
