from openai import OpenAI
import os

openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def translate_to_korean(text: str) -> str:
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"Translate this to natural Korean:\n\n{text}"}],
        temperature=0.1,
    )
    return response.choices[0].message.content.strip()