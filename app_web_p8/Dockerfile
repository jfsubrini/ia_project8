FROM python:3.10.8
# Setting work directory.
WORKDIR /app
COPY . /app
RUN chmod +x start.sh
# Installing dependencies.
RUN pip install -r requirements.txt
# Collecting static files (media).
RUN python manage.py collectstatic --noinput
# Running gunicorn.
CMD ["./start.sh"]
