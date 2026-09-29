# FAQ Chatbot - Sunrise Bakery

A terminal chatbot I built for a fictional bakery. It answers customer
questions from an FAQ file, two ways:

1. **LLM mode** - if you set an API key, answers come from an LLM
   (OpenAI, Anthropic Claude, or Google Gemini) grounded on the FAQ, so it
   handles rephrased and follow-up questions.
2. **Keyword mode** - with no API key set, it matches questions to FAQ
   entries by keyword overlap. Runs with zero setup.

## How to run

```bash
pip install -r requirements.txt
python bot.py
```

Type `quit` to exit.

## Using an LLM backend (optional)

Bring your own API key - keys are never stored in the repo.
Set one environment variable before running:

```bash
export OPENAI_API_KEY="sk-..."        # OpenAI
export ANTHROPIC_API_KEY="sk-ant-..." # Anthropic Claude
export GEMINI_API_KEY="..."           # Google Gemini
```

The bot detects the key automatically and prefers OpenAI > Claude > Gemini
when several are set. API errors fall back to keyword matching instead of
crashing.

## What this demonstrates

- FAQ-driven chatbot architecture (data file separate from logic)
- LLM integration via plain HTTP for three providers
- Graceful degradation: full functionality with zero API keys
- Clean separation: `faq_data.json` (content), `llm_backend.py`
  (AI layer), `bot.py` (interface)
