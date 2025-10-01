import json

from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse


router = APIRouter(tags=["company"], prefix="/company")


@router.get("/perfil", response_class=JSONResponse)
def get_company_perfil():
    result = ""

    return Response(content=json.dumps(result), media_type="application/json")
