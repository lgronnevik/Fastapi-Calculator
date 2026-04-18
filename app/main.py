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
# User Registration Endpoint
@app.post("/users/register", response_model=schemas.UserRead)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    logging.info(f"Registering user: {user.username}")
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
    logging.info(f"User registered: {user.username}")
    return new_user

# User Login Endpoint
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm

@app.post("/users/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    return {"message": "Login successful", "username": user.username, "email": user.email}

# ----------------------
# CALCULATION ROUTES (BREAD)
# ----------------------
from typing import List

# Browse all calculations
@app.get("/calculations", response_model=List[schemas.CalculationRead])
def browse_calculations(db: Session = Depends(get_db)):
    return db.query(models.Calculation).all()

# Read a specific calculation
@app.get("/calculations/{calc_id}", response_model=schemas.CalculationRead)
def read_calculation(calc_id: int, db: Session = Depends(get_db)):
    calculation = db.query(models.Calculation).filter(models.Calculation.id == calc_id).first()
    if not calculation:
        raise HTTPException(status_code=404, detail="Calculation not found")
    return calculation

# Add a new calculation
@app.post("/calculations", response_model=schemas.CalculationRead)
def add_calculation(calc: schemas.CalculationCreate, db: Session = Depends(get_db)):
    # Perform calculation
    if calc.type == "Add":
        result = calc.a + calc.b
    elif calc.type == "Sub":
        result = calc.a - calc.b
    elif calc.type == "Multiply":
        result = calc.a * calc.b
    elif calc.type == "Divide":
        if calc.b == 0:
            raise HTTPException(status_code=400, detail="Division by zero is not allowed.")
        result = calc.a / calc.b
    else:
        raise HTTPException(status_code=400, detail="Invalid calculation type")
    new_calc = models.Calculation(
        a=calc.a,
        b=calc.b,
        type=calc.type,
        result=result
    )
    db.add(new_calc)
    db.commit()
    db.refresh(new_calc)
    return new_calc

# Edit (update) a calculation
@app.put("/calculations/{calc_id}", response_model=schemas.CalculationRead)
def edit_calculation(calc_id: int, calc: schemas.CalculationCreate, db: Session = Depends(get_db)):
    calculation = db.query(models.Calculation).filter(models.Calculation.id == calc_id).first()
    if not calculation:
        raise HTTPException(status_code=404, detail="Calculation not found")
    # Update fields
    calculation.a = calc.a
    calculation.b = calc.b
    calculation.type = calc.type
    # Recalculate result
    if calc.type == "Add":
        calculation.result = calc.a + calc.b
    elif calc.type == "Sub":
        calculation.result = calc.a - calc.b
    elif calc.type == "Multiply":
        calculation.result = calc.a * calc.b
    elif calc.type == "Divide":
        if calc.b == 0:
            raise HTTPException(status_code=400, detail="Division by zero is not allowed.")
        calculation.result = calc.a / calc.b
    else:
        raise HTTPException(status_code=400, detail="Invalid calculation type")
    db.commit()
    db.refresh(calculation)
    return calculation

# Delete a calculation
@app.delete("/calculations/{calc_id}")
def delete_calculation(calc_id: int, db: Session = Depends(get_db)):
    calculation = db.query(models.Calculation).filter(models.Calculation.id == calc_id).first()
    if not calculation:
        raise HTTPException(status_code=404, detail="Calculation not found")
    db.delete(calculation)
    db.commit()
    return {"detail": "Calculation deleted"}