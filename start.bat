@echo off
echo Starting Twitch AutoPoster...
echo.
echo Make sure you have:
echo 1. Created .env file with your configuration
echo 2. Installed requirements: pip install -r requirements.txt
echo 3. Activated virtual environment if using one
echo.
echo Press any key to start...
pause >nul

python main.py
pause
