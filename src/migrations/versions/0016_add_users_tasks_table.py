import sqlalchemy as sa
from alembic import op

revision = "0016"
down_revision = "0015"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users_tasks",
        sa.Column("task_id", sa.Integer(), nullable=False),
        sa.Column("user_login", sa.String(), nullable=False),
        sa.Column("is_completed", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["task_id"],
            ["missions_mission_task.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_login"],
            ["users_user.login"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("task_id", "user_login", name="pk_users_tasks"),
    )


def downgrade() -> None:
    op.drop_table("users_tasks")
