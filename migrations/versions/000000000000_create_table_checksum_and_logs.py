"""Create table checksum_and_logs
Revision ID: c84467455016
Revises:
Create Date: 2020-02-14 20:31:39.065035
"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "000000000000"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "checksums",
        sa.Column("data_resource", sa.String(), nullable=False),
        sa.Column("model_checksum", sa.String(), nullable=False),
        sa.Column("date_modified", sa.DateTime(), nullable=True),
        sa.Column(
            "descriptor_json", postgresql.JSONB(astext_type=sa.Text()), nullable=True
        ),
        sa.PrimaryKeyConstraint("data_resource"),
    )
    op.create_table(
        "logs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("logger", sa.String(), nullable=True),
        sa.Column("level", sa.String(), nullable=True),
        sa.Column("trace", sa.String(), nullable=True),
        sa.Column("msg", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "migrations",
        sa.Column("file_name", sa.String(), nullable=False),
        sa.Column("file_blob", sa.LargeBinary(), nullable=False),
        sa.PrimaryKeyConstraint("file_name"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("logs")
    op.drop_table("checksums")
    # ### end Alembic commands ###
