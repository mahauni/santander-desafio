from google import genai

client = genai.Client(api_key="")


def make_company_perfil():
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Explain how AI works in a few words",
    )

    print(response.text)

    return response.text
