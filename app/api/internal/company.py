from typing import Dict, List, cast
from google import genai
from sqlmodel import Session, select

from app.models import Companies, MomentResponse


def make_company_perfil(
    gemini: genai.Client, session: Session, cnpj: str
) -> MomentResponse:
    exist = cnpj_exists(session, cnpj)

    if not exist:
        raise Exception("No cnpj found")

    companies_occurence = get_cnpj_occurrences_as_table(session, cnpj)

    chat = gemini.chats.create(
        model="gemini-2.5-flash",
        config=genai.types.GenerateContentConfig(
            system_instruction="Voce e um analista e voce esta tendano descobrir em qual momento da empresa ela esta, nao coloque voce na resposta e placeholders como ** empresa ** ou nome de tabela",
        ),
    )

    financial_data = get_cnpj_financial_data(session, cnpj)

    saldo = [item["saldo"] for item in financial_data]
    faturamento = [item["faturamento"] for item in financial_data]
    data = [item["data"].isoformat() for item in financial_data]

    prompt = companies_occurence

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


def get_cnpj_occurrences_as_table(session: Session, cnpj: str) -> str:
    """
    Get all occurrences of a specific CNPJ and format as a table string.

    Args:
        session: SQLModel database session
        cnpj: The CNPJ to search for

    Returns:
        Formatted string table with all occurrences
    """

    # Query all records for the specified CNPJ
    stmt = select(Companies).where(Companies.cnpj == cnpj).order_by(Companies.dt_refe)  # type: ignore

    results = session.exec(stmt).all()

    if not results:
        return f"No records found for CNPJ: {cnpj}"

    # Build the table string
    lines = []

    # Header
    header = "cnpj, vl_fatu, vl_sldo, dt_abrt, ds_cnae, dt_refe"
    lines.append(header)

    # Data rows
    for company in results:
        row = f"{company.cnpj}, {company.vl_fatu}, {company.vl_sldo}, {company.dt_abrt}, {company.ds_cnae}, {company.dt_refe}"
        lines.append(row)

    # Join all lines with newline
    return "\n".join(lines)


def get_cnpj_financial_data(session: Session, cnpj: str) -> List[Dict]:
    """
    Get financial data (saldo, faturamento, data) for a specific CNPJ.

    Args:
        session: SQLModel database session
        cnpj: The CNPJ to search for

    Returns:
        List of dictionaries with saldo, faturamento, and data
    """

    # Query all records for the specified CNPJ
    stmt = (
        select(Companies.vl_sldo, Companies.vl_fatu, Companies.dt_refe)  # type: ignore
        .where(Companies.cnpj == cnpj)
        .order_by(Companies.dt_refe)
    )

    results = session.exec(stmt).all()

    # Format as list of dictionaries
    financial_data = [
        {"saldo": row[0], "faturamento": row[1], "data": row[2]} for row in results
    ]

    return financial_data


def cnpj_exists(session: Session, cnpj: str) -> bool:
    """
    Check if a CNPJ exists in the database.

    Args:
        session: SQLModel database session
        cnpj: The CNPJ to check

    Returns:
        True if CNPJ exists, False otherwise
    """

    stmt = select(Companies).where(Companies.cnpj == cnpj).limit(1)
    result = session.exec(stmt).first()

    return result is not None


def get_all_cnpj_data(session: Session) -> list[str]:
    """
    Get all unique CNPJs from the database.
    Handles duplicates by returning only distinct values.

    Returns:
        List of unique CNPJ strings
    """

    stmt = select(Companies.cnpj).distinct()

    results = session.exec(stmt).all()

    return list(results)
