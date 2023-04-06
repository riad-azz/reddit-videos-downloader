# Use an official Python runtime as a parent image
FROM python:latest

# Install FFmpeg
RUN apt-get -y update
RUN apt-get install -y ffmpeg

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install gunicorn
RUN pip install gunicorn

# Expose port 5000 for the Flask app
EXPOSE 5000

# Start the Flask app
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi.wsgi:app"]