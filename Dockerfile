FROM python:3.8
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app
COPY ./logs /code/logs
COPY dev.env runserver.py /code/
CMD ["python", "runserver.py"]
