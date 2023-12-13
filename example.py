
# uncomment the below code to create DB

# from bookrecs import db
# import pandas as pd
# #
# authors = pd.read_csv(".//data//authors.csv")
# books = pd.read_csv(".//data//books.csv")
# customers = pd.read_csv(".//data//customers.csv")
# inventory= pd.read_csv(".//data//inventory.csv")
# orderitem = pd.read_csv(".//data//orderitem.csv")
# orders = pd.read_csv(".//data//orders.csv")
# publishers = pd.read_csv(".//data//publishers.csv")
#
# db.schema.create_database(authors, books, customers, inventory, orderitem, orders, publishers)


# uncomment the below code to run API Swagger

# API
# from bookrecs.api.api import app
#
# if __name__ == "__main__":
#     import uvicorn
#
#     uvicorn.run(app, host="127.0.0.1", port=8000)



# uncomment the below code to recommend books

# from bookrecs.model import model
# db_path = './/BookStore.db'
# title_to_recommend = input("Enter a book title: ")
# recommendations = model.get_combined_recommendations(title_to_recommend, db_path)
#
# recommendations
