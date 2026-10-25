
# Global Olympic Sports Performance Analysis

A beginner-friendly data analytics project using Python, Pandas, Plotly and Streamlit. It displays medal trends, top countries, sport-wise medals, medal type distribution, and filterable data.

## 1. Run locally (Windows)

1. Install Python 3.10 or newer from https://www.python.org/downloads/ (tick **Add Python to PATH**).
2. Extract this ZIP folder.
3. Open the extracted `olympic_sports_analysis` folder in VS Code.
4. Open Terminal > New Terminal.
5. Run:

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

6. Streamlit will show a local URL, usually `http://localhost:8501`. Open it in your browser.
7. Stop the app by pressing `Ctrl + C` in the terminal.

If `python` is not recognized, try `py` instead:
```bash
py -m pip install -r requirements.txt
py -m streamlit run app.py
```

## 2. Dataset

The app runs immediately with a small illustrative demo dataset built into `app.py`. This is only for demonstrating the dashboard, not for making factual claims about Olympic totals.

For real analysis, place a verified dataset at `data/olympic_medals.csv` with these columns:

- `Year`
- `Country`
- `Region`
- `Season` (Summer or Winter)
- `Sport`
- `Medal` (Gold, Silver, Bronze)
- `Medal_Count` (numeric count represented by each row)
- `Athlete_Count` (numeric athlete count represented by each row)

Each row should represent an aggregated group with consistent units. If your downloaded dataset has one row per athlete/medal, clean and aggregate it first so counts are not double-counted.

## 3. Deploy on Streamlit Community Cloud

1. Create a GitHub account and a new public repository.
2. Upload `app.py`, `requirements.txt`, `README.md`, and the `data` folder (if using your own dataset).
3. Open https://share.streamlit.io/ and sign in with GitHub.
4. Select **Create app**, choose your repository, branch, and `app.py`.
5. Click **Deploy**. Wait for the build to finish.
6. Copy the app URL and add it to the SkillWallet **Add Demo Link** field.
7. Add your GitHub repository URL in **Add Github Link**.

Keep datasets small enough for the hosting service and do not upload private data or credentials.

## 4. Tableau option

The same project can also be built in Tableau Public:
- KPI cards: total medals, gold, silver, bronze.
- Line chart: total medals by year.
- Horizontal bar chart: top 10 countries.
- Bar chart: medals by sport.
- Pie chart: medal type distribution.
- Filters: season, country, year, sport.
- Story points: country performance, sport investment/efficiency, and long-term trends.

The included Streamlit app is a working web-dashboard version. If the SkillWallet task specifically requires Tableau Public, also create and publish the Tableau workbook; a Streamlit URL alone may not satisfy that requirement.

