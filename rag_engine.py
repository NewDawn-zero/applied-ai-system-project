from dotenv import load_dotenv
load_dotenv()
import os
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def load_knowledge_base(path="pet_care_kb.txt"):
    with open(path, "r") as f:
        return f.read()

def retrieve_relevant_chunks(query, knowledge_base):
    chunks = knowledge_base.strip().split("\n\n")
    query_words = set(query.lower().split())
    scored = []
    for chunk in chunks:
        chunk_words = set(chunk.lower().split())
        score = len(query_words & chunk_words)
        scored.append((score, chunk))
    scored.sort(reverse=True)
    top = [chunk for score, chunk in scored[:2] if score > 0]
    return top if top else [chunks[0]]

def ask_rag(query, schedule_context=""):
    kb = load_knowledge_base()
    chunks = retrieve_relevant_chunks(query, kb)
    retrieved = "\n\n".join(chunks)

    system_prompt = """You are PawPal+, a friendly and knowledgeable pet care assistant.
You answer questions using the provided pet care knowledge base.
Always be specific, practical, and caring in your responses.
If the knowledge base does not cover the question, say so honestly.
Keep responses concise -- 3 to 5 sentences max."""

    user_message = f"""Knowledge Base:
{retrieved}

Current Schedule Context:
{schedule_context if schedule_context else "No schedule provided."}

User Question: {query}"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    )
    return response.choices[0].message.content, retrieved

def confidence_score(answer, retrieved_chunks):
    answer_words = set(answer.lower().split())
    chunk_words = set(" ".join(retrieved_chunks).lower().split())
    overlap = len(answer_words & chunk_words)
    score = min(round(overlap / max(len(answer_words), 1), 2), 1.0)
    return score