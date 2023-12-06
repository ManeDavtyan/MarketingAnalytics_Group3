# Book Recommendation System

## Problem Statement

This project aims to develop a sophisticated book recommendation system for Armenian book sellers, Bookinisk, Zangak and more. Current challenges include the absence of recommendation systems, leading to reduced customer engagement and a competitive disadvantage. This project is basically about a `bookstore` python package creation, which is an outstanding package, useful for user interaction in book recommendation process. 
### Objectives

1. **Recommendation System Development:**
   - Data gathering and analysis.
   - Characterizing books using various features.
   - Dashboard and API development.

2. **Goals:**
   - Marketing integration for promotions.
   - Customer feedback integration for continuous improvement.

## Data/Database

The project provides freedom to the user, book store owner, or just a random person, to create a database. Initially, the repository includes `data` folder with 7 csv files that were scrapped and generated. Those files are later used in `example.ipynb` for  `BookStore.db` creation. The user, of course, can specify their own data set, and fill out the database using bookstore.db subpackage. The system works specifically for book stores, that's why initially the database is named as `BookStore.db` and if you run the example.py with the script below, it will create `BookStore.db` in th current working directory. Later on, this data base will be used for recommendation and API Swagger demonstration. Again, the user is free to build the database on his/her own data files, though we initially provide data files scrapped from https://zangakbookstore.am/.  

```{python }
import pandas as pd
from bookstore import db

authors = pd.read_csv(".//data//authors.csv")
books = pd.read_csv(".//data//books.csv")
customers = pd.read_csv(".//data//customers.csv")
inventory= pd.read_csv(".//data//inventory.csv")
orderitem = pd.read_csv(".//data//orderitem.csv")
orders = pd.read_csv(".//data//orders.csv")
publishers = pd.read_csv(".//data//publishers.csv")

db.schema.create_database(authors, books, customers, inventory, orderitem, orders, publishers)

```

## API Interface

FastAPI is used for an intuitive interface allowing customers and bookstore owners to request books, adjust data, or add new books. Besides GET, POST, PUT methods, the Swagger dashboard also provides another additional GET statement, used for printing recommended books. Basically, bookstore.model subpackage is connected to the bookstore.api subpackage, and while calling the api subpackage, the program automatically call the model subpackage and recommends the books for the customer. You can use the api subpackage by simply running `run.py` file. 

```{python }
from bookstore.api.api import app

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)

```

## Models

### Matrix Factorization Model (model.py)

The `model.py` file implements a recommendation system using .... The model does can be called outside the package in the following way. (see `example.ipynb`)

```{python}
#model part
```




