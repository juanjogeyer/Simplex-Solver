from fastapi import FastAPI
from routers import simplex

app = FastAPI()

app.include_router(simplex)

@app.get("/")
def read_root():
    return "hola mundo"
