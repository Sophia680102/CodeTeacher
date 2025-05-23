import streamlit as st
from codeExplain1 import generate_line_comments, generate_summary
from codeExplain2_gpt import build_gpt_prompt, query_gpt
from make_pseudo import generate_pseudocode_and_mermaid

st.set_page_config(page_title="AI 코드 분석기", layout="wide")
st.title("CodeTeacher: 생성형 AI 기반 코드 분석 도우미")
st.markdown("StarCoder2 + GPT-3.5를 활용한 파이썬 코드 해석 도우미")


user_code = st.text_area("🔤 분석할 파이썬 코드를 입력하세요:", height=300, placeholder="여기에 코드를 입력하세요...")


mode = st.radio("학습 수준을 선택하세요:", ["초보자", "중급자", "고급자"], horizontal=True)


mode_key = {
    "초보자": "beginner",
    "중급자": "intermediate",
    "고급자": "advanced"
}[mode]

if st.button("🔍 코드 분석 시작"):
    if not user_code.strip():
        st.warning("Python 코드를 입력해주세요!")
    else:
        with st.spinner("StarCoder2로 코드 분석 중..."):
            summary = generate_summary(user_code)
            line_comments = "\n".join(generate_line_comments(user_code))

        with st.spinner("GPT-3.5로 해설 생성 중..."):
            gpt_prompt = build_gpt_prompt(user_code, line_comments, summary, mode_key)
            gpt_output = query_gpt(gpt_prompt)
            pseudocode, mermaid_code = generate_pseudocode_and_mermaid(user_code)

        st.subheader("📝 StarCoder2 라인별 주석")
        st.code(line_comments, language="python")

        st.subheader("🧩 StarCoder2 전체 요약")
        st.markdown(f"> {summary}")

        st.subheader(f"📖 GPT-3.5 {mode}용 상세 해설")
        st.markdown(gpt_output)

        st.subheader("📄 슈도코드 (Pseudocode)")
        st.code(pseudocode if pseudocode else "(생성 실패)", language="text")
        
        st.subheader("🗺 Mermaid Flowchart 코드")
        st.code(mermaid_code if mermaid_code else "(생성 실패)", language="markdown")
        st.markdown("⚠️ 현재는 Mermaid 렌더링은 코드 형태로만 보여집니다. PNG 출력은 추후 지원 예정입니다.")
 
        st.session_state["gpt_output"] = gpt_output
        st.session_state["line_comments"] = line_comments
        st.session_state["summary"] = summary
        st.session_state["user_code"] = user_code
        st.session_state["pseudocode"] = pseudocode
        st.session_state["mermaid_code"] = mermaid_code