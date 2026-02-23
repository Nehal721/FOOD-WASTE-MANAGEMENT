FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

# Install CPU-only PyTorch FIRST
RUN pip install --no-cache-dir torch==2.1.2 --index-url https://download.pytorch.org/whl/cpu

# Install rest of dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]