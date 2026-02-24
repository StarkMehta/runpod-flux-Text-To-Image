# 1. Use a stable PyTorch base with CUDA 12.4
FROM runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04

WORKDIR /app

# 2. Prevent logs from being trapped in a buffer
ENV PYTHONUNBUFFERED=1

# 3. Install system dependencies for image handling
RUN apt-get update && apt-get install -y libgl1 libglib2.0-0 && rm -rf /var/lib/apt/lists/*

# 4. Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the 'Smart' handler
# Note: Ensure handler.py is in your 'src' folder
COPY src/handler.py .

# 6. Run the worker
CMD ["python", "-u", "handler.py"]