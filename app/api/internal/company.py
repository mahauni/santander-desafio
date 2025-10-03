from google import genai
from google.genai import types
import pandas as pd


def get_data():
    return pd.read_csv(
        "data_company.csv", comment="#", sep=", ", header=0, engine="python"
    )


def make_company_perfil(gemini: genai.Client, cnpj: str) -> str | None:
    df = get_data()

    company_data = df[df["id"] == cnpj]

    if company_data.empty:
        raise Exception("No data found")

    prompt = company_data.to_string()

    prompt += "\nCom base nesses dados, qual e o momento de vida da empresa em inicio, expansao, maturidade e declinio"

    response = gemini.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction="Voce e um analista de empresas tentando descobrir o que elas sao",
            stop_sequences=["\n"],
        ),
    )

    return response.text


def get_all_cnpj_data():
    df = get_data()

    unique_cnpjs: set[str] = set(df["id"])

    return sorted(unique_cnpjs)
