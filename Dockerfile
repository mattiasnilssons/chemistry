# Use an official Python runtime as a parent image
FROM tiangolo/uvicorn-gunicorn:python3.11-slim as builder

# Set the working directory in the builder stage
WORKDIR /app

# Install poetry
RUN python -m pip install poetry

# Copy only the files needed for installing dependencies to avoid cache busting
COPY pyproject.toml poetry.lock ./

# Install dependencies using Poetry in a system-wide location
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Use a second stage to minimize the final image size
FROM tiangolo/uvicorn-gunicorn:python3.11-slim

# Prevent Python from writing pyc files to disc and buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

# Copy installed packages from builder to the final image
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Create a non-privileged user to run the application
RUN useradd --create-home appuser
USER appuser

# Set the working directory in the container
WORKDIR /app

# Copy the application code to the container (ensure the right application structure)
COPY src/ .

# Run the Uvicorn server
CMD ["uvicorn", "chemistry_calculator.api.main:app", "--host", "0.0.0.0", "--port", "8080"]
