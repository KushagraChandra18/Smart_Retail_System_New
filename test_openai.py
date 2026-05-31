from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
import os

print("KEY FOUND:", bool(os.getenv("AZURE_OPENAI_API_KEY")))

client = OpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url=os.getenv("AZURE_OPENAI_ENDPOINT")
)

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": "Hello"
        }
    ]
)

print(response.choices[0].message.content)