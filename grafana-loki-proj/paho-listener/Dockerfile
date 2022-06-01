FROM python:3.8-alpine
ADD . /code
WORKDIR /code
RUN pip install -r requirement.txt
CMD ["python", "app.py"]