"""Creating companies table

Revision ID: 9cd34ce4e6f7
Revises: eee516dc9441
Create Date: 2025-10-04 09:34:46.493098

"""

import os
import logging
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import Table, MetaData
from sqlalchemy.sql import insert
import csv


# revision identifiers, used by Alembic.
revision: str = "9cd34ce4e6f7"
down_revision: Union[str, Sequence[str], None] = "eee516dc9441"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "companies",
        sa.Column("id", sa.INTEGER(), primary_key=True, autoincrement=True),
        sa.Column("cnpj", sa.VARCHAR(200), nullable=False),
        sa.Column("vl_fatu", sa.VARCHAR(200), nullable=False),
        sa.Column("vl_sldo", sa.VARCHAR(200), nullable=False),
        sa.Column("dt_abrt", sa.DATE(), nullable=False),
        sa.Column("ds_cnae", sa.VARCHAR(200), nullable=False),
        sa.Column("dt_refe", sa.DATE(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False
        ),
        # sa.PrimaryKeyConstraint("id"),
    )

    csv_file_path = "./data/data_companies.csv"

    if not os.path.exists(csv_file_path):
        raise FileNotFoundError(f"CSV file not found at {csv_file_path}")

    # Get connection
    conn = op.get_bind()

    # Read CSV and insert data
    with open(csv_file_path, "r", encoding="utf-8") as f:
        csv_reader = csv.DictReader(f, delimiter=";", skipinitialspace=True)
        data_to_insert = []

        for row in csv_reader:
            # Transform row data as needed
            data_to_insert.append(
                {
                    "cnpj": row["cnpj"],
                    "vl_fatu": row["vl_fatu"],
                    "vl_sldo": row["vl_sldo"],
                    "dt_abrt": row["dt_abrt"],
                    "ds_cnae": row["ds_cnae"],
                    "dt_refe": row["dt_refe"],
                    # id and created_at will be auto-generated
                }
            )

        # Bulk insert
        if data_to_insert:
            # Create metadata and table reference for insert
            metadata = MetaData()
            companies = Table(
                "companies",
                metadata,
                sa.Column("cnpj", sa.String()),
                sa.Column("vl_fatu", sa.String()),
                sa.Column("vl_sldo", sa.String()),
                sa.Column("dt_abrt", sa.Date()),
                sa.Column("ds_cnae", sa.String()),
                sa.Column("dt_refe", sa.Date()),
            )

            conn.execute(insert(companies), data_to_insert)
            logger.info(f"Loaded {len(data_to_insert)} rows from {csv_file_path}")
        else:
            logger.info(f"Warning: No data found in {csv_file_path}")


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("companies")
