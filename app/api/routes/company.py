import json

from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse

from app.api.internal.company import make_company_perfil


router = APIRouter(tags=["company"], prefix="/company")


@router.get("/perfil", response_class=JSONResponse)
def get_company_perfil():
    result = make_company_perfil()

    return Response(content=json.dumps(result), media_type="application/json")
