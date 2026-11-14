# Project Startup Rule

When the user says "run the project", "start the project", or similar commands:

1. Immediately launch the Streamlit frontend as a background daemon process:
   ```powershell
   .\.venv\Scripts\streamlit.exe run app.py --server.headless true --server.port 8501
   ```
2. Immediately launch the FastAPI REST API server as a background daemon process:
   ```powershell
   .\.venv\Scripts\python.exe -m uvicorn api:app --host 127.0.0.1 --port 8000
   ```
3. Verify both services are active (HTTP 200 on `http://localhost:8501` and `http://127.0.0.1:8000/api/health`).
4. Present the user with direct clickable links:
   - Streamlit Web App: http://localhost:8501
   - FastAPI Docs: http://127.0.0.1:8000/docs
