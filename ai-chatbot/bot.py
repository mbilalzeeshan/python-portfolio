"""Sunrise Bakery FAQ chatbot - terminal demo.

Answers customer questions about a fictional bakery. If an LLM API key is
present in the environment (see llm_backend.py), answers come from the LLM
grounded on the FAQ. Otherwise it falls back to keyword matching, so the
bot runs with zero setup and zero keys.

Run:
    pip install -r requirements.txt
    python bot.py

Type 'quit' to exit.
"""

import json
import re

from llm_backend import backend_name, get_answer

FAQ_FILE = "faq_data.json"
FALLBACK = ("I'm not sure about that. Please call us at (555) 123-4567 or "
            "email hello@sunrisebakery.example and we'll help you out!")


def load_faqs(path=FAQ_FILE):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return data["business"], data["faqs"]


def keyword_answer(question, faqs):
    """Score each FAQ by keyword overlap and return the best answer."""
    words = set(re.findall(r"[a-z]+", question.lower()))
    best, best_score = None, 0
    for faq in faqs:
        score = len(words & set(faq["keywords"]))
        if score > best_score:
            best, best_score = faq, score
    return best["answer"] if best else FALLBACK


def main():
    business, faqs = load_faqs()
    llm = backend_name()
    if llm:
        print(f"Sunrise Bakery assistant ({llm} backend). Type 'quit' to exit.")
    else:
        print("Sunrise Bakery assistant (keyword-matching mode - no API key set).")
        print("Set OPENAI_API_KEY, ANTHROPIC_API_KEY or GEMINI_API_KEY for LLM answers.")
    print("Ask me about hours, delivery, cakes, prices and more.\n")

    while True:
        try:
            question = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break
        if question.lower() in ("quit", "exit"):
            print("Goodbye!")
            break
        if not question:
            continue

        answer = None
        if llm:
            try:
                answer = get_answer(question, faqs)
            except Exception as exc:  # API error -> fall back gracefully
                print(f"(LLM backend error: {exc} - using keyword matching)")
        if answer is None:
            answer = keyword_answer(question, faqs)
        print(f"Bot: {answer}\n")


if __name__ == "__main__":
    main()
