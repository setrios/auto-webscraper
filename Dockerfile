FROM python:3.13.11-slim-trixie

# Set environment variables
# PIP_DISABLE_PIP_VERSION_CHECK disables an automatic check for pip updates each time
# PYTHONDONTWRITEBYTECODE means Python will not try to write .pyc files | cache
# PYTHONUNBUFFERED ensures our console output is not buffered by Docker
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory | just to use relative path
WORKDIR /code

# Install Firefox, geckodriver, and required dependencies
RUN apt-get update && apt-get install -y firefox-esr

# Install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy entire project to container
COPY . .