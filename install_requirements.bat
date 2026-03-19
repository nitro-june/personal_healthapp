@echo off
setlocal

echo === Mental Health Tracker dependency installer ===
echo.

where py >nul 2>nul
if %errorlevel%==0 (
  set PY=py -m
) else (
  where python >nul 2>nul
  if %errorlevel%==0 (
    set PY=python -m
  ) else (
    echo [ERROR] Python was not found in PATH.
    echo Install Python and try again.
    pause
    exit /b 1
  )
)

echo Upgrading pip...
%PY% pip install --upgrade pip
if errorlevel 1 goto :fail

echo Installing required libraries...
%PY% pip install Jinja2 numpy scipy matplotlib PyQt5 pdfkit
if errorlevel 1 goto :fail

echo.
echo [IMPORTANT] pdfkit also requires wkhtmltopdf (separate install):
echo https://wkhtmltopdf.org/downloads.html
echo After installing, ensure wkhtmltopdf is in PATH.
echo.
echo Done.
pause
exit /b 0

:fail
echo.
echo [ERROR] Installation failed.
pause
exit /b 1
