FROM python:3.11-slim

WORKDIR /workspace

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY stream_generator.py .

CMD ["python", "stream_generator.py"]