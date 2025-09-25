FROM python:3.13.7-slim

WORKDIR /app

COPY ./entrypoint.sh .

RUN chmod +x ./entrypoint.sh && ./entrypoint.sh

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r ./requirements.txt

COPY . .

CMD ["fastapi", "run", "app/main.py", "--port", "80"]
