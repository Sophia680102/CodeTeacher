import openai
import re

openai.api_key = ""

# GPT-3.5를 통해 슈도코드 생성
def generate_pseudocode(code: str) -> str:
    prompt = f"""
    아래의 파이썬 코드를 언어 독립적인 슈도코드(pseudocode)로 변환해줘.
    - 각 줄의 기능이 잘 드러나게 요약할 것
    - 들여쓰기 및 조건/반복문 구조가 명확히 보이게 할 것
    - 불필요한 설명 없이 코드 로직에 집중할 것

    코드:
    {code}
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "당신은 슈도코드 생성기입니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1024
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print("슈도코드 생성 오류:", e)
        return None

# 간단한 슈도코드를 기반으로 Mermaid 흐름도 생성 (flowchart)
def pseudocode_to_mermaid(pseudocode: str) -> str:
    lines = pseudocode.split("\n")
    mermaid_lines = ["graph TD"]

    prev_node = None
    node_count = 1
    for line in lines:
        clean_line = line.strip()
        if not clean_line:
            continue
        node_id = f"N{node_count}"
        mermaid_lines.append(f"    {node_id}[{clean_line}]")
        if prev_node:
            mermaid_lines.append(f"    {prev_node} --> {node_id}")
        prev_node = node_id
        node_count += 1

    return "\n".join(mermaid_lines)

# 통합 함수
def generate_pseudocode_and_mermaid(code: str) -> tuple[str, str]:
    pseudo = generate_pseudocode(code)
    if not pseudo:
        return None, None
    mermaid = pseudocode_to_mermaid(pseudo)
    return pseudo, mermaid