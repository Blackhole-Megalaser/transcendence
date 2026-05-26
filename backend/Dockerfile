FROM python:3.14-slim
WORKDIR /app

RUN pip install --upgrade pip
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000
ENTRYPOINT ["/app/entrypoint.sh"]

CMD [ "python", "-m", "daphne", "transcendence.asgi:application" ]
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# CMD ["python", "manage.py", "check", "--deploy"]