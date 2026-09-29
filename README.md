# Python Projects

A collection of Python projects I built while learning: web scraping,
Excel automation, debugging, and chatbots. Each folder is a complete
mini-project with its own README and run instructions.

## Projects

| Project | What it does |
|---|---|
| `web-scraper/` | Polite scraper for books.toscrape.com - extracts title, price, rating, availability into CSV + Excel |
| `excel-automation/` | Sales report generator - pandas + openpyxl turn raw CSV sales data into a formatted Excel report with charts |
| `bug-fixing-demo/` | Debugging exercise - a buggy script with 4 realistic bugs, the fixed version, and full bugfix notes |
| `ai-chatbot/` | FAQ chatbot for a fictional bakery - LLM backend (OpenAI/Claude/Gemini) with keyword-matching fallback, zero keys needed |

## Tech stack

- `requests`, `beautifulsoup4` - web scraping
- `pandas`, `openpyxl` - Excel automation and reporting
- Standard library - debugging demo, chatbot logic

Nothing else. Every project installs with `pip install -r requirements.txt`
from its own folder.

## How to run each project

```bash
# 1. Web scraper
cd web-scraper && pip install -r requirements.txt && python scrape_books.py

# 2. Excel automation
cd ../excel-automation && pip install -r requirements.txt && python generate_report.py

# 3. Bug-fixing demo
cd ../bug-fixing-demo && python buggy_version.py && python fixed_version.py

# 4. AI chatbot
cd ../ai-chatbot && pip install -r requirements.txt && python bot.py
```

The chatbot runs in keyword-matching mode with no API key. To use an LLM
backend, export one of `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, or
`GEMINI_API_KEY` first.

## Notes

- All data is sample or public. The scraper only touches the public
  practice site books.toscrape.com - no logins, no paywalls.
- No credentials are stored anywhere in this repo.
