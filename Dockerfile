FROM python:3.10.2-slim-bullseye
WORKDIR .
RUN pip install Django
RUN pip install djangorestframework
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
COPY . .
~            
