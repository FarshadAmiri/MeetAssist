# rag_uploader.py

import requests
import textwrap

def chunk_text(text, max_tokens=400):
    """
    Split the text into chunks of approximately `max_tokens` words.
    This is a simple splitter based on whitespace. You can replace this with a token-based splitter if needed.
    """
    words = text.split()
    chunks = [' '.join(words[i:i+max_tokens]) for i in range(0, len(words), max_tokens)]
    return chunks

def upload_to_rag(api_key, corpus_id, full_text, reference_url=None):
    """
    Chunks the full_text and uploads each chunk individually to the RAG vector database.
    """
    url_template = f"https://api.metisai.ir/api/v1/corpora/{corpus_id}/chunks"
    headers = {
        "authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    chunks = chunk_text(full_text)

    results = []
    for i, chunk in enumerate(chunks):
        payload = {
            "text": chunk,
            "metadata": {
                "reference": {
                    "type": "file",
                    "downloadUrl": reference_url or "https://your-default-reference.com"
                },
                "downloadUrl": reference_url or "https://your-default-reference.com"
            }
        }

        response = requests.post(url_template, json=payload, headers=headers)
        response.raise_for_status()
        results.append(response.json())

    return results



def retrieve_relevant_chunks(api_key, corpus_id, query_text, top_k=5):
    url = f"https://api.metisai.ir/api/v1/corpora/{corpus_id}/search"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "query": query_text,
        "topK": top_k
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    results = response.json()

    # Extract and concatenate the retrieved chunk texts
    chunks = [hit["text"] for hit in results.get("hits", [])]
    return "\n\n".join(chunks)


# def retrieve_relevant_chunks(api_key, corpus_id, query_text, top_k=5, min_score=0.7):
#     url = f"https://api.metisai.ir/api/v1/corpora/{corpus_id}/search"
#     headers = {
#         "Authorization": f"Bearer {api_key}",
#         "Content-Type": "application/json"
#     }
#     payload = {
#         "query": query_text,
#         "topK": top_k
#     }

#     response = requests.post(url, headers=headers, json=payload)
#     response.raise_for_status()
#     results = response.json()

#     # Apply confidence score threshold if 'score' is included in hits
#     chunks = [
#         hit["text"] for hit in results.get("hits", [])
#         if "score" not in hit or hit["score"] >= min_score
#     ]

#     return "\n\n".join(chunks)