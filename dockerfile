FROM python:3.10
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --root-user-action=ignore 
COPY . .
EXPOSE 8000

ENTRYPOINT [ "gunicorn", "core.wsgi", "-b", "0.0.0.0:8000","runserver"]