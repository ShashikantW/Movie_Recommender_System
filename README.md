## Live Demo
[Click here to view the app] 
(https://movierecommendersystem-cf3ssvmgl62tcqihp4pch9.streamlit.app/)

#  Movie Recommender System

A content-based movie recommendation system built with **Python, Pandas, NumPy, and Streamlit**.  
It uses **TF‑IDF vectorization** and **cosine similarity** on movie descriptions to suggest films similar to the one selected by the user.  
Movie posters and details are fetched live from the **TMDB API**.

##  Features
- Preprocessing of movie dataset using Jupyter Notebook (`preprocessing_MRSD.ipynb`)
- TF‑IDF vectorization for text-based similarity
- Cosine similarity to recommend top matching movies
- Interactive Streamlit web app for easy use
- Live movie posters, ratings, and overviews via TMDB API

##  Project Structure
- `preprocessing_MRSD.ipynb` → Data cleaning & TF‑IDF matrix creation
- `movies.pkl`, `tfidf.pkl`, `vectorizer.pkl` → Preprocessed files for fast loading
- `app.py` → Streamlit application
- `tmdb_5000_movies.csv`, `tmdb_5000_credits.csv` → Raw dataset


##  Tech Stack
- Python (NumPy, Pandas, Scikit-learn)
- Streamlit
- TMDB API

---

✨ *This project was developed collaboratively as part of an academic minor project, focusing on both technical execution and clear presentation.*
