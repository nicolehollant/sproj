FROM python:3.7-alpine3.7
RUN mkdir -p python-backend
COPY . /python-backend
WORKDIR /python-backend
RUN pip install -r requirements.txt
EXPOSE 3000
CMD ["python3", "app.py"]