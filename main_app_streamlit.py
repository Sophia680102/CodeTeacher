import streamlit as st
from PIL import Image

# ------------------------------
# 가상의 분석 함수들 (나중에 실제 코드로 대체)
# ------------------------------
def fake_code_summary(code: str) -> str:
    return "이 코드는 주어진 숫자의 팩토리얼을 재귀적으로 계산합니다."

def fake_code_with_comments(code: str) -> str:
    return """def factorial(n):  # n의 팩토리얼을 계산하는 함수입니다.
    if n == 0:  # n이 0이면 1을 반환합니다.
        return 1
    return n * factorial(n-1)  # n과 (n-1)의 팩토리얼을 곱합니다.
"""

def load_fake_flowchart_image() -> Image.Image:
    # 실제 흐름도 생성 시에는 Graphviz로 생성된 PNG 파일을 여기에 불러오면 됩니다.
    return Image.open("sample_flowchart.png")  # 예시 이미지 파일 경로

# ------------------------------
# Streamlit 웹앱 시작
# ------------------------------
st.set_page_config(page_title="Code Teacher", layout="wide")
st.title("🧑‍🏫 Code Teacher: AI 코드 설명 도우미")

# 좌측: 코드 입력창
st.subheader("1. 코드 입력")
user_code = st.text_area("아래에 Python 코드를 입력하세요:", height=300)

# 분석 버튼
if st.button("🔍 분석하기"):
    if not user_code.strip():
        st.warning("코드를 입력해주세요!")
    else:
        # 코드 요약 출력
        st.subheader("2. 코드 요약 (한글 설명)")
        summary = fake_code_summary(user_code)
        st.success(summary)

        # 주석 포함된 코드 출력
        st.subheader("3. 코드에 AI 주석 추가")
        code_with_comments = fake_code_with_comments(user_code)
        st.code(code_with_comments, language="python")

        # 흐름도 이미지 출력
        st.subheader("4. 코드 흐름 (시각화)")
        try:
            flow_img = load_fake_flowchart_image()
            st.image(flow_img, caption="코드 흐름도", use_column_width=True)
        except FileNotFoundError:
            st.error("(예시) 흐름도 이미지 파일을 찾을 수 없습니다.")

else:
    st.info("좌측에 코드를 입력한 후 \"분석하기\" 버튼을 눌러주세요.")
