@REM Change directory to the project root
cd %~dp0
cd ../..

@REM Activate the venv
call .\.venv\Scripts\activate

if ERRORLEVEL 1 EXIT /B 1

@REM Run Conreq
call python manage.py run_conreq