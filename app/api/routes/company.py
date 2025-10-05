from fastapi import APIRouter, HTTPException, Query, status

from app.api.deps import GeminiDep, SessionDep
from app.api.internal.company import get_all_cnpj_data, make_company_perfil
from app.models import CnpjList, MomentResponse


router = APIRouter(tags=["company"], prefix="/company")


@router.get("/perfil")
def get_company_perfil(
    gemini: GeminiDep,
    session: SessionDep,
    cnpj: str = Query(
        ..., description="O cnpj principal utilizado para a pesquisa dos dados"
    ),
) -> MomentResponse:
    try:
        result = make_company_perfil(gemini, session, cnpj)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return result


@router.get("/cnpj")
def get_all_cnpj(session: SessionDep) -> CnpjList:
    result = get_all_cnpj_data(session)

    return CnpjList(cnpjs=result)
