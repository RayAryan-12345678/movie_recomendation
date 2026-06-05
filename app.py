import streamlit as st
import pickle
import pandas as pd
import requests

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

# -----------------------------
# LOAD DATA
# -----------------------------
movies_dict = pickle.load(open('models/movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('models/similarity.pkl', 'rb'))

# -----------------------------
# TMDB API
# -----------------------------
API_KEY = "YOUR_TMDB_API_KEY"

def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
        data = requests.get(url).json()

        poster_path = data.get('poster_path')

        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path

    except:
        pass

    return "https://via.placeholder.com/500x750?text=No+Poster"


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]

    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_names = []
    recommended_posters = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_names.append(
            movies.iloc[i[0]].title
        )

        recommended_posters.append(
            fetch_poster(movie_id)
        )

    return recommended_names, recommended_posters


# -----------------------------
# CUSTOM CSS
# -----------------------------
st.markdown("""
<style>
.main {
    background-color: #0E1117;
}

h1 {
    text-align: center;
    color: #FF4B4B;
}

.movie-title {
    text-align:center;
    font-weight:bold;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.title("🎬 Movie Recommendation System")
st.markdown(
    "<h4 style='text-align:center;'>Discover movies you'll love</h4>",
    unsafe_allow_html=True
)

st.divider()

# -----------------------------
# SELECT MOVIE
# -----------------------------
selected_movie = st.selectbox(
    "Choose a Movie",
    movies['title'].values
)

# -----------------------------
# RECOMMEND BUTTON
# -----------------------------
if st.button("🔍 Recommend Movies", use_container_width=True):

    names, posters = recommend(selected_movie)

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.image(posters[i])
            st.markdown(
                f"<p class='movie-title'>{names[i]}</p>",
                unsafe_allow_html=True
            )
