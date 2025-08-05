FROM python:3.10.18-alpine

WORKDIR /app

COPY ./entrypoint.sh .

RUN chmod +x ./entrypoint.sh && ./entrypoint.sh

COPY ./requirements.txt .

RUN pip install -r ./requirements.txt

COPY . .

EXPOSE 5000

CMD flask --app app.py run
