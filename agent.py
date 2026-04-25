from dotenv import load_dotenv
load_dotenv()
import os
from groq import Groq
from pawpal_system import Scheduler

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def run_agent(owner):
    scheduler = Scheduler(owner)
    schedule = scheduler.daily_schedule()
    conflicts = scheduler.detect_conflicts()

    steps = []

    steps.append("STEP 1: Reading current schedule...")
    steps.append(schedule)

    steps.append("\nSTEP 2: Checking for conflicts...")
    if conflicts:
        for c in conflicts:
            steps.append(f"  WARNING: {c}")
    else:
        steps.append("  No conflicts found.")

    steps.append("\nSTEP 3: Analyzing schedule with AI...")

    conflict_text = "\n".join(conflicts) if conflicts else "None"

    prompt = f"""You are PawPal+, a pet care scheduling assistant.

Here is the current pet schedule:
{schedule}

Conflicts detected:
{conflict_text}

Do the following:
1. Identify any missing routine tasks (feeding, exercise, medication, grooming).
2. Flag any scheduling concerns.
3. Suggest 2 to 3 specific improvements to the schedule.
4. Rate the overall schedule quality from 1 to 5 stars.

Be specific, practical, and friendly. Keep your response concise."""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    ai_response = response.choices[0].message.content
    steps.append(ai_response)

    steps.append("\nSTEP 4: Generating final recommendations...")
    steps.append("Agent analysis complete.")

    return "\n".join(steps)