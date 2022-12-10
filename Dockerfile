FROM python:3.10-bullseye

WORKDIR /app

RUN pip3 install poetry
RUN poetry config virtualenvs.create false

COPY ./pyproject.toml ./poetry.lock /app/
RUN poetry install --no-root

COPY . /app

EXPOSE 8050/tcp

ENV API_SERVER_URL=https://mndotbidprices.com/api/v1

CMD ["gunicorn", "--workers=2", "--bind=0.0.0.0:8050", "--forwarded-allow-ips='10.170.3.217,10.170.3.220'", "main:server"]