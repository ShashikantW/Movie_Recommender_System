import numpy as np
import pandas as pd
import requests
import streamlit as st
import pickle

#function for fetching movie posters
#api key = e04810814a4a3ef4df973fb68b6acf55

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0"})


# function for the details of the movie
@st.cache_data
def movie_details(movie_id, retries=3):
    for attempt in range(retries):
        try:
            url = "https://api.themoviedb.org/3/movie/{}?api_key=e04810814a4a3ef4df973fb68b6acf55&language=en-US".format(
                movie_id
            )
            response = session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            poster_path = data.get("poster_path")
            poster_url = "https://image.tmdb.org/t/p/w500{}".format(poster_path) if poster_path \
                         else "https://via.placeholder.com/500x750?text=No+Poster"

            genres_list = data.get("genres", [])
            genres = ", ".join([g["name"] for g in genres_list]) if genres_list else "Unknown"

            return {
                "poster": poster_url,
                "release_date": data.get("release_date", "Unknown"),
                "overview": data.get("overview", "Description not available"),
                "rating": data.get("vote_average", "N/A"),
                "genres": genres,
            }

        except requests.exceptions.RequestException:
            if attempt < retries - 1:
                continue  # try again
            else:
                # return fallback/default data if all retries fail
                return {
                    "poster": "https://via.placeholder.com/500x750?text=No+Poster",
                    "release_date": "Unknown",
                    "overview": "Description not available",
                    "rating": "N/A",
                    "genres": "Unknown",
                }

#function for recommending movies
@st.cache_data
def recommend( movie ,n = 5 ):
    movie_idx = movies_list[movies_list['title'] == movie].index[0] #if I write 1 instead 0 it will give 2nd match instead 1st
    similarity_scores = cosine_similarity(tfidf[movie_idx], tfidf).flatten()

    movie_list_idx= np.argsort(similarity_scores)[::-1][1: n+1]

    recommended_movies = []
    for i in movie_list_idx:
        movie_id = movies_list.iloc[i].movie_id   #will fetch tmdb movie id
        title = movies_list.iloc[i].title
        details = movie_details(movie_id)
        recommended_movies.append({
            "title" : title,
            "poster": details["poster"],
            "release_date": details["release_date"],
            "overview": details["overview"],
            "rating": details["rating"],
            "genres": details["genres"],

        })
    return recommended_movies


#importinig movies list
movies_list = pickle.load(open('movies.pkl','rb'))

#importing tfidf
from sklearn.metrics.pairwise import cosine_similarity
tfidf = pickle.load(open('tfidf.pkl','rb'))


# ---------- UI ------------

#heading or title of the ui
st.title('Movie Recommendation System')

#we added column so we can get our name bar and number bar in same line and added number line so user can freely choose the length of recommendations
col1 , col2 = st.columns([4,1])

with col1:
    selected_movie_name = st.selectbox(
        'Enter Movie Name',
        movies_list['title'].values,
    )
with col2:
   num_recs = st.number_input(
      "No. of Recs", min_value=1, max_value=10, value=5, step=1,
   )


if st.button('Recommend'):

    recommendations = recommend(selected_movie_name , n = num_recs)
    st.subheader("Recommended Movies:")

    for idx, movie in enumerate(recommendations, 1):
        col1, col2 = st.columns([1, 3])  # left narrow, right wide
        with col1:
            st.image(movie["poster"], width=200)
        with col2:
            st.markdown("### {}. {}".format(idx, movie['title']))

            st.write("Release Date:", movie["release_date"])
            st.write("Rating:", movie["rating"])
            st.write("genres:", movie["genres"])
            #st.write(movie["overview"])

            short_overview = movie["overview"][:100] + "..." if len(movie["overview"]) > 100 else movie["overview"]
            st.write(short_overview)
            with st.expander("Read more"):
                st.write(movie["overview"])
