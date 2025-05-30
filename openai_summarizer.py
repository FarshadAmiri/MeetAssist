# openai_summarizer.py

from openai import OpenAI

def chat_with_gpt(transcript, api_key, base_url="https://api.metisai.ir/openai/v1"):
    client = OpenAI(api_key=api_key, base_url=base_url)

    system_prompt = (
        "You are a professional meeting assistant. "
        "Summarize this meeting briefly (under 2000 words) with a structured format. "
        "Highlight the key decisions, discussion points, and tasks assigned. "
        "Mention each task along with the person assigned to it clearly."
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": transcript}
        ]
    )
    return response.choices[0].message.content
