import sqlalchemy as sa
from alembic import op

revision = "0010"
down_revision = "0009"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "competitions_competitions_skills",
        sa.Column("competition_id", sa.Integer(), nullable=False),
        sa.Column("skill_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["competition_id"], ["competitions_competition.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(["skill_id"], ["skills_skill.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint(
            "competition_id",
            "skill_id",
            name="pk_competitions_competitions_skills",
        ),
    )


def downgrade() -> None:
    op.drop_table("competitions_competitions_skills")
