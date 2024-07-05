# Use an official Python runtime as a parent image
FROM python:3.12.3-slim

# Set the working directory
WORKDIR /app

# Install dependencies
RUN apt-get update \
    && apt-get install -y postgresql-dev gcc python3-dev musl-dev

# Copy the requirements file and install Python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt \
    && rm -rf /tmp

# Copy the current directory contents into the container at /app
COPY . .

# Define environment variable
ENV FLASK_APP=app.py
ENV PORT 5000

# Expose the port the app runs on
EXPOSE $PORT

# Run the application
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
