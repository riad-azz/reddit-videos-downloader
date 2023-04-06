# Use an official Python runtime as a parent image
FROM python:latest

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install FFmpeg
RUN apt-get -y update
RUN apt-get install -y ffmpeg

# Set the working directory to /app
WORKDIR /code

# copy required dependencies
COPY ./requirements.txt .

# Intall packages
RUN pip install -r requirements.txt

# Install gunicorn
RUN pip install gunicorn

# Expose port 5000 for the Flask app
EXPOSE 5000

# Start the Flask app : gunicorn --bind 0.0.0.0:5000 wsgi.wsgi:app
# Copy project
COPY . .