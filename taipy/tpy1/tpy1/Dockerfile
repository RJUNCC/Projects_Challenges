# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

# Use poetry to install Python dependencies
RUN /root/.poetry/bin/poetry config virtualenvs.create false \
    && /root/.poetry/bin/poetry install --no-interaction --no-ansi

# Specify the command to run on container start
CMD ["python", "tpy1.py"]