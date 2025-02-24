# Use Python 3.12 as the base image
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy the application code to the container
COPY . /app/

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install -r requirements.txt

# Expose the port for Django
EXPOSE 8000

# Run database migrations and start the server
CMD ["sh", "-c", "
    python manage.py makemigrations RAG_CHATBOT_BACKEND_APIS &&
    python manage.py migrate &&
    python manage.py seed_data &&
    python manage.py runserver 0.0.0.0:8000
"]
