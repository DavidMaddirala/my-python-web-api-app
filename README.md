# My Python Web API App

FastAPI app with a few endpoints. Docs at `/docs` when running.

## Run locally
    python -m venv .venv
    source .venv/bin/activate      # Windows: .venv\Scripts\activate
    pip install -r requirements.txt
    uvicorn main:app --reload

## Run with Docker
    docker build -t my-python-web-api-app .
    docker run -p 8000:8000 my-python-web-api-app
