FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install flask spyne mysql-connector-python zeep
CMD ["python", "registro.py"]
