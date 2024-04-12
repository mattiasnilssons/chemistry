FROM tiangolo/uvicorn-gunicorn:python3.11-slim as builder

RUN python -m pip install poetry
#RUN python -m pip install poetry && \
#    $POETRY_HOME/bin/pip install --user poetry-plugin

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
COPY pyproject.toml .
COPY poetry.lock .
RUN --mount=type=cache,target=/root/.cache/pip \
#    --mount=type=bind,source=pyproject.toml,target=/app/pyproject.toml \  this doesn't work on Cloud Build
#    --mount=type=bind,source=poetry.lock,target=/app/poetry.lock \  this doesn't work on Cloud Build
    poetry export --without-hashes --output requirements.txt && \
    python -m pip install -r requirements.txt

FROM tiangolo/uvicorn-gunicorn:python3.11-slim

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

COPY src /app

# Switch to the non-privileged user to run the application.
USER appuser

CMD ["uvicorn", "chemistry_calculator.api.main:app", "--host", "0.0.0.0", "--port", "8080"]
