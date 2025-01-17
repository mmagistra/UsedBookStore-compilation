FROM python:3.12

RUN apt-get update

COPY ./requirements.txt ./requirements.txt

RUN pip3 install --upgrade pip && pip3 install -r requirements.txt
RUN pip3 install gunicorn

COPY ./ ./

#CMD ["python manage.py migrate"]
#CMD ["gunicorn", "UsedBookStore.wsgi", "-b 0.0.0.0:8000"]