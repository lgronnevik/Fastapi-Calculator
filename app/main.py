from fastapi import FastAPI, HTTPException
import logging
from app.operations import add, subtract, multiply, divide  # use absolute import

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="FastAPI Calculator")

@app.get("/")
def home():
    return {"message": "FastAPI Calculator Running"}

@app.post("/add")
def add_numbers(a: float, b: float):
    return {"result": add(a, b)}

@app.post("/subtract")
def subtract_numbers(a: float, b: float):
    return {"result": subtract(a, b)}

@app.post("/multiply")
def multiply_numbers(a: float, b: float):
    return {"result": multiply(a, b)}

@app.post("/divide")
def divide_numbers(a: float, b: float):
    try:
        return {"result": divide(a, b)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))