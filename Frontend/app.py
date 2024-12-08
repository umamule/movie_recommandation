import pickle
import streamlit as st
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

# Add responsive CSS styling
st.markdown(
    """
    <style>
    .main {
        background-color: #f0f0f0;
        padding: 20px;
        font-family: Arial, sans-serif;
    }
    .header {
        font-size: 2.5em;
        color: #333;
        text-align: center;
        margin-bottom: 20px;
        font-weight: bold;
    }
    .movie-title {
        font-size: 1.2em;
        color: #444;
        text-align: center;
        margin-top: 10px;
        font-weight: bold;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 24px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stSelectbox>div {
        background-color: #fff;
        border: 1px solid #ccc;
        border-radius: 4px;
        padding: 10px;
        font-size: 16px;
    }
    .flex-container {
        display: flex;
        justify-content: space-between;
        flex-wrap: wrap;
    }
    .flex-item {
        flex: 1 1 48%; /* Adjust the size of the divs */
        margin: 10px;
        text-align: center;
    }
    .flex-item img {
        max-width: 100%;
        height: auto;
        border-radius: 8px;
    }
    @media (max-width: 768px) {
        .flex-item {
            flex: 1 1 100%; /* Full width on smaller screens */
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="header">Movie Recommender System</div>', unsafe_allow_html=True)
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    st.markdown('<div class="flex-container">', unsafe_allow_html=True)
    for name, poster in zip(recommended_movie_names, recommended_movie_posters):
        st.markdown(
            f"""
            <div class="flex-item">
                <div class="movie-title">{name}</div>
                <img src="{poster}" alt="{name}">
            </div>
            """,
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)
