import os
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv("OPENROUTER_API_KEY")  # Secure way
openai.api_base = "https://openrouter.ai/api/v1"

MODEL = "deepseek/deepseek-r1:free"

def get_topic_content(subject, topic, grade_level):
    prompt = f"Explain the topic '{topic}' under subject '{subject}' to a student in class {grade_level} in simple terms with examples."
    
    try:
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful AI tutor that simplifies concepts for school students."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']
    
    except Exception as e:
        return f"❌ Error: {str(e)}"

def generate_quiz(topic, grade_level, num_questions=5):
    prompt = f"Create a {num_questions}-question multiple choice quiz on the topic '{topic}' for class {grade_level} students. Provide 4 options labeled A-D and specify the correct answer (e.g., A, B, C, or D). Return result in structured JSON."

    try:
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are an AI that creates quizzes for students."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']
    
    except Exception as e:
        return f"❌ Error: {str(e)}"



