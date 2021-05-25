FROM python:3

# copy directory
WORKDIR /rest_api
COPY . .

# install python packages
RUN pip install -r requirements.txt

# initialize django
RUN python manage.py makemigrations benchmarks
RUN python manage.py makemigrations machines
RUN python manage.py makemigrations postgres
RUN python manage.py makemigrations runs
RUN python manage.py makemigrations systems
RUN python manage.py makemigrations users
RUN python manage.py migrate
RUN python manage.py loaddata initial_data.json

ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]
