@echo off
echo Fixing missing sqlite3.h for pysqlite3 installation...

:: Step 1: Update pip, setuptools, and wheel
echo Updating pip, setuptools, and wheel...
python -m pip install --upgrade pip setuptools wheel

:: Step 2: Install SQLite3
echo Installing SQLite3...
winget install -e --id SQLite.SQLite

:: Step 3: Install Microsoft Build Tools (for compiling dependencies)
echo Installing Microsoft C++ Build Tools...
winget install -e --id Microsoft.VisualStudio.2022.BuildTools

:: Step 4: Set environment variables
echo Setting environment variables...
setx SQLITE3_INCLUDE_DIR "C:\Program Files\SQLite\include"
setx SQLITE3_LIB_DIR "C:\Program Files\SQLite\lib"

:: Step 5: Install pysqlite3
echo Installing pysqlite3...
pip install pysqlite3-binary

:: Step 6: Verify installation
echo Verifying SQLite installation...
python -c "import sqlite3; print('SQLite Version:', sqlite3.sqlite_version)"

echo All done! Restart your terminal and try running your Python script again.
pause
