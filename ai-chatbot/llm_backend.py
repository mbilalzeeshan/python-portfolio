"""LLM backend with graceful fallback.

Checks for an API key in the environment, in this order:
  1. OPENAI_API_KEY   -> OpenAI chat completions API
  2. ANTHROPIC_API_KEY -> Anthropic messages API
  3. GEMINI_API_KEY (or GOOGLE_API_KEY) -> Google Gemini API

If a key is found, the question is answered by the LLM using ONLY the
business FAQ as context. If no key is found, get_answer() returns None and
bot.py falls back to keyword matching - so the chatbot runs with zero keys.

IMPORTANT: API keys are never stored in this repo. The buyer (business
owner) provides their own key via an environment variable, e.g.:
    export OPENAI_API_KEY="sk-..."
"""

import json
import os

import requests

TIMEOUT = 20


def _faq_context(faqs):
    lines = [f"Q: {item['question']}\nA: {item['answer']}" for item in faqs]
    return "\n\n".join(lines)


def _openai_answer(question, context):
    key = os.environ["OPENAI_API_KEY"]
    resp = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json={
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system",
                 "content": "You are a helpful FAQ assistant for a small business. "
                            "Answer ONLY using the FAQ below. If the FAQ does not "
                            "cover the question, say you don't know and suggest "
                            "contacting the business.\n\n" + context},
                {"role": "user", "content": question},
            ],
            "max_tokens": 200,
        },
        timeout=TIMEOUT,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"].strip()


def _anthropic_answer(question, context):
    key = os.environ["ANTHROPIC_API_KEY"]
    resp = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        },
        json={
            "model": "claude-3-5-haiku-latest",
            "max_tokens": 200,
            "system": "You are a helpful FAQ assistant for a small business. "
                      "Answer ONLY using the FAQ below. If the FAQ does not "
                      "cover the question, say you don't know and suggest "
                      "contacting the business.\n\n" + context,
            "messages": [{"role": "user", "content": question}],
        },
        timeout=TIMEOUT,
    )
    resp.raise_for_status()
    return resp.json()["content"][0]["text"].strip()


def _gemini_answer(question, context):
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    resp = requests.post(
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"gemini-2.0-flash:generateContent?key={key}",
        headers={"Content-Type": "application/json"},
        json={
            "system_instruction": {
                "parts": [{"text": "You are a helpful FAQ assistant for a small business. "
                                   "Answer ONLY using the FAQ below. If the FAQ does not "
                                   "cover the question, say you don't know and suggest "
                                   "contacting the business.\n\n" + context}]
            },
            "contents": [{"parts": [{"text": question}]}],
            "generationConfig": {"maxOutputTokens": 200},
        },
        timeout=TIMEOUT,
    )
    resp.raise_for_status()
    return resp.json()["candidates"][0]["content"]["parts"][0]["text"].strip()


def backend_name():
    """Name of the active LLM backend, or None if no API key is set."""
    if os.environ.get("OPENAI_API_KEY"):
        return "OpenAI"
    if os.environ.get("ANTHROPIC_API_KEY"):
        return "Anthropic Claude"
    if os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY"):
        return "Google Gemini"
    return None


def get_answer(question, faqs):
    """Return an LLM answer string, or None when no API key is configured
    (caller should fall back to keyword matching)."""
    context = _faq_context(faqs)
    name = backend_name()
    if name == "OpenAI":
        return _openai_answer(question, context)
    if name == "Anthropic Claude":
        return _anthropic_answer(question, context)
    if name == "Google Gemini":
        return _gemini_answer(question, context)
    return None
