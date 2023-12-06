import sqlite3
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.decomposition import TruncatedSVD

# Connect to the SQLite database
db_path = './/BookStore.db'
conn = sqlite3.connect(db_path)

books_query = "SELECT * FROM books"
books = pd.read_sql_query(books_query, conn)
conn.close()

# Combine titles into a single string
titles = books['title'].str.lower().str.replace('[^\w\s]', '', regex=True).str.split()
titles = titles.apply(lambda x: ' '.join(set(x)))  # Keep only unique words in each title

# Use Count Vectorizer
vectorizer = CountVectorizer()
title_matrix = vectorizer.fit_transform(titles)

# Compute cosine similarity for titles
cosine_sim_titles = linear_kernel(title_matrix, title_matrix)

def get_combined_recommendations(title, books_data):
    idx = books_data.loc[books_data['title'] == title].index[0]

    # Step 1: Check for title similarity
    title_sim_scores = list(enumerate(cosine_sim_titles[idx]))
    title_sim_scores = sorted(title_sim_scores, key=lambda x: x[1], reverse=True)

    # Filter out the input title
    title_sim_scores = [score for score in title_sim_scores if books_data.iloc[score[0]]['title'] != title]

    # If there are similar titles, recommend based on titles
    if title_sim_scores:
        title_indices = [i[0] for i in title_sim_scores[:5]]
        title_recommendations = books_data.iloc[title_indices].copy()
        return title_recommendations

    # Step 2: Check for the same author
    author = books_data.iloc[idx]['author']
    author_recommendations = books_data[books_data['author'] == author].head(5)
    if not author_recommendations.empty:
        return author_recommendations

    # Step 3: Check for the same genre and high rating
    genre = books_data.iloc[idx]['Genre']
    high_rated_genre_recommendations = books_data[(books_data['Genre'] == genre) & (books_data['Rating'] >= 4)].head(5)
    if not high_rated_genre_recommendations.empty:
        return high_rated_genre_recommendations

    # If no matches found, return an empty DataFrame
    return pd.DataFrame()

# Get user input for the book title
title_to_recommend = input("Enter a book title: ")
recommendations = get_combined_recommendations(title_to_recommend, books)
