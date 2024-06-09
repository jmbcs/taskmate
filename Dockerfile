# Use an official Python runtime as a parent image
FROM python:3.12 

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


# Run database migrations
RUN python todo_app/manage.py makemigrations && \
    python todo_app/manage.py migrate

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["python", "todo_app/manage.py", "runserver", "0.0.0.0:8000"]
