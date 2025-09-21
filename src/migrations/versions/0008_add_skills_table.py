import sqlalchemy as sa
from alembic import op

revision = "0008"
down_revision = "0007"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "skills_skill",
        sa.Column("id", sa.Integer(), nullable=False, autoincrement=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("max_level", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk_skills_skill"),
    )
    op.create_unique_constraint("uq_skills_name", "skills_skill", ["name"])


def downgrade() -> None:
    op.drop_constraint("uq_skills_name", "skills_skill", type_="unique")
    op.drop_table("skills_skill")
