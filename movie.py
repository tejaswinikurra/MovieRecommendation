# movie_recommender_app.py

import streamlit as st
import pandas as pd
import ast

# --- Page Configuration ---
st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")

# --- Cursor Style for Genre Dropdown ---
st.markdown("""
    <style>
    div[data-baseweb="select"] > div {
        cursor: pointer !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- Load Data ---
titles_path = "C:/Users/saite/OneDrive/Documents/archive/titles.csv"
credits_path = "C:/Users/saite/OneDrive/Documents/archive/credits.csv"
titles_df = pd.read_csv(titles_path)
credits_df = pd.read_csv(credits_path)

# --- Merge titles and credits on id ---
movies_df = pd.merge(titles_df, credits_df, on="id", how="left")

# --- UI Layout ---
st.title("🎬 Movie Watch List")
st.write("Get movie recommendations based on genre, description, and release year!")

# --- Helper Function ---
def clean_genre(genre_str):
    try:
        genre_list = ast.literal_eval(genre_str)
        if isinstance(genre_list, list):
            return [g.strip() for g in genre_list]
    except:
        pass
    return []

# --- Sidebar Controls ---
st.sidebar.header("🔍 Filter Options")
all_genres = titles_df['genres'].dropna().apply(clean_genre).explode().dropna().unique()
selected_genre = st.sidebar.selectbox("Choose a genre:", sorted(all_genres))

user_description = st.sidebar.text_area("Describe the type of movie you want:", placeholder="e.g., thrilling action, space adventure...", key="desc_input")

# --- Get Recommendations Button ---
get_recommendations = st.sidebar.button("🎯 Get Recommendations")

selected_year = st.sidebar.slider("Select release year:", int(titles_df["release_year"].min()), int(titles_df["release_year"].max()), (2000, 2023))

# --- Display Results After Button Click ---
if get_recommendations:
    filtered_movies = titles_df[
        titles_df['genres'].apply(lambda g: selected_genre in clean_genre(g) if pd.notna(g) else False) &
        titles_df['release_year'].between(selected_year[0], selected_year[1])
    ]

    st.subheader(f"🎥 Top {min(10, len(filtered_movies))} {selected_genre} Movies ({selected_year[0]}–{selected_year[1]}):")
    
    if user_description:
        st.markdown(f"**Description:** _{user_description}_")

    for _, row in filtered_movies.head(10).iterrows():
        st.markdown(f"**🎬 {row['title']}** ({row['release_year']})")
        st.markdown(f"📂 Genres: {row['genres']}")
        if pd.notna(row.get("description")):
            st.markdown(f"> {row['description']}")
        st.markdown("---")
