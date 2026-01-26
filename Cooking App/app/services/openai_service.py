import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

env_path = Path(__file__).parent.parent.parent / ".env"
if not env_path.exists():
    # Fallback: try current working directory
    env_path = Path.cwd() / ".env"
load_dotenv(env_path)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL")

client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)

SYSTEM_PROMPT = "You are a cooking assistant that talks like a pirate."
USER_PROMPT = "What is the best cooking recipe in the world?"

TEMPERATURE = 0.7
MODEL = os.environ.get("OPENAI_MODEL")


completion = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": USER_PROMPT},
    ],
    temperature=TEMPERATURE,
)

print(completion.choices[0].message.content.strip())
