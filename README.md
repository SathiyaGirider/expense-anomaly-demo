# Expense Anomaly Demo

This is a demonstration project for detecting expense anomalies. It consists of a FastAPI backend and a clean HTML/CSS frontend.

## Project Structure

- `backend/`
  - `main.py` - Minimal FastAPI hello-world API.
  - `requirements.txt` - Project dependencies (`fastapi`, `uvicorn`).
- `frontend/`
  - `index.html` - Simple and beautiful frontend homepage.

## Running the Project

### Backend
1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend
Open `frontend/index.html` directly in your browser or serve it using any local static file server.
