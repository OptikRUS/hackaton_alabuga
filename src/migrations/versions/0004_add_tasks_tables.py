import sqlalchemy as sa
from alembic import op

revision = "0004"
down_revision = "0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "missions_mission_task",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("title", name="uq_missions_task_title"),
    )
    op.create_table(
        "missions_missions_tasks",
        sa.Column("task_id", sa.Integer(), nullable=False),
        sa.Column("mission_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["mission_id"],
            ["missions_mission.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["task_id"],
            ["missions_mission_task.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("task_id", "mission_id", name="pk_missions_mission_tasks"),
    )


def downgrade() -> None:
    op.drop_table("missions_missions_tasks")
    op.drop_table("missions_mission_task")
