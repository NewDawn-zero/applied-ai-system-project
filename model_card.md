# PawPal+ Model Card

## 1. System Design

**Initial Design**

Owner -- holds the owner's name and their list of pets
Pet -- holds pet info and a list of tasks
Task -- represents one care activity with a time, duration, and priority
Scheduler -- sorts, filters, and manages all tasks across pets

**Design Changes**

The core class structure stayed the same from Module 2. For this final version we added a RAG engine, an agentic workflow, and an eval harness on top of the existing system without changing the original logic layer.

---

## 2. Scheduling Logic and Tradeoffs

**Constraints and Priorities**

The scheduler considers time of day and priority level. Time was the most important constraint because tasks like medication and feeding are time-sensitive and need to happen in the right order.

**Tradeoffs**

Conflict detection only checks for exact time matches, not overlapping durations. Two tasks at 08:00 and 08:10 with 30 minute durations would not be flagged even though they overlap.

---

## 3. AI Collaboration

**How I Used AI**

Used AI to help retrieve and reason over pet care knowledge through the RAG engine. The AI looks up the most relevant chunks from the knowledge base before generating a response, which keeps answers grounded in real data instead of making things up.

**Helpful Suggestion**

The agent correctly identified missing feeding and grooming tasks when analyzing a real schedule, which showed it was actually reasoning over the data and not just generating generic advice.

**Flawed Suggestion**

The AI sometimes pulled from the wrong knowledge chunk when a question was too vague. Asking "what should I do for my pet" returned scheduling guidelines instead of health advice because the keyword scoring matched the wrong section.

---

## 4. Testing and Verification

**What Was Tested**

Tested task completion, chronological sorting, recurring task scheduling, conflict detection, and 5 RAG questions through the eval harness.

**Results**

5/5 eval harness tests passed. Confidence scores averaged 0.35 to 0.45. Edge cases like empty pet lists or identical task names across pets could use more coverage.

**Confidence Level**

4/5. The core system is reliable but RAG retrieval could be smarter with a vector database instead of keyword scoring.

---

## 5. Limitations and Ethics

**Limitations**

The knowledge base is small and hand-written so the AI can only answer questions covered in that file. It would struggle with rare medical conditions or breed-specific care questions.

**Potential Misuse**

Someone could treat the AI advice as a replacement for a real vet which could harm their pet. The system should always make clear it is not a substitute for professional veterinary advice.

**What Surprised Me**

How much the quality of the retrieved chunk affected the final answer. When the wrong chunk was retrieved the answer was still confident but completely off topic.

---

## 6. Reflection

**What Went Well**

The UML design from Module 2 made it easy to extend the system. Having a clean class structure meant adding RAG and the agent on top was straightforward.

**What I Would Improve**

Add a vector database like FAISS for smarter retrieval and add the ability to mark tasks complete directly in the Streamlit UI.

**Key Takeaway**

RAG is a simple but powerful way to ground AI responses in real data. The difference between a hallucinated answer and a grounded one comes down to what context you give the model.