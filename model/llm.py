import google.generativeai as genai
from openai import OpenAI
from model.constants import GEMINI_API_KEY, GPT_API_KEY, MODEL

genai.configure(api_key=GEMINI_API_KEY)

def make_gemini_call(PROMPT):
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(PROMPT).text
    return response.strip()

def make_gpt_call(PROMPT):
    client = OpenAI(api_key=GPT_API_KEY)
    completion = client.chat.completions.create(
        model=MODEL,
        store=True,
        messages=[
            {"role": "user", "content": PROMPT}
        ]
    )
    response = completion.choices[0].message.content
    return response.strip()