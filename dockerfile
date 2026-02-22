FROM python:3.11-slim

WORKDIR /Nazarenko_EO

COPY trans_prog.py .

RUN pip install googletrans==3.1.0a0

CMD ["python", "trans_prog.py"]