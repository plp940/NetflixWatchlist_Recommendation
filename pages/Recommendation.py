import streamlit as st
import pandas as pd

st.title("🎯 Netflix Movie Recommendation")

# Load the dataset
df = pd.read_csv("cleaned_netflix_data.csv")
df.fillna("Not Available", inplace=True)

# Extract genres
genre_series = df['listed_in'].str.split(', ').explode()
unique_genres = sorted(genre_series.dropna().unique().tolist())
unique_ratings = sorted(df['rating'].dropna().unique().tolist())
unique_types = sorted(df['type'].dropna().unique().tolist())
unique_countries = sorted(df['country'].dropna().unique().tolist())
unique_years = sorted(df['release_year'].dropna().unique().tolist())


# Sidebar Filters
st.sidebar.header("🎛️ Filter Criteria")

selected_genre = st.sidebar.multiselect("Select Genre(s)", options=["All"] + unique_genres, default="All")
selected_rating = st.sidebar.multiselect("Select Rating(s)", options=["All"] + unique_ratings, default="All")
selected_type = st.sidebar.multiselect("Select Type(s)", options=["All"] + unique_types, default="All")
selected_country = st.sidebar.multiselect("Select Country(ies)", options=["All"] + unique_countries, default="All")
selected_year = st.sidebar.multiselect("Select Release Year(s)", options=["All"] + unique_years, default="All")

# Filter logic
recommendations = df.copy()

if "All" not in selected_genre:
    recommendations = recommendations[recommendations['listed_in'].str.contains('|'.join(selected_genre), na=False)]
if "All" not in selected_rating:
    recommendations = recommendations[recommendations['rating'].isin(selected_rating)]
if "All" not in selected_type:
    recommendations = recommendations[recommendations['type'].isin(selected_type)]
if "All" not in selected_country:
    recommendations = recommendations[recommendations['country'].isin(selected_country)]
if "All" not in selected_year:
    recommendations = recommendations[recommendations['release_year'].isin(selected_year)]



st.subheader("🎬 Top Matching Recommendations")
with st.expander("📘 What Do Ratings Mean?"):
    st.markdown("""
    | Rating   | Meaning                                | Audience            |
    |----------|----------------------------------------|---------------------|
    | **G**     | General Audience – Suitable for all ages       | 👶 Kids & Families |
    | **PG**    | Parental Guidance Suggested                     | 🧒 Younger Viewers |
    | **PG-13** | Parents Strongly Cautioned – May be inappropriate under 13 | 👦 Teens 13+ |
    | **R**     | Restricted – Under 17 requires accompanying adult | 🧑 Adults/Teens 17+ |
    | **NC-17** | No one 17 and under admitted                    | 🔞 Adults Only     |
    | **TV-G**  | Suitable for all ages (TV content)              | 📺 General Audience |
    | **TV-14** | May be inappropriate for children under 14      | 📺 Teens 14+       |
    | **NR**    | Not Rated                                        | ⚠️ Varies          |
    """)

# Results
if not recommendations.empty:
# Pagination setup
   page_size = 10
   total_results = len(recommendations)
   total_pages = (total_results - 1) // page_size + 1

   selected_page = st.number_input("Page", min_value=1, max_value=total_pages, step=1, value=1)

# Show paginated results
   start_idx = (selected_page - 1) * page_size
   end_idx = start_idx + page_size
   paginated_results = recommendations.iloc[start_idx:end_idx]

   st.subheader(f"🎬 Showing results {start_idx+1} to {min(end_idx, total_results)} of {total_results}")
   st.write(paginated_results[['title', 'type', 'country', 'release_year', 'rating']])
else:
    st.warning("No titles match the selected filters.")
