from openai import OpenAI
import os

openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_gpt_explanation(code: str, comments: dict, style: str = "학생용") -> str:
    style_prompt = {
        "학생용": "초보 학생도 쉽게 이해할 수 있게 설명해줘.",
        "개발자용": "기술적으로 정확하게 설명해줘.",
        "튜터 스타일": "튜터가 학생에게 질문과 답변을 주듯이 설명해줘."
    }

    prompt = f"아래는 Python 코드와 각 줄별 주석이다.\n\n코드:\n{code}\n\n주석:\n{comments}\n\n{style_prompt[style]}"
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
    )
    return response.choices[0].message.content.strip()