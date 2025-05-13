import openai

openai.api_key = ""

def query_gpt(prompt: str, model: str="gpt-3.5-turbo", temperature: float=0.3)->str:
    try:
        response = openai.ChatCompletion.create(
            model=model, 
            messages=[
                {"role": "system", "content": "당신은 친절하고 매우 전문적인 파이썬 튜터입니다."},
                {"role": "user", "content": prompt}
            ], 
            temperature=temperature,
            max_tokens=1024
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print("OpenAI API 호출 중 오류", e)
        return None

def build_gpt_prompt(code: str, line_comments: str, mode: str) -> str :
    '''
    Args:
        code: 사용자가 입력한 코드 (str)
        line_comments: StarCoder2가 생성한 라인별 주석(str)
        summary: StarCoder2가 생성한 전체 요약 (str)
        mode: "bigginer", "intermediate", "advanced" 중 하나
    '''

    prompt_templates = {
        "beginner": f"""
당신은 초보자를 위한 파이썬 튜터입니다.
아래는 사용자가 입력한 코드입니다.

{code}

그리고 아래는 코드에 대한 라인별 주석과 전체 요약입니다.

라인별 주석:
{line_comments}

전체 요약:
{summary}

이 내용을 바탕으로,
1. 이 코드에서 사용된 **기초 문법/개념**을 설명해주세요.
2. 각 부분이 무슨 의미인지 아주 쉽게 풀어서 설명해주세요.
3. 사용자가 앞으로 **어떤 부분부터 공부하면 좋을지** 우선순위를 정해서 알려주세요.

※ 모든 설명은 한국어로 해주세요. 초등학생도 이해할 수 있게 설명하는 것이 목표입니다.
""",
        "intermediate": f"""
당신은 중급 개발자를 위한 파이썬 튜터입니다.
아래는 사용자가 입력한 코드입니다.

{code}

그리고 아래는 코드에 대한 라인별 주석과 전체 요약입니다.

라인별 주석:
{line_comments}

전체 요약:
{summary}

이 내용을 바탕으로,
1. 코드의 전체적인 **논리 흐름**을 설명해주세요.
2. 코드에서 **개선할 수 있는 부분**이나 **더 깔끔한 구조**가 있다면 알려주세요.
3. 더 좋은 방식이 있다면 예시를 들어 설명해주세요.

※ 설명은 한국어로 해주시고, 실제 개발에서 참고할 수 있도록 현실적인 팁을 포함해주세요.
""",
        "advanced": f"""
당신은 고급 개발자를 위한 파이썬 멘토입니다.
아래는 사용자가 입력한 코드입니다.

{code}

그리고 아래는 코드에 대한 라인별 주석과 전체 요약입니다.

라인별 주석:
{line_comments}

전체 요약:
{summary}

이 내용을 바탕으로,
1. 코드의 성능과 구조 측면에서 분석해주세요.
2. 이 구조나 접근 방식이 **다른 문제에 어떻게 응용될 수 있는지** 알려주세요.
3. **코드 리팩토링, 추상화, 패턴 적용** 등의 고급 아이디어가 있다면 제시해주세요.

※ 설명은 한국어로 작성하고, 전문가 수준의 인사이트를 제공해주세요.
"""
    }
    return prompt_templetes[mode].strip()