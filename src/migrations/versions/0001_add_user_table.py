import sqlalchemy as sa
from alembic import op

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users_user",
        sa.Column("login", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("role", sa.String(), nullable=False),
        sa.Column("rank_id", sa.Integer(), nullable=False),
        sa.Column("exp", sa.Integer(), nullable=False),
        sa.Column("mana", sa.Integer(), nullable=False),
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("login", name="pk_users_user_table"),
    )


def downgrade() -> None:
    op.drop_table("users_user")
