# Use official Python runtime as a base image
FROM python:3.8-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the application code into the container
COPY . /app/

RUN pip install -r requirements.txt

# Expose port 5000 to the outside world
EXPOSE 5000

# Command to run the Flask application
CMD ["python", "app.py"]
