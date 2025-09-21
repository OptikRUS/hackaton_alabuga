import sqlalchemy as sa
from alembic import op

revision = "0005"
down_revision = "0004"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "artifacts_artifact",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("rarity", sa.String(length=100), nullable=False),
        sa.Column("image_url", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("title", name="uq_artifacts_artifact_title"),
    )
    op.create_table(
        "artifacts_users_artifacts",
        sa.Column("artifact_id", sa.Integer(), nullable=False),
        sa.Column("user_login", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(["artifact_id"], ["artifacts_artifact.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_login"], ["users_user.login"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("artifact_id", "user_login", name="pk_artifacts_users_artifacts"),
    )
    op.create_table(
        "artifacts_missions_artifacts",
        sa.Column("artifact_id", sa.Integer(), nullable=False),
        sa.Column("mission_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["artifact_id"], ["artifacts_artifact.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["mission_id"], ["missions_mission.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint(
            "artifact_id", "mission_id", name="pk_artifacts_missions_artifacts"
        ),
    )


def downgrade() -> None:
    op.drop_table("artifacts_missions_artifacts")
    op.drop_table("artifacts_users_artifacts")
    op.drop_table("artifacts_artifact")
