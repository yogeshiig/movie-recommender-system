import pickle
import streamlit as st
import requests
import os

API_KEY = "abca3786961409a119bec8d11ac6e390"

# Function to fetch movie poster
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    data = requests.get(url)
    data = data.json()
    poster_path = data.get("poster_path", "")
    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    return ""  # Return empty string if poster_path is not found

# Function to load a model in chunks
def load_model_from_chunks(folder_path, filename):
    chunk_files = sorted([f for f in os.listdir(folder_path) if f.startswith(filename)])
    model_data = b""
    for chunk_file in chunk_files:
        with open(os.path.join(folder_path, chunk_file), "rb") as f:
            model_data += f.read()
    return pickle.loads(model_data)

# Recommendation function
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

# Streamlit app UI
st.header('Movie Recommender System')

# Load data from chunks
movies = load_model_from_chunks('models', 'movies')
similarity = load_model_from_chunks('models', 'similarity')

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
