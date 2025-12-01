# Use a Python base image (Python 3.13 is your current version)
FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies needed by Pillow (libjpeg-dev)
RUN apt-get update && apt-get install -y libjpeg-dev

# Copy the requirements file and install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the remaining project code
COPY backend /app/backend
COPY static /app/static

# Expose the port (Render handles mapping this)
EXPOSE 8000

# Define the command to run the application using Gunicorn
CMD ["gunicorn", "backend.app:app", "--bind", "0.0.0.0:8000"]
