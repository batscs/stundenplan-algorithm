@echo off
:: Set the server URL and port
set SERVER_URL=http://127.0.0.1
set PORT=1111

:: Set the path to the input JSON file (relative to the batch file)
set INPUT_FILE=resources\input\FHW_DEV.json

:: Check if the input file exists
if not exist "%INPUT_FILE%" (
    echo Error: Input file "%INPUT_FILE%" not found.
    pause
    exit /b 1
)

:: Send a POST request to the /stundenplan route
echo Sending POST request to /stundenplan with data from %INPUT_FILE%...
curl -X POST -H "Content-Type: application/json" --data "@%INPUT_FILE%" %SERVER_URL%:%PORT%/stundenplan
echo.

pause