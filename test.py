from assembly_transcriber import assembly_stt_diarization
from config import *
from openai_summarizer import MOMWriterBot

# assembly_stt_diarization(ASSEMBLY_API_KEY, 3, r"C:\Users\Sina\Desktop\repo_MeetAssist\output\audio.wav", r"C:\Users\Sina\Desktop\repo_MeetAssist\output\transcript.txt")


# import requests

# def get_all_bots(api_key):
#     url = "https://api.metisai.ir/api/v1/bots/all"
#     headers = {
#         "Authorization": f"Bearer {api_key}",
#         "Content-Type": "application/json"
#     }
#     response = requests.get(url, headers=headers)
#     response.raise_for_status()
#     return response.json()  # List of bots


# print(get_all_bots(METIS_API_KEY))


res = MOMWriterBot(METIS_API_KEY, MOMWriterBot_ID, "Hey how you doing?")
print(res)