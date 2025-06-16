FROM python:latest

WORKDIR /code

COPY ./requirements.txt .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN mkdir datasets

COPY ./srcs/. /code

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]