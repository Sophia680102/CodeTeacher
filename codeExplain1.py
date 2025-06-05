from openai import OpenAI

client = OpenAI(
    api_key=""
    )  

def query_gpt(prompt: str, temperature: float=0.2, max_tokens: int=256):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a Python code expert."},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
        max_tokens=max_tokens
    )
    return response.choices[0].message.content.strip()

def generate_line_comments(code: str):
    lines = code.split('\n')
    numbered_code = '\n'.join([f"{idx+1}: {line}" for idx, line in enumerate(lines)])
    prompt = f"""
아래 코드에 대하여 각 라인별로 코드의 내용을 해석해주세요요

{numbered_code}

Format:
line_number: comment
"""
    comments_response = query_gpt(prompt, max_tokens=512)
    comments_dict = {}
    for line in comments_response.split('\n'):
        if ': ' in line:
            num, comment = line.split(': ', 1)
            comments_dict[int(num.strip())] = comment.strip()

    result = []
    for idx, line in enumerate(lines, 1):
        comment = comments_dict.get(idx, "No comment generated.")
        result.append(f"{line}  # {comment}")
    return result

def generate_summary(code: str):
    prompt = f"""
아래 전체 파이썬 코드의 목적에 대해 간단하게 요약해주세요.:

{code}
"""
    return query_gpt(prompt, max_tokens=128)