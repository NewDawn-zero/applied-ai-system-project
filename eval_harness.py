from dotenv import load_dotenv
load_dotenv()
from pawpal_system import Owner, Pet, Task, Scheduler
from rag_engine import ask_rag, confidence_score

test_cases = [
    {
        "query": "How often should I feed my dog?",
        "expected_keywords": ["feed", "day", "morning", "evening"]
    },
    {
        "query": "How much exercise does my cat need?",
        "expected_keywords": ["play", "minutes", "daily", "active"]
    },
    {
        "query": "When should I take my pet to the vet?",
        "expected_keywords": ["annual", "checkup", "senior", "vaccination"]
    },
    {
        "query": "How often should I groom my dog?",
        "expected_keywords": ["brush", "weekly", "bath", "nails"]
    },
    {
        "query": "What foods are dangerous for pets?",
        "expected_keywords": ["chocolate", "grapes", "onions", "avoid"]
    },
]

def run_eval():
    print("PawPal+ Evaluation Harness")
    print("=" * 40)
    passed = 0
    total = len(test_cases)
    scores = []

    for i, test in enumerate(test_cases):
        print(f"\nTest {i+1}: {test['query']}")
        answer, retrieved = ask_rag(test["query"])
        score = confidence_score(answer, [retrieved])
        scores.append(score)
        answer_lower = answer.lower()
        hits = [kw for kw in test["expected_keywords"] if kw in answer_lower]
        result = "PASS" if len(hits) >= 2 else "FAIL"
        if result == "PASS":
            passed += 1
        print(f"Result: {result}")
        print(f"Confidence Score: {score}")
        print(f"Keywords matched: {hits}")
        print(f"Answer preview: {answer[:100]}...")

    print("\n" + "=" * 40)
    print(f"Tests Passed: {passed}/{total}")
    print(f"Average Confidence: {round(sum(scores)/len(scores), 2)}")
    print("=" * 40)

if __name__ == "__main__":
    run_eval()