FROM python:3.10.8
WORKDIR /app
COPY . /app
RUN chmod +x start.sh
RUN pip install -r requirements.txt
CMD ["./start.sh"]
