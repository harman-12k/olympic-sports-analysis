import os
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Global Olympic Sports Performance Analysis", layout="wide")
st.title("🏅 Global Olympic Sports Performance Analysis")
st.caption("Explore medal trends, country performance, sports, and athlete participation.")

DATA_PATH = "data/olympic_medals.csv"

@st.cache_data
def load_data():
    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
    else:
        # Small demo dataset so the project runs immediately.
        df = pd.DataFrame([
            [1992, "Spain", "Europe", "Summer", "Athletics", "Gold", 1, 1],
            [1992, "United States", "North America", "Summer", "Swimming", "Gold", 1, 1],
            [1996, "United States", "North America", "Summer", "Basketball", "Gold", 12, 12],
            [2000, "Australia", "Oceania", "Summer", "Swimming", "Gold", 3, 3],
            [2004, "China", "Asia", "Summer", "Gymnastics", "Gold", 4, 4],
            [2008, "China", "Asia", "Summer", "Diving", "Gold", 5, 5],
            [2012, "United States", "North America", "Summer", "Athletics", "Gold", 8, 8],
            [2016, "Great Britain", "Europe", "Summer", "Cycling", "Gold", 6, 6],
            [2020, "Japan", "Asia", "Summer", "Judo", "Gold", 9, 9],
            [2024, "United States", "North America", "Summer", "Swimming", "Gold", 8, 8],
            [1994, "Norway", "Europe", "Winter", "Cross-Country Skiing", "Gold", 5, 5],
            [1998, "Germany", "Europe", "Winter", "Luge", "Gold", 3, 3],
            [2002, "Canada", "North America", "Winter", "Ice Hockey", "Gold", 20, 20],
            [2006, "Italy", "Europe", "Winter", "Alpine Skiing", "Gold", 4, 4],
            [2010, "Canada", "North America", "Winter", "Ice Hockey", "Gold", 20, 20],
            [2014, "Norway", "Europe", "Winter", "Cross-Country Skiing", "Gold", 11, 11],
            [2018, "Norway", "Europe", "Winter", "Biathlon", "Gold", 8, 8],
            [2022, "Norway", "Europe", "Winter", "Cross-Country Skiing", "Gold", 9, 9],
            [2000, "Kenya", "Africa", "Summer", "Athletics", "Silver", 3, 3],
            [2004, "Ethiopia", "Africa", "Summer", "Athletics", "Gold", 2, 2],
            [2008, "Jamaica", "North America", "Summer", "Athletics", "Gold", 6, 6],
            [2012, "Jamaica", "North America", "Summer", "Athletics", "Gold", 4, 4],
            [2016, "Kenya", "Africa", "Summer", "Athletics", "Gold", 6, 6],
            [2024, "China", "Asia", "Summer", "Table Tennis", "Gold", 5, 5],
        ], columns=["Year", "Country", "Region", "Season", "Sport", "Medal", "Medal_Count", "Athlete_Count"])
    required = ["Year", "Country", "Region", "Season", "Sport", "Medal", "Medal_Count", "Athlete_Count"]
    for col in required:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df["Medal_Count"] = pd.to_numeric(df["Medal_Count"], errors="coerce").fillna(0)
    df["Athlete_Count"] = pd.to_numeric(df["Athlete_Count"], errors="coerce").fillna(0)
    df = df.dropna(subset=["Year", "Country", "Sport", "Medal"])
    df["Year"] = df["Year"].astype(int)
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Could not load data: {e}")
    st.info("Check that data/olympic_medals.csv has the required columns. See README.md.")
    st.stop()

with st.sidebar:
    st.header("Filters")
    seasons = ["All"] + sorted(df["Season"].dropna().astype(str).unique().tolist())
    season = st.selectbox("Olympic season", seasons)
    countries = ["All"] + sorted(df["Country"].dropna().astype(str).unique().tolist())
    country = st.selectbox("Country", countries)
    years = sorted(df["Year"].unique().tolist())
    year_range = st.slider("Year range", min_value=int(min(years)), max_value=int(max(years)),
                           value=(int(min(years)), int(max(years))))
    sports = ["All"] + sorted(df["Sport"].dropna().astype(str).unique().tolist())
    sport = st.selectbox("Sport", sports)

filtered = df.copy()
if season != "All":
    filtered = filtered[filtered["Season"] == season]
if country != "All":
    filtered = filtered[filtered["Country"] == country]
filtered = filtered[filtered["Year"].between(year_range[0], year_range[1])]
if sport != "All":
    filtered = filtered[filtered["Sport"] == sport]

gold = int(filtered.loc[filtered["Medal"].str.lower() == "gold", "Medal_Count"].sum())
silver = int(filtered.loc[filtered["Medal"].str.lower() == "silver", "Medal_Count"].sum())
bronze = int(filtered.loc[filtered["Medal"].str.lower() == "bronze", "Medal_Count"].sum())
total = int(filtered["Medal_Count"].sum())
athletes = int(filtered["Athlete_Count"].sum())
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total medals", f"{total:,}")
c2.metric("Gold medals", f"{gold:,}")
c3.metric("Silver medals", f"{silver:,}")
c4.metric("Bronze medals", f"{bronze:,}")
c5.metric("Athlete entries", f"{athletes:,}")

if filtered.empty:
    st.warning("No records match the selected filters.")
    st.stop()

left, right = st.columns(2)
with left:
    st.subheader("Medal trend by year")
    trend = filtered.groupby("Year", as_index=False)["Medal_Count"].sum()
    st.plotly_chart(px.line(trend, x="Year", y="Medal_Count", markers=True,
                            title="Total medals by Olympic year"), use_container_width=True)
with right:
    st.subheader("Top countries")
    top_countries = filtered.groupby("Country", as_index=False)["Medal_Count"].sum()
    top_countries = top_countries.sort_values("Medal_Count", ascending=False).head(10)
    st.plotly_chart(px.bar(top_countries, x="Medal_Count", y="Country", orientation="h",
                           title="Top 10 countries by medals"), use_container_width=True)

left, right = st.columns(2)
with left:
    st.subheader("Medals by sport")
    by_sport = filtered.groupby("Sport", as_index=False)["Medal_Count"].sum().sort_values("Medal_Count", ascending=False).head(12)
    st.plotly_chart(px.bar(by_sport, x="Sport", y="Medal_Count", title="Medals by sport"),
                    use_container_width=True)
with right:
    st.subheader("Medal type distribution")
    by_medal = filtered.groupby("Medal", as_index=False)["Medal_Count"].sum()
    st.plotly_chart(px.pie(by_medal, names="Medal", values="Medal_Count", hole=0.35,
                           title="Gold, silver and bronze"), use_container_width=True)

st.subheader("Country and sport comparison")
pivot = filtered.pivot_table(index="Country", columns="Sport", values="Medal_Count",
                             aggfunc="sum", fill_value=0)
st.dataframe(pivot, use_container_width=True)

st.subheader("Filtered data")
st.dataframe(filtered, use_container_width=True)
st.download_button("Download filtered CSV", filtered.to_csv(index=False).encode("utf-8"),
                   file_name="olympic_filtered_data.csv", mime="text/csv")

st.markdown("### Notes")
st.write("This project includes a small demonstration dataset so it runs immediately. Replace it with a verified Olympic medal dataset for real historical conclusions.")
