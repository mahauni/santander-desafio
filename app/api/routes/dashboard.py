from datetime import datetime
from fastapi import APIRouter, Query

from app.api.deps import SessionDep
from app.api.internal.dashboard import (
    get_all_cnpj_data,
    get_all_transactions_grouped,
    get_transaction_type_counts,
    get_transactions_json,
    get_value_per_types,
)
from app.models import (
    PaginatedTransactions,
    TransactionsChart,
    TransactionsCount,
    TransactionsSummary,
    CnpjList,
)


router = APIRouter(tags=["dashboard"], prefix="/dashboard")


# this is the sittiest thing ive ever build
# need maybe to send the array with the data by date, and then send only that
@router.get("/transactions")
def get_transactions(
    session: SessionDep,
    start_date: str = Query("2025-05-01", description="start date for the query"),
    end_date: str = Query("2025-05-31", description="end date for the query"),
    page: int = Query(0, ge=0),
    page_size: int = Query(20, ge=0, le=100),
) -> PaginatedTransactions:
    result = get_transactions_json(
        session,
        datetime.strptime(start_date, "%Y-%m-%d").date(),
        datetime.strptime(end_date, "%Y-%m-%d").date(),
        page,
        page_size,
    )

    return result


@router.get("/transactions/type")
def get_value_per_type(
    session: SessionDep,
    start_date: str = Query("2025-05-01", description="start date for the query"),
    end_date: str = Query("2025-05-31", description="end date for the query"),
) -> TransactionsSummary:
    result = get_value_per_types(
        session,
        datetime.strptime(start_date, "%Y-%m-%d").date(),
        datetime.strptime(end_date, "%Y-%m-%d").date(),
    )

    return result


@router.get("/transactions/value-per-month")
def get_transactions_values_per_month(
    session: SessionDep,
    start_date: str = Query("2025-05-01", description="start date for the query"),
    end_date: str = Query("2025-05-31", description="end date for the query"),
) -> TransactionsChart:
    result = get_all_transactions_grouped(
        session,
        datetime.strptime(start_date, "%Y-%m-%d").date(),
        datetime.strptime(end_date, "%Y-%m-%d").date(),
    )

    return TransactionsChart(dates=result)


@router.get("/transactions/count-per-month")
def get_transactions_count_per_month(
    session: SessionDep,
    start_date: str = Query("2025-05-01", description="start date for the query"),
    end_date: str = Query("2025-05-31", description="end date for the query"),
) -> TransactionsCount:
    result = get_transaction_type_counts(
        session,
        datetime.strptime(start_date, "%Y-%m-%d").date(),
        datetime.strptime(end_date, "%Y-%m-%d").date(),
    )

    return TransactionsCount(dates=result)


@router.get("/cnpj")
def get_all_cnpj(session: SessionDep) -> CnpjList:
    cnpj = get_all_cnpj_data(session)

    return CnpjList(cnpjs=cnpj)
