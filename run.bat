@echo off
echo Starting Legal Research Chatbot...
echo.

echo Activating virtual environment...
call venv\Scripts\activate
echo.

echo Starting backend server...
echo The server will be available at http://127.0.0.1:5000
echo Please open chatpot.html in your browser to use the chatbot
echo.
python chatbot.py
echo.

pause