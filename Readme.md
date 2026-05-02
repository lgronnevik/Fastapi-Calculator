## User Authentication & Front-End Pages

- User registration and login are available at:
  - http://localhost:8000/register
  - http://localhost:8000/login
- These pages include client-side validation for email and password requirements.
- Upon successful registration or login, a JWT access token is stored in localStorage for authenticated API access.
- All user and calculation endpoints are protected with JWT authentication.

## Playwright E2E Tests for Auth

- End-to-end tests for registration and login flows are implemented using Playwright in `tests/test_e2e_auth.py`.
- These tests cover:
  - Successful registration and login
  - Validation errors (e.g., short password)
  - Error handling for invalid credentials
- To run only the auth E2E tests:

```sh
pytest tests/test_e2e_auth.py
```

# FastAPI Calculator

FastAPI-based calculator supporting add, subtract, multiply, divide, and exponentiation.  
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

To run all tests locally:

```sh
pytest
```

To run only Playwright end-to-end tests:

```sh
pytest tests/test_e2e.py
```

> **Note:**  
> This project includes unit tests for calculation logic, validation, and a factory pattern, as well as integration tests for the Calculation model and database. All tests are run automatically in CI/CD.

## Logging

- API calls and operations are logged  
- Division by zero triggers an error log

## Docker

Build and run with Docker Compose:

```sh
docker-compose up --build
```

The app will be available at http://localhost:8000 and docs at http://localhost:8000/docs

## CI/CD Pipeline

- GitHub Actions runs all tests on every push to the main branch.
- If tests pass, the workflow builds and pushes the Docker image to Docker Hub: `lgronnevik/fastapi-calculator`.
- The pipeline uses a Postgres service for integration tests.


## Docker Hub Repository

Your Docker image is automatically pushed to Docker Hub by the CI/CD pipeline:

- [View on Docker Hub](https://hub.docker.com/r/lgronnevik/fastapi-calculator)

## Integration Tests & OpenAPI

- To run all integration tests locally: `pytest`
- To manually check endpoints, visit [http://localhost:8000/docs](http://localhost:8000/docs) after starting the app.
- All endpoints (user registration/login, calculation BREAD) are documented and testable in the OpenAPI UI.

## Calculation BREAD Operations

- Browse, Read, Edit, Add, and Delete calculations for the logged-in user.
- All calculation endpoints are protected and user-specific.
- Front-end pages for all calculation operations are available at http://localhost:8000/calculations (after login).

## Running the Application

1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Start the server:
   ```sh
   uvicorn app.main:app --reload
   ```
3. Visit http://localhost:8000/register to create a user, then log in and access calculations.

## Running Tests

- Run all tests (unit, integration, E2E):
  ```sh
  pytest
  ```
- Run Playwright E2E tests:
  ```sh
  pytest tests/test_calculations_e2e.py
  ```

## Docker & CI/CD

- The project includes a Dockerfile and docker-compose.yml for containerization.
- GitHub Actions workflow automatically runs tests and pushes the Docker image to Docker Hub on each push to main.
- Set `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` as GitHub repository secrets for Docker image publishing.

## Docker Hub

- Docker image: https://hub.docker.com/repository/docker/lgronnevik/fastapi-calculator

## New Feature: Exponentiation

- The calculator now supports exponentiation (a^b) in addition to add, subtract, multiply, and divide.
- To use exponentiation, select "Exponentiation" from the calculation type dropdown on the Add Calculation page.
- The backend, API, and front-end all support this operation.
- Unit and integration tests for exponentiation are included and passing.

