# Points to base image to get started
FROM python:3.9-slim

# install everything in requirements.txt file
COPY . .
RUN pip3 install -r requirements.txt

# all commands after this line of code will be in this work directory
WORKDIR /app

# use linux package manager to install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# # create non-root user for more security
# RUN useradd --create-home appuser
# USER appuser


# RUN sudo chown -R riain .
# RUN pip freeze > requirements.txt

# Copy code on local machine to the image
# COPY /app/main.py .

# API_KEY now is an evironment variable 
# ENV API_KEY=news_article_env

# building web server people can connect to, which requires a port for ext traffic
# make port accessible
EXPOSE 8501

# command to start container
# CMD ["python3", "-m", "http.server", "8000"]

# add some metadata
# LABEL maintainer="Ryan Jacobs"
# LABEL version="1.0"
# LABEL description="News articles with sentiment analysis and noun word count."

# healthcheck to make sure its running properly
# HEALTHCHECK --interval=30s --timeout=10s \ 
# CMD curl -f http://localhost:8501/health || exit 1

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# if container needs to store data thats going to be used later or by multiple containers
# VOLUME /data

# pass/override args to command when running it
# ENTRYPOINT ["python3", "-m", "http.server"]
# CMD ["8000"]
ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]