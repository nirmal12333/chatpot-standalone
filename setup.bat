@echo off
echo Setting up Legal Research Chatbot Environment...
echo.

echo Creating virtual environment...
python -m venv venv
echo.

echo Activating virtual environment...
call venv\Scripts\activate
echo.

echo Installing required packages...
pip install -r requirements.txt
echo.

echo Setup complete!
echo.
echo To run the chatbot:
echo 1. Activate the virtual environment: venv\Scripts\activate
echo 2. Run the backend: python chatbot.py
echo 3. Open chatpot.html in your browser
echo.
pause