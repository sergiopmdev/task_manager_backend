FROM python:3.11.4-bullseye

WORKDIR /app

ENV PIP_ROOT_USER_ACTION=ignore

COPY ./requirements.txt /code/requirements.txt

RUN pip install --upgrade pip

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /app

WORKDIR /app/src

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
