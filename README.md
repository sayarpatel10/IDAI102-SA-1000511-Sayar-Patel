# ShopImpact 🌿

A friendly conscious-shopping dashboard built with Python and Streamlit.

## Features
- Log planned purchases with category, brand, price and planned date.
- Estimate CO₂e using category multipliers.
- Monthly spending dashboard and purchase history.
- Eco badges, greener alternatives and rotating eco tips.
- CSV export.
- Turtle-inspired illustration in the Streamlit interface.
- A separate `turtle_graphics.py` file that uses Python's actual `turtle` library to draw a turtle and leaf.

## Run the Streamlit app locally/ Live Link
```bash
pip install -r requirements.txt
streamlit run app.py
Live Link: https://ndtjzgpnx2vpfmg2hqykhu.streamlit.app/
```

## Run the actual Python Turtle drawing
On a computer with a desktop display and Python Tk support:
```bash
python turtle_graphics.py
```
This opens a Turtle graphics window. Streamlit Community Cloud runs without a desktop display, so it cannot open tkinter/Turtle windows. The web app uses an SVG fallback illustration so the deployed app still works. Include `turtle_graphics.py` in your GitHub repository as evidence of the actual Turtle implementation.

## CO₂ estimate note
The multipliers are simplified illustrative classroom estimates, not verified product life-cycle assessment data.

## Deploy
Upload `app.py`, `requirements.txt`, `turtle_graphics.py` and `README.md` to GitHub. In Streamlit Community Cloud, select the repository and `app.py` as the main file.
