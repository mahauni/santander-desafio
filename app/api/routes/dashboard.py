from fastapi import APIRouter, Response

from app.api.internal.dashboard import get_transactions_json, get_value_per_types


router = APIRouter(tags=["dashboard"], prefix="/dashboard")


@router.get("/transactions")
def get_transactions():
    json = get_transactions_json()

    return Response(content=json, media_type="application/json")


@router.get("/transactions/type")
def get_value_per_type():
    json = get_value_per_types()

    return Response(content=json, media_type="application/json")
