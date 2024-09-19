# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt first (to leverage Docker's caching feature)
COPY requirements.txt requirements.txt

# Install any necessary dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the Flask app's port (5000 by default)
EXPOSE 5000

# Set the environment variable to define Flask app
ENV FLASK_APP=app.py

# Command to run the Flask app when the container starts
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]



#This Dockerfile is set to:

#    Use Python 3.10.
#    Set the working directory in the container to /app.
#    Install dependencies from requirements.txt.
#    Expose port 5000 to run the Flask app.
#    Use Flask’s built-in server to run the app, binding to all network interfaces (0.0.0.0).
