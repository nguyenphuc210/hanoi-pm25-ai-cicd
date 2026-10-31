"""
Integration & Functional Tests for FastAPI AI Serving Backend
Author: Nguyen Hong Phuc (2351260680 - 65TTNT)
"""

import io
import pytest
import pandas as pd
import numpy as np
from fastapi.testclient import TestClient

from app import app, feature_cols

client = TestClient(app)


def test_health_check_endpoint():
    """Kiểm tra endpoint /health hoạt động chuẩn xác"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "SOFTS" in data["model"]
    assert "DINOv3" in data["model"]


def test_dashboard_homepage():
    """Kiểm tra endpoint / trả về giao diện HTML Dashboard"""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Hà Nội" in response.text or "PM2.5" in response.text


def test_predict_endpoint_with_csv_upload():
    """
    Kiểm tra endpoint suy luận /api/predict khi tải lên file dữ liệu CSV:
    - Tự tạo dữ liệu 96 dòng x 7 cột
    - Đảm bảo suy luận offline thành công không phụ thuộc internet
    - Kiểm tra phản hồi trả về đúng cấu trúc 24 giờ dự báo
    """
    # Tạo dataframe mẫu 96 giờ
    synthetic_data = np.random.uniform(15.0, 75.0, size=(96, len(feature_cols)))
    df = pd.DataFrame(synthetic_data, columns=feature_cols)
    
    csv_bytes = io.BytesIO()
    df.to_csv(csv_bytes, index=False)
    csv_bytes.seek(0)

    files = {"file": ("test_input.csv", csv_bytes, "text/csv")}
    data = {"station": "Trạm Đống Đa (Láng Hạ)"}

    response = client.post("/api/predict", data=data, files=files)
    assert response.status_code == 200
    result = response.json()

    assert "time_series" in result, "Thiếu trường 'time_series' trong kết quả JSON"
    assert "forecast_data" in result["time_series"], "Thiếu 'forecast_data' trong 'time_series'"
    assert len(result["time_series"]["forecast_data"]) == 24, f"Dự báo không đúng 24 mốc giờ: {len(result['time_series']['forecast_data'])}"
    assert "metrics" in result, "Thiếu trường đánh giá 'metrics'"
    assert "mae" in result["metrics"]
    assert "rmse" in result["metrics"]
    assert float(result["metrics"]["mae"]) > 0
