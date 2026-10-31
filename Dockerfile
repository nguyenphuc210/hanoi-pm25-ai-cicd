# Multi-stage / Slim Python runtime for AI Model Serving
FROM python:3.10-slim

# Thiết lập biến môi trường chuẩn cho container Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=7860

WORKDIR /app

# Cài đặt curl phục vụ container healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Cài đặt dependencies trước để tối ưu Docker layer cache
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy source code, layers, models và checkpoint AI
COPY . .

# Expose port mặc định (7860 phù hợp cho cả HuggingFace Spaces, Render, Docker Hub)
EXPOSE 7860

# Health check endpoint định kỳ
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:7860/health || exit 1

# Khởi chạy FastAPI backend
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT:-7860}"]
