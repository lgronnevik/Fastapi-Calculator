from fastapi import FastAPI, HTTPException
import logging
from app.operations import add, subtract, multiply, divide  # use absolute import

# Configure logging
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="FastAPI Calculator")

@app.get("/")
def home():
    logging.info("Home route accessed")
    return {"message": "FastAPI Calculator Running"}

@app.post("/add")
def add_numbers(a: float, b: float):
    logging.info(f"Received request to add {a} + {b}")
    return {"result": add(a, b)}

@app.post("/subtract")
def subtract_numbers(a: float, b: float):
    logging.info(f"Received request to subtract {a} - {b}")
    return {"result": subtract(a, b)}

@app.post("/multiply")
def multiply_numbers(a: float, b: float):
    logging.info(f"Received request to multiply {a} * {b}")
    return {"result": multiply(a, b)}

@app.post("/divide")
def divide_numbers(a: float, b: float):
    logging.info(f"Received request to divide {a} / {b}")
    try:
        return {"result": divide(a, b)}
    except ValueError as e:
        logging.error(f"Division error: {e}")
        raise HTTPException(status_code=400, detail=str(e))