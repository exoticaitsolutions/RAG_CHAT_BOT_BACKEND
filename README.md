# Project Name
## RAG Backend Django 
### Python Installation Process
Before proceeding, ensure Python is installed on your system. If not, you can download and install Python from [python.org](https://www.python.org/downloads/).
### Clone the Project
```bash
git clone https://github.com/exoticaitsolutions/RAG_Backend.git
```

## Navigate to the Project Directory

```bash
  cd RAG_Backend
```

This script will create a virtual environment, activate it, and install all required packages specified in requirements.txt. and updating the pip 

# **_Windows:_**
```
setup.bat
```
**Unix/MacOS:**
```
bash setup.sh
```
Then run the migrate command to create the tables in the database

Windows:

```bash
python manage.py migrate

```

Unix/MacOS/LInux:

```bash
python3 manage.py migrate
```

Start the server

**Windows:**

```bash
python manage.py runserver

```

**Unix/MacOS/LLinux:**

```bash
python3 manage.py runserver
```
