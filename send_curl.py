# rag_uploader.py (or a separate module if you'd like)

import requests
from config import METIS_API_KEY 

def get_all_corpora(api_key):
    """
    Sends a GET request to fetch all available corpora from MetisAI.

    Returns a list of corpora or raises an exception on error.
    """
    url = "https://api.metisai.ir/api/v1/corpora/all"
    headers = {
        "authorization": f"Bearer {api_key}"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raises HTTPError for bad responses
    return response.json()


print(get_all_corpora(METIS_API_KEY))
