# Web Scraper - Books to Scrape

A polite Python web scraper built with `requests` and `BeautifulSoup`. It
scrapes every book on [books.toscrape.com](http://books.toscrape.com)
(a public site made for practising scraping - no login, no paywall) and
saves clean data to **books.csv** and **books.xlsx**.

Portfolio project: **web scraping and data extraction**.

## What it extracts

- Book title
- Price (GBP)
- Star rating (1-5)
- Availability (in stock / out of stock)

## How to run

```bash
pip install -r requirements.txt
python scrape_books.py
```

Output files `books.csv` and `books.xlsx` are created in this folder.

## How it stays polite

- Sends a real `User-Agent` header identifying the scraper
- Waits 0.7 seconds between page requests (see `DELAY_SECONDS`)
- Stops automatically at the last catalogue page (first 404)
- Only scrapes publicly available pages - no logins, no forms, no bypassing
