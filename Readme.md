# FastAPI Calculator

FastAPI-based calculator supporting add, subtract, multiply, divide.  
Includes logging, unit tests, integration tests, and Playwright end-to-end tests.

## Project Structure

app/
  main.py
  operations.py
tests/
  test_operations.py
  test_api.py
  test_e2e.py
requirements.txt
.github/workflows/ci.yml

## Setup & Run

git clone <your-repo-link>
cd Fastapi-Calculator
python -m venv venv
.\venv\Scripts\activate   # Windows
pip install -r requirements.txt
pip install playwright
playwright install
uvicorn app.main:app --reload

Open http://127.0.0.1:8000 and http://127.0.0.1:8000/docs

## Tests

pytest                 # Run all tests
pytest tests/test_e2e.py  # Run only Playwright tests

## Logging

- API calls and operations are logged  
- Division by zero triggers an error log

## CI

GitHub Actions runs all tests on push to main branch.