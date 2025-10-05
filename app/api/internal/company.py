from typing import cast
import pandas as pd
from google import genai

from app.models import MomentResponse


def get_data():
    return pd.read_csv(
        "data_company.csv", comment="#", sep=", ", header=0, engine="python"
    )


def make_company_perfil(gemini: genai.Client, cnpj: str) -> MomentResponse:
    df = get_data()

    company_data = df[df["id"] == cnpj]

    if company_data.empty:
        raise Exception("No data found")

    chat = gemini.chats.create(
        model="gemini-2.5-flash",
        config=genai.types.GenerateContentConfig(
            system_instruction="Voce e um analista e voce esta tendano descobrir em qual momento da empresa ela esta, nao coloque voce na resposta",
            stop_sequences=["\n"],
        ),
    )

    saldo = company_data["vl_sldo"].tolist()
    faturamento = company_data["vl_fatu"].tolist()
    data = company_data["dt_refe"].tolist()

    prompt = company_data.to_string()

    prompt += "\nCom base nesses dados, qual e o momento de vida da empresa em inicio, expansao, maturidade e declinio"

    moment = chat.send_message(prompt)

    prompt = "descreva o porque a voce chegou a essa conclusao, falando sobre o porque com alguns dados"

    problem = chat.send_message(prompt)

    return MomentResponse(
        moment=cast(str, moment.text),
        problem=cast(str, problem.text),
        saldo=saldo,
        faturamento=faturamento,
        data=data,
    )


def get_all_cnpj_data():
    df = get_data()

    unique_cnpjs: set[str] = set(df["id"])

    return sorted(unique_cnpjs)
