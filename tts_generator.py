from openai import OpenAI
import uuid

client = OpenAI(
    api_key=""
)

def generate_expert_tts(summary: str, explanation: str, gpt_prompt_func) -> str:
    """
    summary: 코드에 대한 전체 요약
    explanation: GPT가 생성한 상세 설명
    gpt_prompt_func: GPT 텍스트 생성 함수 (예: query_gpt)

    Returns: 생성된 mp3 파일 경로 (str)
    """
    tts_prompt = f"""
아래 코드는 사용자가 작성한 파이썬 코드에 대한 해설입니다.

요약: {summary}

해설: {explanation}

이제 당신은 전문가입니다.
이 코드의 전체 목적, 핵심 개념, 꼭 명심해야 할 점을 3~4문장으로 설명해주세요.
설명은 전문적인 말투로 해주세요.
"""

    # GPT로 TTS용 요약 텍스트 생성
    tts_text = gpt_prompt_func(tts_prompt, temperature=0.4)

    # OpenAI TTS 호출
    audio_response = client.audio.speech.create(
        model="tts-1",
        voice="shimmer",
        input=tts_text
    )

    # 파일로 저장
    audio_path = f"expert_summary_{uuid.uuid4().hex}.mp3"
    audio_response.stream_to_file(audio_path)

    return audio_path