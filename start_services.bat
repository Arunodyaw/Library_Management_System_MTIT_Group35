@echo off
echo Starting Library Management Microservices...

:: Start Book Service
start "Book Service (8001)" cmd /k "call venv\Scripts\activate && cd Book-service && uvicorn main:app --port 8001 --reload"

:: Start Borrowbook Service
start "Borrowbook Service (8002)" cmd /k "call venv\Scripts\activate && cd Borrowbook-service && uvicorn main:app --port 8002 --reload"

:: Start Member Service (Port 8003)
start "Member Service (8003)" cmd /k "call venv\Scripts\activate && cd Member-service && uvicorn main:app --port 8003 --reload"

:: Start Payment Service (Port 8004)
start "Payment Service (8004)" cmd /k "call venv\Scripts\activate && cd Fine-service && uvicorn main:app --port 8004 --reload"

:: Start Reservation Service (Port 8005)
start "Reservation Service (8005)" cmd /k "call venv\Scripts\activate && cd Reservation-service && uvicorn main:app --port 8005 --reload"

:: Start Notification Service (Port 8006)
start "Notification Service (8006)" cmd /k "call venv\Scripts\activate && cd Notification-service && uvicorn main:app --port 8006 --reload"

:: Start API Gateway
start "API Gateway (8000)" cmd /k "call venv\Scripts\activate && cd Api-Gateway && uvicorn main:app --port 8000 --reload"

echo All available services have been launched in new windows!