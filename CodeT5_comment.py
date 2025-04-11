from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# CodeT5+ 모델 로딩
MODEL_NAME = "Salesforce/codet5p-220m"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

def generate_summary(code: str) -> str:
    """
    CodeT5+를 사용하여 전체 코드에 대한 간단한 요약(영어)을 반환
    """
    prompt = f"summarize: {code.strip()}"
    input_ids = tokenizer(prompt, return_tensors="pt", truncation=True).input_ids
    summary_ids = model.generate(input_ids, max_length=64, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

def generate_line_comments(code: str) -> dict:
    """
    각 코드 라인에 대한 간단한 주석을 CodeT5+로 생성 (영어)
    반환값: {line_number: comment}
    """
    line_comments = {}
    code_lines = code.strip().split('\n')
    for idx, line in enumerate(code_lines):
        if not line.strip():
            continue  # 빈 줄은 건너뜀
        prompt = f"summarize: {line.strip()}"
        input_ids = tokenizer(prompt, return_tensors="pt", truncation=True).input_ids
        output_ids = model.generate(input_ids, max_length=32, num_beams=4, early_stopping=True)
        comment = tokenizer.decode(output_ids[0], skip_special_tokens=True)
        line_comments[idx] = comment
    return line_comments