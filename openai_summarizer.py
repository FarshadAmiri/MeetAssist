# openai_summarizer.py

from openai import OpenAI
import requests

def mom_summarizer(transcript, api_key, base_url="https://api.metisai.ir/openai/v1"):
    client = OpenAI(api_key=api_key, base_url=base_url)

    system_prompt = (
        """You are a meeting assistant tasked with generating a structured summary (Minutes of Meeting - MoM).

            The input may include retrieved notes or summaries from prior meetings. If applicable, refer to previous tasks or conversations and show continuity. For example, if someone was assigned a task earlier and gives an update now, reflect that.

            Generate the MoM in this structure:
            1. Title
            2. Date
            3. Participants
            4. Discussion Summary
            5. Decisions Made
            6. Tasks and Action Items (with responsible people and deadlines)
            7. Follow-ups

            Make the summary clear, concise, and professional."""
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": transcript}
        ]
    )
    return response.choices[0].message.content


def session_top_subjects(transcript, api_key, base_url="https://api.metisai.ir/openai/v1"):
    client = OpenAI(api_key=api_key, base_url=base_url)

    system_prompt = (
        """You are a meeting analysis assistant.

            Given a transcript of a meeting, your task is to extract:
            1. Top recurring or important terms/concepts.
            2. Tasks or action items mentioned (along with responsible persons if available).
            3. Any follow-ups, open issues, or deadlines mentioned.

            Provide the output as a structured JSON like:
            {
            "important_terms": ["term1", "term2", ...],
            "tasks": [
                {"person": "Alice", "task": "Prepare project report", "due": "next week"},
                ...
            ],
            "open_issues": ["Unclear timeline for budget approval", ...]
            }"""
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": transcript}
        ]
    )
    return response.choices[0].message.content



def MOMWriterBot(api_key, bot_id, user_message):
    url = "https://api.metisai.ir/api/v1/chat/session"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "botId": bot_id,
        "user": None,
        "initialMessages": [
            {
                "type": "USER",
                "content": user_message
            }
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code != 200:
        print("❌ Metis API Error:")
        print(f"Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")
        raise Exception("Failed to get response from Metis API.")

    return response.json()
