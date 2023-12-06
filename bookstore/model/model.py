
import sqlite3
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.decomposition import TruncatedSVD

# Connect to the SQLite database
db_path = './/BookStore.db'
conn = sqlite3.connect(db_path)

books_query = "SELECT * FROM books"
books = pd.read_sql_query(books_query, conn)
conn.close()

# Preprocess the 'books' DataFrame
books['content'] = books['title'] + ' ' + books['author_id'].astype(str) + ' ' + books['Genre']

# TF-IDF Vectorization
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(books['content'])

# Include the 'rating' as a numerical feature
rating_matrix = books['Rating'].values.reshape(-1, 1)

combined_matrix = pd.concat([pd.DataFrame(tfidf_matrix.toarray()), pd.DataFrame(rating_matrix)], axis=1)

svd = TruncatedSVD(n_components=100)
tfidf_matrix_reduced = svd.fit_transform(tfidf_matrix)

# Compute cosine similarity
cosine_sim = linear_kernel(tfidf_matrix_reduced, tfidf_matrix_reduced)

def get_recommendations(title, books_data):
    idx = books_data.loc[books_data['title'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]  # Get top 5 similar books
    book_indices = [i[0] for i in sim_scores]
    recommended_books = books_data.iloc[book_indices].copy()  # Create a copy to avoid modifying the original DataFrame
    return recommended_books

# Get user input for the book title
title_to_recommend = input("Enter a book title: ")
recommendations = get_recommendations(title_to_recommend, books)

# Connect to the SQLite database again to save recommendations
conn = sqlite3.connect(db_path)

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Check if the Recommendations table already exists
check_table_query = "SELECT name FROM sqlite_master WHERE type='table' AND name='recommendations';"
cursor.execute(check_table_query)
table_exists = cursor.fetchone()

# Create the Recommendations table if it doesn't exist
if not table_exists:
    create_table_query = '''
    CREATE TABLE recommendations (
        input_book_title TEXT,
        recommended_book_title TEXT,
        author_id INTEGER,
        genre TEXT,
        price REAL,
        rating REAL,
        similarity_score REAL
    )
    '''
    try:
        cursor.execute(create_table_query)
        conn.commit()
    except sqlite3.OperationalError as e:
        print(f"Error creating table: {e}")

# Save recommendations to the database
try:
    if not recommendations.empty:
        # Convert 'author_id' to INTEGER before saving to the database
        recommendations['author_id'] = recommendations['author_id'].astype(int)

        recommendations.to_sql('recommendations', conn, if_exists='append', index=False)
        print("Recommendations saved to the database.")
    else:
        print("No recommendations to save.")
except Exception as e:
    print(f"Error saving recommendations to the database: {e}")

# Close the database connection
conn.close()
