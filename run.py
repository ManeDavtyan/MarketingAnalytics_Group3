# before the model is corrected, run this after commenting model in api/init and bookstore/init
from bookstore.api.api import app

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
