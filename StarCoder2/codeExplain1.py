import requests 
import time

API_URL = "https://api-inference.huggingface.co/models/bigcode/starcoder2-7b"
HF_TOKEN = ""

'''headers는 HTTP 요청에 포함되는 추가 정보(메타데이터)를 담는 딕셔너리. 
Authorization 헤더는 HuggingFace API에 접근할 때 토큰 인증용. '''
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

# 단일 요청(여기서 prompt는 입력 prompt)
def query_huggingface(prompt:str, max_new_tokens: int=128, temperature: float=0.2):
    payload = {
        "inputs":prompt, 
        "parameters":{
            "max_new_tokens":max_new_tokens, # 새로 생성할 최대 토큰 수. 너무 작으면 문장이 잘리고 너무 크면 비용 낭비 -> 요약은 256, 설명은 128 정도 적절. 
            "temperature":temperature, # 생성의 무작위성 정도. (0= 완전 결정적, 1 = 매우 다양) 일반적으로 0.2 ~ 0.7 사이에서 많이 조절절
            "return_full_text":False # 입력 프롬프트까지 포함해서 반환할지 여부
        }
    }
    # HuggingFace는 단지 API endpoint를 열어주는 서버일 뿐, 그걸 호출하는 건 requests가 함.
    response = requests.post(API_URL, headers=headers, json=payload) # Python의 requests 라이브러리에서 제공. HTTP POST 요청을 보냄냄
    if response.status_code == 200: # 서버가 요청에 대해 무슨 상태코드를 반환했는지 알려주는 값. 200은 웹에서 "성공"을 의미하는 표준 HTTP 상태 코드드
        return response.json()[0]['generated_text']
    else:
        print("Error:", response.status_code, response.text)
        return None

# 줄별 주석 생성
def generate_line_comments(code: str) -> list:
    comments = []
    for line in code.split('\n'):
        if not line.strip(): # 빈줄은 건너뛰기
            comments.append('')
            continue
        prompt = f"# Please explain the following code in english. \n{line}"
        explanation = query_huggingface(prompt)
        time.sleep(1) # HuggingFace  API 호출 간 간격
        comments.append(f"{line} #{explanation.strip() if explanation else '설명 실패'} ")
    return comments

# 전체 요약 생성
def generate_summary(code: str) -> str : 
    prompt = f"# Analyze the following Python code and summarize its overall structure. \n{code} "
    return query_huggingface(prompt, max_new_tokens=256)



    