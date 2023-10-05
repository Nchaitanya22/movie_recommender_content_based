import pickle
import streamlit as st
import requests

# Function to fetch a movie poster by title using the OMDB API
def fetch_movie_poster(title):
    api_key = 'f4acb996'  # Replace with your actual OMDB API key
    url = f"http://www.omdbapi.com/?t={title}&apikey={api_key}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'Poster' in data:
                return data['Poster']
            else:
                return None
        else:
            return None
    except Exception as e:
        return None

def recommend(movie):
    index = movies[movies['Title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    for i in distances[1:6]:
        recommended_movie_title = movies.iloc[i[0]].Title
        recommended_movie_poster = fetch_movie_poster(recommended_movie_title)
        recommended_movies.append((recommended_movie_title, recommended_movie_poster))
    return recommended_movies

st.header('Movie Recommender System')
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_list = movies['Title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movies = recommend(selected_movie)
    cols= st.columns(5)
    for i, (movie_title, movie_poster) in enumerate(recommended_movies):
        with cols[i]:
            st.text(movie_title)
            if movie_poster:
                st.image(movie_poster)
