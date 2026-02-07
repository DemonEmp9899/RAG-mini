import os
from dotenv import load_dotenv
from openai import OpenAI

from src.qa.prompts import PROMPT_V2

# Load env only here
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY not found in .env")

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url=OPENROUTER_BASE_URL
)

MODEL_NAME = "openai/gpt-3.5-turbo"  # or another OpenRouter-supported model


def generate_answer(context: str, question: str) -> str:
    prompt = PROMPT_V2.format(
        context=context,
        question=question
    )

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.0
    )

    return response.choices[0].message.content.strip()
