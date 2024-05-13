# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the Flask application files into the container
COPY . .

# Install the required dependencies
RUN pip install flask flask-mysqldb

# Expose port 5003 to the outside world
EXPOSE 5003

# Specify the command to run the Flask application
CMD ["python", "informationapp.py"]
