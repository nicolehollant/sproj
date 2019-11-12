FROM python:3.7-alpine3.7
RUN mkdir -p app
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python3", "-m", "model"]