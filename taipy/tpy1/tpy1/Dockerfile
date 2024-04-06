FROM python:3.11.5-slim-bookworm

ARG POETRY_DS

ENV POETRY_DS=${POETRY_DS} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # Poetry's configuration:
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local' \
  POETRY_VERSION=1.8.2
# ^^^
# Make sure to update it!

RUN pip install poetry

# System deps:
RUN curl -sSL https://install.python-poetry.org | python3 -

# Copy only requirements to cache them in docker layer
WORKDIR /app
COPY poetry.lock pyproject.toml /app/
COPY tpy1/dashboard.py /app/

# Project initialization:
RUN poetry install $(test "$POETRY_DS" == production && echo "--only=main") --no-interaction --no-ansi

# Creating folders, and files for a project:
COPY . /code