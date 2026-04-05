FROM python:3.11

WORKDIR /app

# Copy only requirements first
COPY requirements.txt .



# Install build dependencies for bcrypt
RUN apt-get update && apt-get install -y build-essential python3-dev libffi-dev

# Upgrade pip and uninstall any broken bcrypt/passlib, then install correct versions
RUN pip install --upgrade pip
RUN pip uninstall -y bcrypt passlib || true
RUN pip install --no-cache-dir bcrypt==4.1.2 passlib[bcrypt]==1.7.4
# Install the rest of your requirements
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers for e2e tests
RUN pip install playwright && playwright install --with-deps

# Then copy the rest of your code
COPY . .

# Run FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]