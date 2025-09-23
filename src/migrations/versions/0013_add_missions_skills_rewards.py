import sqlalchemy as sa
from alembic import op

revision = "0013"
down_revision = "0012"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "missions_skills_rewards",
        sa.Column("mission_id", sa.Integer(), nullable=False),
        sa.Column("skill_id", sa.Integer(), nullable=False),
        sa.Column("level_increase", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["mission_id"], ["missions_mission.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["skill_id"], ["skills_skill.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint(
            "mission_id",
            "skill_id",
            name="pk_missions_skills_rewards",
        ),
    )


def downgrade() -> None:
    op.drop_table("missions_skills_rewards")
