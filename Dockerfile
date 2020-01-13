FROM python:3.6-alpine

WORKDIR /src/app/

COPY ./requirements.txt .

RUN ["pip", "install", "-r", "./requirements.txt"]

COPY . .

RUN addgroup -S projects && adduser -S -H projects -G projects
RUN chown -R projects:projects /src/app
USER projects

RUN ["python3", "-m", "venv", "venv"]
RUN ["source", "venv/bin/activate"]

WORKDIR /src/app/device_data
ENTRYPOINT [ "python3", "app.py" ]

# ENTRYPOINT [ "flask", "run" ]