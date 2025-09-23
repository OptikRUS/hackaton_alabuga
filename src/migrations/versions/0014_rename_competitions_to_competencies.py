from alembic import op

revision = "0014"
down_revision = "0013"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.rename_table(
        "competitions_competition",
        "competencies_competency",
    )

    op.rename_table(
        "competitions_competitions_skills",
        "competencies_competencies_skills",
    )
    op.rename_table(
        "ranks_competitions_requirements",
        "ranks_competencies_requirements",
    )
    op.rename_table(
        "missions_competitions_rewards",
        "missions_competencies_rewards",
    )

    op.alter_column(
        "competencies_competencies_skills",
        "competition_id",
        new_column_name="competency_id",
    )
    op.alter_column(
        "ranks_competencies_requirements",
        "competition_id",
        new_column_name="competency_id",
    )
    op.alter_column(
        "missions_competencies_rewards",
        "competition_id",
        new_column_name="competency_id",
    )

    op.drop_constraint(
        "uq_competitions_name",
        "competencies_competency",
        type_="unique",
    )
    op.create_unique_constraint(
        "uq_competencies_name",
        "competencies_competency",
        ["name"],
    )

    op.drop_constraint(
        "pk_competitions_competitions_skills",
        "competencies_competencies_skills",
        type_="primary",
    )
    op.create_primary_key(
        "pk_competencies_competencies_skills",
        "competencies_competencies_skills",
        ["competency_id", "skill_id"],
    )

    op.drop_constraint(
        "pk_ranks_competitions_requirements",
        "ranks_competencies_requirements",
        type_="primary",
    )
    op.create_primary_key(
        "pk_ranks_competencies_requirements",
        "ranks_competencies_requirements",
        ["rank_id", "competency_id"],
    )

    op.drop_constraint(
        "pk_missions_competitions_rewards",
        "missions_competencies_rewards",
        type_="primary",
    )
    op.create_primary_key(
        "pk_missions_competencies_rewards",
        "missions_competencies_rewards",
        ["mission_id", "competency_id"],
    )


def downgrade() -> None:
    op.alter_column(
        "missions_competencies_rewards",
        "competency_id",
        new_column_name="competition_id",
    )
    op.alter_column(
        "ranks_competencies_requirements",
        "competency_id",
        new_column_name="competition_id",
    )
    op.alter_column(
        "competencies_competencies_skills",
        "competency_id",
        new_column_name="competition_id",
    )

    op.drop_constraint(
        "pk_missions_competencies_rewards",
        "missions_competencies_rewards",
        type_="primary",
    )
    op.create_primary_key(
        "pk_missions_competitions_rewards",
        "missions_competencies_rewards",
        ["mission_id", "competition_id"],
    )

    op.drop_constraint(
        "pk_ranks_competencies_requirements",
        "ranks_competencies_requirements",
        type_="primary",
    )
    op.create_primary_key(
        "pk_ranks_competitions_requirements",
        "ranks_competencies_requirements",
        ["rank_id", "competition_id"],
    )

    op.drop_constraint(
        "pk_competencies_competencies_skills",
        "competencies_competencies_skills",
        type_="primary",
    )
    op.create_primary_key(
        "pk_competitions_competitions_skills",
        "competencies_competencies_skills",
        ["competition_id", "skill_id"],
    )

    op.drop_constraint(
        "uq_competencies_name",
        "competencies_competency",
        type_="unique",
    )
    op.create_unique_constraint(
        "uq_competitions_name",
        "competencies_competency",
        ["name"],
    )

    op.rename_table(
        "missions_competencies_rewards",
        "missions_competitions_rewards",
    )
    op.rename_table(
        "ranks_competencies_requirements",
        "ranks_competitions_requirements",
    )
    op.rename_table(
        "competencies_competencies_skills",
        "competitions_competitions_skills",
    )

    op.rename_table("competencies_competency", "competitions_competition")
