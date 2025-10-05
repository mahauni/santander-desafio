import uuid
import json

from fastapi import APIRouter, Query, Response
from fastapi.responses import FileResponse, JSONResponse

from app.api.internal.analysis import impact_on_remove, make_analysis
from app.api.deps import SessionDep


router = APIRouter(tags=["analysis"], prefix="/analysis")


@router.get("/image", response_class=FileResponse)
def analysis_image():
    return FileResponse("./image/graph.gv.jpg")


@router.get("/make", response_class=JSONResponse)
def get_analysis(
    session: SessionDep,
    cnpj: str = Query(
        "CNPJ_01000", description="O cnpj principal utilizado como node principal"
    ),
):
    result = make_analysis(session, cnpj)

    return Response(content=json.dumps(result), media_type="application/json")


@router.get("/delete/{id}", response_class=JSONResponse)
def remove_cnpj(session: SessionDep, id: uuid.UUID):
    result = impact_on_remove(session, id.int)

    return Response(content=result, media_type="application/json")
