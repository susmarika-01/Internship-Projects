import streamlit as st
import pickle
import pandas as pd

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = list(enumerate(similarity[index]))
    distances = sorted(distances, reverse=True, key=lambda x: x[1])
    recommended_movies = []
    for i in distances[1:6]:
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies

movies_dict = pickle.load(open("movies.dict.pkl","rb"))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))

st.set_page_config(page_title="Movie Recommender", layout="wide")

st.markdown(
    """
    <div style="
        text-align:center; 
        background: linear-gradient(90deg, #4b6cb7, #182848);
        padding:30px; 
        border-radius:15px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.2);
        color: white;
    ">
        <h1 style="margin-bottom:5px;">🎬 Movie Recommender System</h1>
        <p style="font-size:18px; margin-top:0;">Discover movies similar to your favorites</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")

st.markdown(
    "<h3 style='text-align:center; color:#182848; margin-top:30px;'>Your Favourite Movie:</h3>",
    unsafe_allow_html=True
)

selected_movie = st.selectbox(
    '',
    movies['title'].values,
    label_visibility="collapsed"
)

st.write("")

st.markdown(
    """
    <style>
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #4b6cb7, #182848);
        color: white;
        height: 50px;
        width: 300px;
        border-radius: 10px;
        border: none;
        font-size: 18px;
        font-weight: bold;
        cursor: pointer;
        transition: transform 0.2s, background 0.3s;
        display: block;
        margin: 0 auto;
    }
    div.stButton > button:first-child:hover {
        transform: scale(1.05);
    }
    </style>
    """,
    unsafe_allow_html=True
)

if st.button("Get Recommendations", key="rec_btn"):
    recommendations = recommend(selected_movie)
    st.markdown(
        "<h3 style='text-align:center; color:#182848; margin-top:40px;'>Recommended Movies</h3>",
        unsafe_allow_html=True
    )
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        if idx < len(recommendations):
            movie_title = recommendations[idx]
            col.markdown(
                f"""
                <div style="
                    background-color:#e0e0eb; 
                    padding:20px; 
                    border-radius:12px; 
                    text-align:center; 
                    height:150px; 
                    display:flex; 
                    align-items:center; 
                    justify-content:center;
                    box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
                    font-size:16px;
                    color:#182848;
                ">
                    <strong>{movie_title}</strong>
                </div>
                """,
                unsafe_allow_html=True
            )
