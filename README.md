# GreenScore.ai

A Streamlit app that turns raw electricity usage into a sustainability "credit score" for a home, hostel, or company — with an ESG-style letter grade, an estimated green incentive or carbon cost, and side-by-side comparison across multiple sites.

## What it does

1. **Single-entity scoring** — enter electricity used (kWh), and optionally headcount and floor area. The app converts usage to CO₂ (using a fixed grid emission factor of 0.82 kg CO₂/kWh), normalizes it per person and per unit area, and maps the result to:
   - a **Green Score** (0–100)
   - an **ESG grade** (A+ to D)
   - an estimated **green incentive or carbon cost**, in ₹ or $
   - plain-language insights and suggested next actions (solar, green loans, efficiency report)

2. **Bulk comparison** — upload a CSV/XLSX with `Name, Units, People, Area` columns to rank multiple homes/hostels/companies by Green Score, with a bar chart comparison.

## Run it locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Open the URL Streamlit prints (defaults to `http://localhost:8501`).

## Bulk upload format

| Name    | Units | People | Area |
|---------|-------|--------|------|
| Block A | 1200  | 40     | 500  |
| Block B | 900   | 35     | 450  |

## Tech stack

Python, Streamlit, pandas, NumPy, openpyxl.

## Notes / limitations

- The emission factor (0.82 kg CO₂/kWh) and score thresholds are fixed constants for demo purposes, not calibrated against a specific grid or regulatory standard.
- This is a single-file prototype (`app.py`) with no persistence, auth, or automated tests — a good starting point for a real sustainability-scoring product, not production-ready as-is.
