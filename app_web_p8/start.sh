#/bin/sh
gunicorn app_web_p8.wsgi:application --bind 0.0.0.0:$PORT
