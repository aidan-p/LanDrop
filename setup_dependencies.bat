@echo off
SETLOCAL

:: Check if python.exe and pythonw.exe are available
where python >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Installing Python...
    :: Download Python installer
    set pythonInstaller=https://www.python.org/ftp/python/3.9.7/python-3.9.7-amd64.exe
    set installerPath=%TEMP%\python-installer.exe
    powershell -Command "Invoke-WebRequest -Uri %pythonInstaller% -OutFile %installerPath%"
    
    :: Install Python with the necessary options
    start /wait %installerPath% /quiet InstallAllUsers=1 PrependPath=1
    
    :: Clean up the installer
    del /f /q %installerPath%
    echo Python 3.9 installed successfully.
) ELSE (
    echo Python is already installed.
)

:: Check if pythonw.exe is installed and point it to the right version
where pythonw >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo pythonw.exe not found. Please ensure that it is installed with Python.
    exit /b
)

:: Update the PATH to ensure the correct Python version is used
set pythonPath=C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python39
echo Checking and updating PATH...
set pathEnv=%PATH%
echo %pathEnv% | findstr /C:"%pythonPath%" >nul
IF %ERRORLEVEL% NEQ 0 (
    setx PATH "%pathEnv%;%pythonPath%"
    echo Python 3.9 added to PATH.
) ELSE (
    echo Python 3.9 is already in the PATH.
)

:: Install required Python packages
echo Installing required Python packages...
python -m pip show flask >nul 2>nul || python -m pip install flask
python -m pip show flask-socketio >nul 2>nul || python -m pip install flask-socketio
python -m pip show infi.systray >nul 2>nul || python -m pip install infi.systray
python -m pip show requests >nul 2>nul || python -m pip install requests
python -m pip show tk >nul 2>nul || python -m pip install tk

:: Clean up temporary files
echo Cleaning up temporary files...
for /f "delims=" %%i in ('dir /b /a-d "%TEMP%"') do (
    if %%~ti lss %DATE% (
        del /f /q "%TEMP%\%%i"
    )
)

echo Installation and setup completed.

ENDLOCAL
pause
