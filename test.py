from dotenv import load_dotenv
import os

print("📂 Current Working Directory:", os.getcwd())
print("📁 Files Present:", os.listdir())

load_dotenv()

key = os.getenv("OPENROUTER_API_KEY")

if key:
    print("✅ API Key loaded successfully:", key[:8] + "...")
else:
    print("❌ API Key not loaded! Check your .env file.")


