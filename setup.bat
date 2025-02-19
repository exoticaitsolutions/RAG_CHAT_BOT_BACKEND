@echo off
echo Starting setup script...

:: Check if virtual environment exists
if exist venv (
    echo Virtual environment found. Activating...
    call .venv\Scripts\activate
) else (
    echo Virtual environment not found. Creating...
    python -m venv venv
    echo Activating virtual environment...
    call .venv\Scripts\activate
)

if %errorlevel% neq 0 (
    echo Failed to activate virtual environment.
    exit /b 1
)

echo Virtual environment activated.

:: Update pip, setuptools, and wheel
echo Updating pip...
pip install --upgrade pip setuptools wheel

:: Install requirements
echo Installing required packages...
pip install -r requirements.txt

:: Create .env file
echo Configuring environment variables...
set /p DB_TYPE="Choose Database Type (mysql/sqlite/postgres): "
set /p DB_NAME="Enter Database Name: "
set /p DB_USER="Enter Database User (default: root): "
if "%DB_USER%"=="" set DB_USER=root
set /p DB_PASSWORD="Enter Database Password: "
set /p DB_HOST="Enter Database Host (default: localhost): "
if "%DB_HOST%"=="" set DB_HOST=localhost
set DB_PORT=3306
set /p OPENAI_API_KEY="Enter OpenAI API Key: "

(
echo DB_TYPE=%DB_TYPE%
echo DB_NAME=%DB_NAME%
echo DB_USER=%DB_USER%
echo DB_PASSWORD=%DB_PASSWORD%
echo DB_HOST=%DB_HOST%
echo DB_PORT=%DB_PORT%
echo OPENAI_API_KEY=%OPENAI_API_KEY%
) > .env

echo .env file created successfully.

:: Wait for 3 seconds
timeout /t 3 /nobreak

:: Check MySQL connection
if "%DB_TYPE%"=="mysql" (
   
