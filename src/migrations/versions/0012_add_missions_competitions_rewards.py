import sqlalchemy as sa
from alembic import op

revision = "0012"
down_revision = "0011"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "missions_competitions_rewards",
        sa.Column("mission_id", sa.Integer(), nullable=False),
        sa.Column("competition_id", sa.Integer(), nullable=False),
        sa.Column("level_increase", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["mission_id"], ["missions_mission.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["competition_id"], ["competitions_competition.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint(
            "mission_id",
            "competition_id",
            name="pk_missions_competitions_rewards",
        ),
    )


def downgrade() -> None:
    op.drop_table("missions_competitions_rewards")
