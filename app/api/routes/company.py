import json

from fastapi import APIRouter, HTTPException, Query, Response, status
from fastapi.responses import JSONResponse

from app.api.deps import GeminiDep
from app.api.internal.company import get_all_cnpj_data, make_company_perfil
from app.models import CnpjList


router = APIRouter(tags=["company"], prefix="/company")


@router.get("/perfil", response_class=JSONResponse)
def get_company_perfil(
    gemini: GeminiDep,
    cnpj: str = Query(
        ..., description="O cnpj principal utilizado para a pesquisa dos dados"
    ),
):
    try:
        result = make_company_perfil(gemini, cnpj)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return Response(content=json.dumps(result), media_type="application/json")


@router.get("/cnpj")
def get_all_cnpj() -> CnpjList:
    result = get_all_cnpj_data()

    return CnpjList(cnpjs=result)
