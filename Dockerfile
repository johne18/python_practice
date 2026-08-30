FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY project_two_dir ./project_two_dir

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "project_two_dir.poke_fast_api:app", "--host", "0.0.0.0", "--port", "8000"]