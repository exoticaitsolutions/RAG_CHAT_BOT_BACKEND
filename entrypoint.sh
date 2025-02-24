#!/bin/sh

# Database connection test (optional but recommended)
echo "Testing database connection..."
python manage.py check --database default

if [ $? -ne 0 ]; then
  echo "Database connection failed. Exiting..."
  exit 1
fi

# Check if migrations have already been applied
if [ ! -f "/app/db_initialized" ]; then
    echo "First-time setup: Applying database migrations..."
    python manage.py makemigrations
    python manage.py migrate

    # Create a flag file to indicate that migrations have been applied
    touch /app/db_initialized
else
    echo "Migrations already applied, skipping..."
fi

# Collect static files (for production)
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start the Django server (development) or Gunicorn (production)
echo "Starting Django server..."
exec python manage.py runserver 0.0.0.0:8000 #For development

#For production use this instead of the runserver command above.
#exec gunicorn rag_app_portal.wsgi:application --bind 0.0.0.0:8000