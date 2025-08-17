# 🤖 AI Meeting Assistant

An **agentic AI system** that assists with online meetings (currently supports **Google Meet**).  
It automatically joins meetings on behalf of subscribed users, **transcribes**, **summarizes**, and generates **meeting minutes** with action items.  

---

## ✨ Features

- 🔑 **Google Account Agent**  
  - Securely signs in to a Gmail account.  
  - Joins Google Meet sessions that the subscribed user invites it to.  

- 🎤 **Transcription (English & Persian)**  
  - Real-time or post-meeting transcription of conversations.  
  - Powered by robust speech-to-text models.  

- 📝 **Meeting Summaries (Minutes)**  
  - Uses an LLM (default: OpenAI GPT models) to summarize discussions.  
  - Highlights key decisions, topics, and **action items per participant**.  

- 📚 **Knowledge Memory with Vector DB**  
  - Stores meeting data into a vector database.  
  - Supports **semantic search & retrieval** of past discussions.  
  - Links current meeting context with **previous commitments & progress**.  

- 📧 **Automated Recap Emails**  
  - After each meeting, participants receive a **recap document** including:  
    - Summary of discussions.  
    - Key decisions.  
    - Action items with assigned owners.  

---

## 🛠️ Tech Stack

- **Frontend/Interface**: TBD (CLI, Web UI, or API integration).  
- **Backend**: Python (FastAPI / Django optional).  
- **LLM**: OpenAI GPT models (configurable).  
- **Vector DB**: ChromaDB / Weaviate / Pinecone.  
- **Speech-to-Text**: OpenAI Whisper / other ASR models.  
- **Google API**: Google Meet & Gmail integration (for participation + emailing).  
