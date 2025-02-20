@echo off
echo "Starting setup script..."

echo "Creating virtual environment..."
python.exe -m venv .venv

echo "Activating virtual environment in directory: %cd%"
echo "Activating virtual environment..."
call .\.venv\Scripts\activate.bat

if %errorlevel% neq 0 (
    echo "Failed to activate virtual environment."
    pause
    exit /b 1
)

echo "Virtual environment activated in directory: %cd%"

echo.
echo "Installing required packages..."
python.exe -m pip install --upgrade pip setuptools wheel
echo.

<<<<<<< HEAD
echo.
echo "Installing required packages..."
pip install -r requirements.txt > pip_install_log.txt 2>&1
type pip_install_log.txt

echo "Setup complete."
pause
=======
:: Update pip, setuptools, and wheel
echo Updating pip...
pip install --upgrade pip
:: Install required packages
echo Installing required packages...
pip install -r requirements.txt
:: Check if .env file exists and is non-empty
if not exist .env (
    echo Configuring environment variables...
    set /p DB_TYPE="Choose Database Type (mysql/sqlite): "
    set /p DB_NAME="Enter Database Name: "
    set /p DB_USER="Enter Database User (default: root): "
    if "%DB_USER%"=="" set DB_USER=root
    set /p DB_PASSWORD="Enter Database Password: "
    set /p DB_HOST="Enter Database Host (default: localhost): "
    if "%DB_HOST%"=="" set DB_HOST=localhost
    set DB_PORT=3306
    set /p OPENAI_API_KEY="Enter OpenAI API Key: "
    set BASE_APP_URL=http://127.0.0.1:8000


    (
        echo DB_TYPE=%DB_TYPE%
        echo DB_NAME=%DB_NAME%
        echo DB_USER=%DB_USER%
        echo DB_PASSWORD=%DB_PASSWORD%
        echo DB_HOST=%DB_HOST%
        echo DB_PORT=%DB_PORT%
        echo OPENAI_API_KEY=%OPENAI_API_KEY%
        echo BASE_APP_URL=%BASE_APP_URL% >> .env
    ) > .env
    
    echo .env file created successfully.
) else (
    echo .env file found. Skipping configuration.
)

:: Waiting for database configuration
echo Configuring database...
choice /t 3 /d y /n >nul

:: Check MySQL database connection if .env exists
if exist .env (
    for /f "tokens=1,2 delims==" %%A in (.env) do set %%A=%%B
    if "%DB_TYPE%"=="mysql" (
        where mysql >nul 2>nul
        if %ERRORLEVEL% NEQ 0 (
            echo MySQL command not found. Please ensure MySQL is installed and in your PATH.
            exit /b 1
        )
        
        echo Checking database connection...
        mysql -u%DB_USER% -p%DB_PASSWORD% -h %DB_HOST% -e "USE %DB_NAME%;" 2>nul
        if %ERRORLEVEL% NEQ 0 (
            echo Database connection failed. Please check your credentials.
            exit /b 1
        ) else (
            echo Database connected successfully.
        )
    )
) else (
    echo Skipping database setup since .env is empty or missing.
)

:: Run Django migrations
echo Running migrations...
python manage.py makemigrations RAG_CHATBOT_BACKEND_APIS
python manage.py migrate

echo Setup complete!
ENDLOCAL
>>>>>>> 4f2ff96ff6e59c1ed95fb7570ec6a2164f6e9406
