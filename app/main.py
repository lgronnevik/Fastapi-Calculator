from fastapi import FastAPI, HTTPException, Depends, Request, Form, status
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import os
from sqlalchemy.orm import Session
import logging
from app.operations import add, subtract, multiply, divide
from app import models, schemas, database, auth
from app.schemas import CalculationCreate, CalculationUpdate

app = FastAPI(title="FastAPI Calculator")


# Configure logging
logging.basicConfig(level=logging.INFO)

# Create DB tables
models.Base.metadata.create_all(bind=database.engine)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "..", "templates"))

# Dependency to get DB session (must be above all endpoints)
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----------------------
# CALCULATION API ROUTES (JSON, for tests)
# ----------------------
# Create calculation
@app.post("/api/calculations", response_model=schemas.CalculationRead)
def api_create_calculation(calc: CalculationCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    # Validate type
    if calc.type not in ["Add", "Sub", "Multiply", "Divide"]:
        return JSONResponse(status_code=422, content={"detail": [{"msg": "Invalid calculation type"}]})
    if calc.type == "Divide" and calc.b == 0:
        return JSONResponse(status_code=422, content={"detail": [{"msg": "Division by zero"}]})
    if calc.type == "Add":
        result = calc.a + calc.b
    elif calc.type == "Sub":
        result = calc.a - calc.b
    elif calc.type == "Multiply":
        result = calc.a * calc.b
    elif calc.type == "Divide":
        result = calc.a / calc.b
    new_calc = models.Calculation(a=calc.a, b=calc.b, type=calc.type, result=result, user_id=current_user.id)
    db.add(new_calc)
    db.commit()
    db.refresh(new_calc)
    return new_calc

@app.get("/api/calculations/{calc_id}", response_model=schemas.CalculationRead)
def api_get_calculation(calc_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    calc = db.query(models.Calculation).filter(models.Calculation.id == calc_id, models.Calculation.user_id == current_user.id).first()
    if not calc:
        return JSONResponse(status_code=404, content={"detail": "Calculation not found"})
    return calc

@app.put("/api/calculations/{calc_id}", response_model=schemas.CalculationRead)
def api_update_calculation(calc_id: int, update: CalculationUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    calc = db.query(models.Calculation).filter(models.Calculation.id == calc_id, models.Calculation.user_id == current_user.id).first()
    if not calc:
        return JSONResponse(status_code=404, content={"detail": "Calculation not found"})
    if update.type not in ["Add", "Sub", "Multiply", "Divide"]:
        return JSONResponse(status_code=422, content={"detail": [{"msg": "Invalid calculation type"}]})
    if update.type == "Divide" and update.b == 0:
        return JSONResponse(status_code=422, content={"detail": [{"msg": "Division by zero"}]})
    calc.a = update.a
    calc.b = update.b
    calc.type = update.type
    if update.type == "Add":
        calc.result = update.a + update.b
    elif update.type == "Sub":
        calc.result = update.a - update.b
    elif update.type == "Multiply":
        calc.result = update.a * update.b
    elif update.type == "Divide":
        calc.result = update.a / update.b
    db.commit()
    db.refresh(calc)
    return calc

# Delete calculation
@app.delete("/api/calculations/{calc_id}")
def api_delete_calculation(calc_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    calc = db.query(models.Calculation).filter(models.Calculation.id == calc_id, models.Calculation.user_id == current_user.id).first()
    if not calc:
        return JSONResponse(status_code=404, content={"detail": "Calculation not found"})
    db.delete(calc)
    db.commit()
    return {"detail": "Calculation deleted"}



# ----------------------
# FRONTEND ROUTES
# ----------------------
@app.get("/register", response_class=HTMLResponse)
def serve_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
def serve_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

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
# User Registration Endpoint (returns JWT)
@app.post("/register")
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
    # Create JWT
    access_token = auth.create_access_token({"sub": new_user.email})
    logging.info(f"User registered: {user.username}")
    return {"access_token": access_token, "token_type": "bearer"}

# User Login Endpoint
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm

# User Login Endpoint (returns JWT)
@app.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    access_token = auth.create_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# ----------------------
# CALCULATION FRONTEND ROUTES
# ----------------------
@app.get("/calculations", response_class=HTMLResponse)
def calculations_page(request: Request, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    calculations = db.query(models.Calculation).filter(models.Calculation.user_id == current_user.id).all()
    return templates.TemplateResponse("calculations.html", {"request": request, "calculations": calculations})

@app.get("/calculations/add", response_class=HTMLResponse)
def add_calculation_page(request: Request):
    return templates.TemplateResponse("add_calculation.html", {"request": request})

@app.post("/calculations/add", response_class=HTMLResponse)
def add_calculation_form(request: Request, a: float = Form(...), b: float = Form(...), type: str = Form(...), db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    # Validate type
    if type not in ["Add", "Sub", "Multiply", "Divide"]:
        return templates.TemplateResponse("add_calculation.html", {"request": request, "error": "Invalid operation type."})
    # Validate division by zero
    if type == "Divide" and b == 0:
        return templates.TemplateResponse("add_calculation.html", {"request": request, "error": "Division by zero is not allowed."})
    # Calculate result
    if type == "Add":
        result = a + b
    elif type == "Sub":
        result = a - b
    elif type == "Multiply":
        result = a * b
    elif type == "Divide":
        result = a / b
    new_calc = models.Calculation(a=a, b=b, type=type, result=result, user_id=current_user.id)
    db.add(new_calc)
    db.commit()
    return RedirectResponse("/calculations", status_code=303)

@app.get("/calculations/{calc_id}", response_class=HTMLResponse)
def calculation_detail_page(calc_id: int, request: Request, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    calc = db.query(models.Calculation).filter(models.Calculation.id == calc_id, models.Calculation.user_id == current_user.id).first()
    if not calc:
        return HTMLResponse("Calculation not found", status_code=404)
    return templates.TemplateResponse("calculation_detail.html", {"request": request, "calc": calc})

@app.get("/calculations/{calc_id}/edit", response_class=HTMLResponse)
def edit_calculation_page(calc_id: int, request: Request, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    calc = db.query(models.Calculation).filter(models.Calculation.id == calc_id, models.Calculation.user_id == current_user.id).first()
    if not calc:
        return HTMLResponse("Calculation not found", status_code=404)
    return templates.TemplateResponse("edit_calculation.html", {"request": request, "calc": calc})

@app.post("/calculations/{calc_id}/edit", response_class=HTMLResponse)
def edit_calculation_form(calc_id: int, request: Request, a: float = Form(...), b: float = Form(...), type: str = Form(...), db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    calc = db.query(models.Calculation).filter(models.Calculation.id == calc_id, models.Calculation.user_id == current_user.id).first()
    if not calc:
        return HTMLResponse("Calculation not found", status_code=404)
    if type not in ["Add", "Sub", "Multiply", "Divide"]:
        return templates.TemplateResponse("edit_calculation.html", {"request": request, "calc": calc, "error": "Invalid operation type."})
    if type == "Divide" and b == 0:
        return templates.TemplateResponse("edit_calculation.html", {"request": request, "calc": calc, "error": "Division by zero is not allowed."})
    calc.a = a
    calc.b = b
    calc.type = type
    if type == "Add":
        calc.result = a + b
    elif type == "Sub":
        calc.result = a - b
    elif type == "Multiply":
        calc.result = a * b
    elif type == "Divide":
        calc.result = a / b
    db.commit()
    return RedirectResponse(f"/calculations/{calc_id}", status_code=303)

@app.post("/calculations/{calc_id}/delete", response_class=HTMLResponse)
def delete_calculation_form(calc_id: int, request: Request, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    calc = db.query(models.Calculation).filter(models.Calculation.id == calc_id, models.Calculation.user_id == current_user.id).first()
    if not calc:
        return HTMLResponse("Calculation not found", status_code=404)
    db.delete(calc)
    db.commit()
    return RedirectResponse("/calculations", status_code=303)