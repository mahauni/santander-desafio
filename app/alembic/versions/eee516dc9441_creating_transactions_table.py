"""Creating transactions table

Revision ID: eee516dc9441
Revises:
Create Date: 2025-10-03 22:47:36.491536

"""

import logging
import os
from typing import Sequence, Union
from sqlalchemy import Table, MetaData
from sqlalchemy.sql import insert
import csv

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "eee516dc9441"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "transactions",
        sa.Column("id", sa.INTEGER(), primary_key=True, autoincrement=True),
        sa.Column("id_pgto", sa.VARCHAR(200), nullable=False),
        sa.Column("id_rcbe", sa.VARCHAR(200), nullable=False),
        sa.Column("vl", sa.VARCHAR(200), nullable=False),
        sa.Column("ds_tran", sa.VARCHAR(200), nullable=False),
        sa.Column("dt_refe", sa.DATE(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False
        ),
        # sa.PrimaryKeyConstraint("id")
    )

    csv_file_path = "./data/data_transactions.csv"

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
                    "id_pgto": row["id_pgto"],
                    "id_rcbe": row["id_rcbe"],
                    "vl": row["vl"],
                    "ds_tran": row["ds_tran"],
                    "dt_refe": row["dt_refe"],
                    # id and created_at will be auto-generated
                }
            )

        # Bulk insert
        if data_to_insert:
            # Create metadata and table reference for insert
            metadata = MetaData()
            transactions = Table(
                "transactions",
                metadata,
                sa.Column("id_pgto", sa.String()),
                sa.Column("id_rcbe", sa.String()),
                sa.Column("vl", sa.String()),
                sa.Column("ds_tran", sa.String()),
                sa.Column("dt_refe", sa.Date()),
            )

            conn.execute(insert(transactions), data_to_insert)
            logger.info(f"Loaded {len(data_to_insert)} rows from {csv_file_path}")
        else:
            logger.info(f"Warning: No data found in {csv_file_path}")


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("transactions")
