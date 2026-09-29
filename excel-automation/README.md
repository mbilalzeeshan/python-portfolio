# Sales Report Generator

A project I built to learn Excel automation: reads `sample_sales.csv`
(60 realistic sales rows across 3 months) and builds a formatted Excel
report with `pandas` + `openpyxl`.

## What it produces: monthly_report.xlsx

- **Summary sheet** - revenue totals by month and by product, grand total,
  plus a bar chart of revenue per product
- **Data sheet** - every sale with a computed Revenue column, styled
  headers, tuned column widths, currency and date formats, filters

## How to run

```bash
pip install -r requirements.txt
python generate_report.py
```

## What this demonstrates

- Reading and transforming CSV data with pandas
- Multi-sheet Excel workbooks with openpyxl
- Cell styling: fonts, fills, borders, number formats
- Native Excel charts generated from code
