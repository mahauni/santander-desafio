from typing import Optional
import uuid
import json

from fastapi import APIRouter, Query, Response
from fastapi.responses import FileResponse, JSONResponse

from app.api.internal.analysis import impact_on_remove, make_analysis


router = APIRouter(tags=["analysis"], prefix="/analysis")


@router.get("/image", response_class=FileResponse)
def analysis_image():
    return FileResponse("./image/graph.gv.jpg")


@router.get("/make", response_class=JSONResponse)
def get_analysis(
    cnpj: Optional[str] = Query(
        None, description="O cnpj principal utilizado como node principal"
    ),
):
    if cnpj and cnpj != "CNPJ_00001":
        result = make_analysis(True, cnpj)
    else:
        result = make_analysis()

    return Response(content=json.dumps(result), media_type="application/json")


@router.get("/delete/{id}", response_class=JSONResponse)
def remove_cnpj(id: uuid.UUID):
    result = impact_on_remove(id.int)

    return Response(content=result, media_type="application/json")
