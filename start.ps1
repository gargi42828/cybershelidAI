# CyberShield AI - One Click Start

$project = "C:\Users\gargi\OneDrive\Desktop\cybershelidAI"

# Start Backend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$project'; .\venv\Scripts\Activate.ps1; python -m uvicorn backend.app.main:app --reload"

# Wait for backend
Start-Sleep -Seconds 3

# Start Frontend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$project\frontend'; npm run dev"

# Wait for frontend
Start-Sleep -Seconds 5

# Open CyberShield AI
Start-Process "http://localhost:5173"