FROM python:3.8-slim

COPY ./docker/requirements.txt .

RUN python -m pip install --upgrade pip 
RUN pip install -r requirements.txt

WORKDIR /app/src

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "6300"]
