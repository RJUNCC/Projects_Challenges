# # Use an official Python runtime as a parent image
# FROM python:3.11-slim

# # Set the working directory in the container
# WORKDIR /app

# # Copy the current directory contents into the container at /app
# COPY . .

# # Install system dependencies
# RUN apt-get update && apt-get install -y \
#     curl \
#     && rm -rf /var/lib/apt/lists/*

# # Install Poetry
# RUN curl -sSL https://install.python-poetry.org | python -
# # Use poetry to install Python dependencies
# RUN poetry install

# # Specify the command to run on container start
# CMD ["python", "tpy1.py"]

FROM python:3.11.5-slim-bookworm

ARG TPY1_ENV

ENV TPY1_ENV=${TPY1_ENV} \
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

# System deps:
RUN curl -sSL https://install.python-poetry.org | python3 -

# Copy only requirements to cache them in docker layer
WORKDIR /code
COPY poetry.lock pyproject.toml /code/

# Project initialization:
RUN poetry install $(test "$TPY1_ENV" == production && echo "--only=main") --no-interaction --no-ansi

# Creating folders, and files for a project:
COPY . /code