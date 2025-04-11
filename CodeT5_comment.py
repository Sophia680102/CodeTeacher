from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODEL_NAME = "Salesforce/codet5p-220m"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

def generate_line_comments(code: str) -> dict:
    lines = code.strip().split('\n')
    comments = {}
    for i, line in enumerate(lines, start=1):
        if line.strip():
            input_ids = tokenizer(f"summarize: {line}", return_tensors="pt").input_ids
            output_ids = model.generate(input_ids, max_length=32, num_beams=2, early_stopping=True)
            comment = tokenizer.decode(output_ids[0], skip_special_tokens=True)
            comments[i] = comment
    return comments