from datetime import date
from typing import Dict
from sqlmodel import Numeric, Session, text, func, select, cast
from sqlalchemy import Float

from app.models import (
    PaginatedTransactions,
    Transactions,
    TransactionsSummary,
    TransactionsTypeCount,
)


def get_transactions_json(
    session: Session, start_date: date, end_date: date, page: int, page_size: int
) -> PaginatedTransactions:
    offset = page * page_size

    # Query for total count
    count_stmt = select(func.count(Transactions.id)).where(  # type: ignore
        Transactions.dt_refe.between(start_date, end_date)  # type: ignore
    )
    total = session.exec(count_stmt).one()

    stmt = (
        select(Transactions)
        .where(Transactions.dt_refe.between(start_date, end_date))  # type: ignore
        .order_by(Transactions.dt_refe)  # type: ignore
        .offset(offset)
        .limit(page_size)
    )

    result = session.exec(stmt).all()

    return PaginatedTransactions(
        data=result, total=total, page=page, page_size=page_size
    )


def get_value_per_types(
    session: Session, start_date: date, end_date: date
) -> TransactionsSummary:
    # Remove "R$ " and "," using SQL string functions
    clean_value = func.replace(func.replace(Transactions.vl, "R$ ", ""), ",", "")

    # Convert to float
    value_numeric = cast(clean_value, Float)

    stmt = (
        select(
            Transactions.ds_tran.label("type"),  # type: ignore
            func.sum(value_numeric).label("total"),
        )
        .where(Transactions.dt_refe.between(start_date, end_date))  # type: ignore
        .group_by(Transactions.ds_tran)
    )

    result = session.exec(stmt).all()

    # Initialize summary with zeros
    summary = TransactionsSummary()

    # Map the aggregated sums into the class attributes
    for row in result:
        type_lower = row.type.lower()  # type: ignore
        if hasattr(summary, type_lower):
            setattr(summary, type_lower, row.total)  # type: ignore

    return summary


def get_all_cnpj_data(session: Session) -> list[str]:
    query = text(
        """
        SELECT id_pgto AS company_id FROM transactions
        UNION
        SELECT id_rcbe AS company_id FROM transactions
    """
    )

    result = session.exec(query)  # type: ignore
    unique_ids = [row.company_id for row in result]

    return unique_ids


def get_all_transactions_grouped(
    session: Session, start_date: date, end_date: date
) -> Dict[date, TransactionsSummary]:
    """
    Get all transactions grouped by date, with types and totals in arrays.
    Filtered by date range and sorted by date.

    Args:
        session: SQLModel database session
        start_date: Start date of the range (inclusive)
        end_date: End date of the range (inclusive)
    """

    # Query to sum values grouped by date and transaction type
    stmt = (
        select(
            Transactions.dt_refe,  # type: ignore
            Transactions.ds_tran,
            func.sum(
                cast(
                    func.replace(
                        func.replace(func.replace(Transactions.vl, "R$ ", ""), ".", ""),
                        ",",
                        ".",
                    ),
                    Numeric,
                )
            ),
        )  # type: ignore
        .where(Transactions.dt_refe >= start_date)
        .where(Transactions.dt_refe <= end_date)
        .group_by(Transactions.dt_refe, Transactions.ds_tran)
        .order_by(Transactions.dt_refe, Transactions.ds_tran)
    )

    results = session.exec(stmt).all()

    # Group by date with TransactionsSummary for each date
    grouped: Dict[date, TransactionsSummary] = {}

    for row in results:
        dt_refe, ds_tran, total = row

        # Create summary for date if it doesn't exist
        if dt_refe not in grouped:
            grouped[dt_refe] = TransactionsSummary()

        # Map transaction type to corresponding field (case-insensitive)
        field_name = ds_tran.lower()
        if hasattr(grouped[dt_refe], field_name):
            setattr(grouped[dt_refe], field_name, float(total))

    return grouped


def get_transaction_type_counts(
    session: Session, start_date: date, end_date: date
) -> Dict[date, TransactionsTypeCount]:
    stmt = (
        select(Transactions.dt_refe, Transactions.ds_tran, func.count().label("count"))  # type: ignore
        .where(Transactions.dt_refe.between(start_date, end_date))  # type: ignore
        .group_by(Transactions.dt_refe, Transactions.ds_tran)
        .order_by(Transactions.dt_refe)
    )

    result = session.exec(stmt).all()

    data: Dict[date, TransactionsTypeCount] = {}

    for dt_refe, ds_tran, count in result:
        if dt_refe not in data:
            data[dt_refe] = TransactionsTypeCount()

        match ds_tran.upper():
            case "PIX":
                data[dt_refe].pix += count
            case "TED":
                data[dt_refe].ted += count
            case "SISTEMICO":
                data[dt_refe].sistemico += count
            case "BOLETO":
                data[dt_refe].boleto += count

    return data
