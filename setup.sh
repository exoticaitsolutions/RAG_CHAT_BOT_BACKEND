#!/bin/bash
echo "Starting setup script..."

echo "Creating virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate


if [ $? -ne 0 ]; then
    echo "Failed to activate virtual environment."
    exit 1
fi

echo "Virtual environment activated."

echo
echo "Updating pip..."
pip install --upgrade pip setuptools wheel
echo


echo
echo "Installing required packages..."
pip install -r requirements.txt > pip_install_log.txt 2>&1
cat pip_install_log.txt

<<<<<<< HEAD

echo "Setup complete."
=======
# Check if .env file exists and is non-empty
if [ ! -s ".env" ]; then
    echo "Configuring environment variables..."
    read -p "Choose Database Type (mysql/sqlite): " DB_TYPE
    read -p "Enter Database Name: " DB_NAME
    read -p "Enter Database User (default: root): " DB_USER
    DB_USER=${DB_USER:-root}
    read -s -p "Enter Database Password: " DB_PASSWORD
    echo
    read -p "Enter Database Host (default: localhost): " DB_HOST
    DB_HOST=${DB_HOST:-localhost}
    DB_PORT=3306
    read -p "Enter OpenAI API Key: " OPENAI_API_KEY

    cat <<EOL > .env
DB_TYPE=$DB_TYPE
DB_NAME=$DB_NAME
DB_USER=$DB_USER
DB_PASSWORD=$DB_PASSWORD
DB_HOST=$DB_HOST
DB_PORT=$DB_PORT
OPENAI_API_KEY=$OPENAI_API_KEY
EOL

    echo ".env file created successfully."
else
    echo ".env file found. Skipping configuration."
fi

# Waiting for database configuration
echo "Configuring database..."
sleep 3

# Check MySQL database connection if .env exists
if [ -s ".env" ]; then
    source .env
    if [ "$DB_TYPE" = "mysql" ]; then
        if ! command -v mysql &> /dev/null; then
            echo "MySQL command not found. Please ensure MySQL is installed and in your PATH."
            exit 1
        fi

        mysql -u"$DB_USER" -p"$DB_PASSWORD" -h "$DB_HOST" -e "USE $DB_NAME;" 2>/dev/null
        if [ $? -ne 0 ]; then
            echo "Database connection failed. Please check your credentials."
            exit 1
        else
            echo "Database connected successfully."
        fi
    fi
else
    echo "Skipping database setup since .env is empty or missing."
fi
# Run Django migrations
echo "Running migrations..."
python manage.py makemigrations RAG_CHATBOT_BACKEND_APIS
python manage.py migrate
python manage.py seed_data
echo "Setup complete!"
>>>>>>> 4f2ff96ff6e59c1ed95fb7570ec6a2164f6e9406
