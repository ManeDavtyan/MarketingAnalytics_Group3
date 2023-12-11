# Book Recommendation Package 

## Problem Statement

The main objective of this project is to create an advanced book recommendation system that can be offered to book sellers, such as Bookinist and Zangak, operating in Armenia. Currently, both book sellers lack a comprehensive recommendation system, which hinders their ability to provide tailored book suggestions to customers. The challenges and limitations in this context include:

- **Absence of Recommendation Systems:** Bookinist and Zangak currently do not have any recommendation systems in place, which leaves customers without guidance in discovering books that align with their preferences and needs. Of course, both have in-store assistants, but sometimes the lack of knowledge of sellers brings difficulties to the companies.

- **Customer Engagement:** The absence of effective book recommendations results in reduced customer engagement and may lead to missed sales opportunities for both book sellers.

- **Competitiveness:** In a competitive book market, the absence of a recommendation system puts Bookinist and Zangak at a disadvantage compared to online retailers that offer sophisticated recommendation algorithms.

- **Limited Data Utilization:** Both book sellers have access to valuable customer data, including purchase history and browsing behavior, which is currently underutilized for improving customer experience and increasing sales.

## Objective

**Recommendation System Development:** After addressing the initial challenges, proceed to develop an advanced recommendation system for books that can be utilized by Bookinist and Zangak. The development of the recommendation system can be broken down into the following steps:

a. **Data Gathering or Generation:** Collect a diverse and extensive dataset of books, including their titles, authors, genres, publication dates, descriptions, customer ratings, and any other relevant information. This dataset will serve as the foundation for generating recommendations.

b. **Data Analysis:** Conduct a thorough analysis of the collected data to understand patterns, trends, and correlations. This analysis will help identify key features and factors that influence book recommendations.

c. **Characterizing Books Based on Various Features:** Develop algorithms and models to characterize books based on a wide range of features, including genre, author, language, historical context, themes, and customer preferences. Implement natural language processing (NLP) techniques to extract insights from book descriptions and reviews.

**Dashboard Development:** Create a user-friendly dashboard that serves as the interface for inputting a book title and receiving similar book recommendations. The dashboard should be accessible to both customers and book sellers and should include features such as search functionality, user profiles for personalization, and feedback mechanisms for continuous improvement.

**API Development:** Create a fast and efficient API (Application Programming Interface) that accepts a book title as input and returns a list of similar books as output. This API will serve as the core engine for the book recommendation system.

## Goals

- **Marketing Integration:** Integrate the recommendation system into Bookinist's and Zangak's marketing efforts. Use it to suggest new releases, promotions, and special offers to customers, thereby enhancing sales and customer engagement.

- **Customer Feedback Integration:** Develop mechanisms for collecting and analyzing customer feedback on recommended books. Use this feedback to continually improve the recommendation algorithm and book inventory, aligning with evolving customer preferences.

To sum up, developing an intelligent book recommendation system for Bookinist and Zangak is an important project that addresses the lack of recommendation systems that current Armenian booksellers experience. The project's goals include collecting data and developing a plan, customizing it, and implementing an intuitive user interface. The objectives are to ensure that the recommendation system increases sales, improves customer engagement, and makes book dealers in the Armenian market more competitive.

## Data/Database

The project provides freedom to the user, book store owner, or just a random person, to create a database. Initially, the repository includes `data` folder with 7 csv files that were scrapped and generated. Those files (not mandatory) are later used  in `BookStore.db` creation. The user, of course, can specify their own data set, and fill out the database using bookrec.db subpackage. Take a look at the script below, it creates a database using csv files provided and the `bookrec` package. 
```{python}
import pandas as pd
from bookrec import db

authors = pd.read_csv(".//data//authors.csv")
books = pd.read_csv(".//data//books.csv")
customers = pd.read_csv(".//data//customers.csv")
inventory= pd.read_csv(".//data//inventory.csv")
orderitem = pd.read_csv(".//data//orderitem.csv")
orders = pd.read_csv(".//data//orders.csv")
publishers = pd.read_csv(".//data//publishers.csv")

db.schema.create_database(authors, books, customers, inventory, orderitem, orders, publishers)
```
The system works specifically for book stores, that's why initially the database is named as `BookStore.db`. Later on, this data base will be used in recommendation model and API Swagger demonstration. Again, the user is free to build the database on his/her own data files, though we initially provide data files scrapped from https://zangakbookstore.am/.  

## API Interface

FastAPI package is used for an intuitive interface allowing customers and bookstore owners to request books, adjust data, or add new books. Besides GET, POST, PUT methods, the Swagger dashboard also provides another additional GET statement, used for printing recommended books. Basically, bookrec.model subpackage is connected to the bookrec.api subpackage, and while calling the api subpackage, the program automatically calls the model subpackage and recommends the books for the customer. You can use the api subpackage by simply running `run.py` file, or the script below.
```{python}
from bookrec.api.api import app

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
```
Make sure you have all packages downloaded in your venv, by installing requirements.txt.

## Model

#### Matrix Factorization Model 
The model subpackage within the package is dedicated to handling the book recommendation aspect. This submodule employs a Matrix Factorization Model and implements a recommendation system based on cosine similarity string distances.

When interacting with the bookrec.model subpackage, users are prompted to provide a book title. If the specified book title exists in the BookStore.db database, the system responds by presenting five new recommended books.

To use the recommendation model, the following Python script can be employed:

```{python}
from bookrec.model import model
db_path = './/BookStore.db'
title_to_recommend = input("Enter a book title: ")
recommendations = model.get_combined_recommendations(title_to_recommend, db_path)

print(recommendations)
```
Feel free to incorporate this script into your application to leverage the book recommendation functionality provided by the Matrix Factorization Model!