import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from difflib import get_close_matches

# Page Config
st.set_page_config(page_title="Netflix Explorer", layout="wide")

# Load Data
df = pd.read_csv("cleaned_netflix_data.csv")

# Fill missing values (if any were missed)
df.fillna("Not Available", inplace=True)

# Sidebar Filters
st.sidebar.header("🔎 Filter Netflix Content")

type_filter = st.sidebar.selectbox("Select Type", options=["All"] + df['type'].unique().tolist())
country_filter = st.sidebar.multiselect("Select Country", options=df['country'].dropna().unique().tolist())
genre_filter = st.sidebar.multiselect("Select Genre", options=df['listed_in'].dropna().unique().tolist())
year_min, year_max = st.sidebar.slider("Release Year Range", int(df['release_year'].min()), int(df['release_year'].max()), (2010, 2021))

# Filter Logic
filtered_df = df.copy()

if type_filter != "All":
    filtered_df = filtered_df[filtered_df['type'] == type_filter]
if country_filter:
    filtered_df = filtered_df[filtered_df['country'].isin(country_filter)]
if genre_filter:
    filtered_df = filtered_df[filtered_df['listed_in'].isin(genre_filter)]
    filtered_df = filtered_df[(filtered_df['release_year'] >= year_min) & (filtered_df['release_year'] <= year_max)]

# Main Title
st.title("🎬 Netflix Explorer")

# Key Metrics
col1, col2 = st.columns(2)
col1.metric("Total Titles", len(df))
col2.metric("Filtered Titles", len(filtered_df))

# Visualization Section
st.subheader("📊 Visual Insights")

col3, col4, col5 = st.columns(3)

# Type Distribution
with col3:
    st.write("**Type Distribution**")
    st.write("Distribution of Titles by Type (Movie/TV Show)")
    type_counts = filtered_df['type'].value_counts()
    st.bar_chart(type_counts)

# Country Distribution
with col4:
    st.write("**Top 10 Countries**")
    st.write("Distribution of Titles by Country")
    top_countries = filtered_df['country'].value_counts().head(10)
    st.bar_chart(top_countries)

# Yearly Trend
with col5:
    st.write("**Titles Added per Year**")
    st.write("Trend of Titles Added to Netflix Over the Years")
    if 'year_added' in filtered_df.columns:
        # Convert year_added to numeric, coercing errors to NaN and dropping NaNs
        filtered_df['year_added'] = pd.to_numeric(filtered_df['year_added'], errors='coerce')
        filtered_df = filtered_df.dropna(subset=['year_added'])

# Convert to int (if you want)
        filtered_df['year_added'] = filtered_df['year_added'].astype(int)

# Now value_counts and sort_index should work fine
        year_counts = filtered_df['year_added'].value_counts().sort_index()
        st.line_chart(year_counts)
    else:
        st.info("'year_added' column not available.")



# Recommendation Section
st.subheader("📽️ You May Also Like")
selected_title = st.selectbox("Pick a Title to Explore Similar Ones:", filtered_df['title'].unique())

selected_genre = df[df['title'] == selected_title]['listed_in'].values[0]
recommended = df[df['listed_in'].str.contains(selected_genre, na=False)]
recommended = recommended[recommended['title'] != selected_title]

st.write(recommended[['title', 'type', 'country', 'release_year']].head(10))
