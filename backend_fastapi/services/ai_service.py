import openai
import os
from backend_fastapi.services.xml_parser_service import parse_nfe_xml
from backend_fastapi.services.tax_service import calculate_tax
from backend_fastapi.dependencies import get_current_user
from backend_fastapi import database
from backend_fastapi.dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def gerar_resposta(texto):
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": texto}]
    )
    return response.choices[0].message["content"]
