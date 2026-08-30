FROM python:3.12-slim

WORKDIR /app

COPY ../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./pokemon_worker

CMD ["python", "pokemon_worker/app.py"]