FROM ubi/python:3.12
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY . /code/app
CMD ["fastapi", "run", "app/app.py", "--port", "8000"]
