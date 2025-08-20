import os
import openai
import json
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENROUTER_API_KEY")
openai.api_base = "https://openrouter.ai/api/v1"

def generate_quiz(topic, level='medium', num_questions=5):
    prompt = f"""
You are a quiz generator for school students. 
Return ONLY valid JSON (no code fences, no prose). 
Schema:
{{
  "quiz": [
    {{
      "question": "string",
      "options": ["string","string","string","string"],  // exactly 4
      "correct_index": 0                                  // 0..3
    }}
  ]
}}

Rules:
- Make {num_questions} MCQs on "{topic}" at {level} difficulty.
- Keep options short and distinct.
- Do NOT include letters (A/B/C/D) inside options.
- Do NOT include "Answer:" anywhere.
- Output ONLY the JSON object above.
"""

    try:
        resp = openai.ChatCompletion.create(
            model="openai/gpt-3.5-turbo",  # keep your current model; temperature 0 for consistency
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        content = resp["choices"][0]["message"]["content"]
        # Light sanity check that it's JSON
        json.loads(content)
        return content  # raw JSON text
    except Exception as e:
        return f"Error generating quiz: {e}"

import re
import json

def _letter_to_index(letter: str):
    if not letter:
        return None
    l = letter.strip().upper().replace(")", "").replace(".", "")
    return {"A":0,"B":1,"C":2,"D":3}.get(l, None)

def parse_quiz(content):
    questions = []
    if not isinstance(content, str):
        return []

    parts = re.split(r'\n(?=\d+\.)', content)

    for part in parts:
        lines = part.strip().split('\n')
        if len(lines) < 6:
            continue
        try:
            question = lines[0][3:].strip()
            options = [line.strip() for line in lines[1:5]]

            answer_line = lines[5].split("Answer:")[-1].strip()

            # Agar A/B/C/D diya hai
            if answer_line.upper() in ["A", "B", "C", "D"]:
                correct_index = ["A","B","C","D"].index(answer_line.upper())
            else:
                # Agar text diya hai (e.g. "Delhi")
                correct_index = next(
                    (i for i, opt in enumerate(options) if answer_line.lower() in opt.lower()), 
                    -1
                )

            if correct_index == -1:
                continue

            questions.append({
                'question': question,
                'options': options,
                'answer': options[correct_index],
                'correct_index': correct_index   # ✅ add index here
            })
        except Exception:
            continue

    return questions
