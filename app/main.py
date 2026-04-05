from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import logging

from app.operations import add, subtract, multiply, divide
from app import models, schemas, database, auth

# Configure logging
logging.basicConfig(level=logging.INFO)

# Create DB tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="FastAPI Calculator")

# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----------------------
# BASIC ROUTE
# ----------------------
@app.get("/")
def home():
    logging.info("Home route accessed")
    return {"message": "FastAPI Calculator Running"}

# ----------------------
# CALCULATOR ROUTES
# ----------------------
@app.post("/add")
def add_numbers(a: float, b: float):
    logging.info(f"Add: {a} + {b}")
    return {"result": add(a, b)}

@app.post("/subtract")
def subtract_numbers(a: float, b: float):
    logging.info(f"Subtract: {a} - {b}")
    return {"result": subtract(a, b)}

@app.post("/multiply")
def multiply_numbers(a: float, b: float):
    logging.info(f"Multiply: {a} * {b}")
    return {"result": multiply(a, b)}

@app.post("/divide")
def divide_numbers(a: float, b: float):
    logging.info(f"Divide: {a} / {b}")
    try:
        return {"result": divide(a, b)}
    except ValueError as e:
        logging.error(f"Division error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

# ----------------------
# USER ROUTES (NEW)
# ----------------------
@app.post("/users/", response_model=schemas.UserRead)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    logging.info(f"Creating user: {user.username}")

    existing_user = db.query(models.User).filter(
        (models.User.username == user.username) |
        (models.User.email == user.email)
    ).first()

    if existing_user:
        logging.warning("User already exists")
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = auth.hash_password(user.password)

    new_user = models.User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    logging.info(f"User created: {user.username}")

    return new_user