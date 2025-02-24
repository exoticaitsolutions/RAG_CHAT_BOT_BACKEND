# Use official Python image
FROM python:3.13

# Set the working directory inside the container
WORKDIR /var/www/html

# Copy project files to the working directory
COPY . /var/www/html

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000
EXPOSE 8000

# Default command to run the Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
