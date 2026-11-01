# BÁO CÁO BÀI THỰC HÀNH 3: TRIỂN KHAI CI/CD & BUILD DOCKER IMAGE CHO BÀI TOÁN AI

- **Học phần:** Chuyên đề Trí tuệ Nhân tạo
- **Họ và tên sinh viên:** Nguyễn Hồng Phúc
- **Mã số sinh viên (MSSV):** 2351260680
- **Lớp:** 65TTNT
- **Đề tài bài toán AI:** Dự báo ô nhiễm không khí PM2.5 tại Hà Nội (Multivariate Time-series Forecasting)
- **Mô hình cốt lõi:** SOFTS (*Series-Core Fusion*) tích hợp backbone **DINOv3 (ViT-S/16)**
- **GitHub Repository CI/CD:** [https://github.com/nguyenphuc210/hanoi-pm25-ai-cicd](https://github.com/nguyenphuc210/hanoi-pm25-ai-cicd)
- **GitHub Actions Run (Thành công 100%):** [https://github.com/nguyenphuc210/hanoi-pm25-ai-cicd/actions/runs/41311841207](https://github.com/nguyenphuc210/hanoi-pm25-ai-cicd/actions/runs/41311841207)
- **Docker Hub Repository (Public Image):** [https://hub.docker.com/r/phucnguyen210/hanoi-pm25-softs-dinov3](https://hub.docker.com/r/phucnguyen210/hanoi-pm25-softs-dinov3)

---

## BẢNG TỔNG HỢP KẾT QUẢ ĐẠT ĐƯỢC

| STT | Hạng mục yêu cầu | Trạng thái | Minh chứng / Đường dẫn nghiệm thu |
|:---:|---|:---:|---|
| **1** | **Triển khai CI/CD cho bài toán AI** | **Hoàn thành 100%** | Pipeline GitHub Actions 2 giai đoạn: `CI (Test 7/7 bài)` $\rightarrow$ `CD (Docker Build & Push)`. Toàn bộ steps đều xanh lá.<br>👉 [*GitHub Actions Run #6*](https://github.com/nguyenphuc210/hanoi-pm25-ai-cicd/actions/runs/41311841207) |
| **2** | **Build Docker Image & Public lên Docker Hub** | **Hoàn thành 100%** | Docker Image `phucnguyen210/hanoi-pm25-softs-dinov3:latest` (Dung lượng: 448.14 MB) đã publish công khai trên Docker Hub.<br>👉 [*Docker Hub Public Repo*](https://hub.docker.com/r/phucnguyen210/hanoi-pm25-softs-dinov3) |
| **3** | **Báo cáo Step-by-Step dạng PDF** | **Hoàn thành 100%** | Xuất tài liệu chuẩn báo cáo chi tiết từng bước tái hiện và giải thích kiến trúc. |

---

## PHẦN 1. THIẾT KẾ KIẾN TRÚC CI/CD CHO BÀI TOÁN AI

### 1.1. Luồng vận hành tổng thể (Pipeline Architecture)

Hệ thống MLOps CI/CD được xây dựng hoàn toàn tự động dựa trên GitHub Actions và Docker Hub:

```
[Developer: git push main]
            │
            ▼
┌─────────────────────────────────────────────────────────────┐
│ GIAI ĐOẠN 1: CONTINUOUS INTEGRATION (CI)                    │
│ 1. Checkout mã nguồn ứng dụng & checkpoint mô hình          │
│ 2. Khởi tạo môi trường Python 3.10 & Pip Cache              │
│ 3. Cài đặt PyTorch CPU & dependencies phục vụ inference    │
│ 4. Chạy Pytest Suite (7 bài kiểm thử đơn vị & tích hợp)   │
│    - Kiểm tra tính toàn vẹn file softs_dinov3_hanoi.pt      │
│    - Kiểm tra khởi tạo mạng SOFTS tích hợp DINOv3           │
│    - Kiểm tra nạp trọng số state_dict                       │
│    - Kiểm tra suy luận tensor (1, 96, 7) -> (1, 24, 7)      │
│    - Kiểm tra endpoint /health & /api/predict               │
└──────────────────────────────┬──────────────────────────────┘
                               │ (100% Passed)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ GIAI ĐOẠN 2: CONTINUOUS DEPLOYMENT (CD)                     │
│ 1. Khởi tạo Docker Buildx đa nền tảng                      │
│ 2. Xác thực thông tin đăng nhập Docker Hub qua Secrets      │
│ 3. Trích xuất metadata (tag latest, git sha, branch name)   │
│ 4. Build Docker Image tối ưu (Python 3.10-slim)             │
│ 5. Đẩy image trực tiếp lên Docker Hub công khai (Public)    │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
     [Docker Hub: phucnguyen210/hanoi-pm25-softs-dinov3:latest]
                               │
                               ▼
            [Edge Servers / Users: docker run]
```

### 1.2. Chi tiết cấu hình Workflow (`.github/workflows/ci_cd.yml`)

Workflow được kích hoạt tự động mỗi khi có sự kiện `push` hoặc `pull_request` vào nhánh `main`, đồng thời hỗ trợ `workflow_dispatch` để kích hoạt thủ công:

```yaml
name: AI MLOps CI/CD Pipeline

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]
  workflow_dispatch:

env:
  DOCKER_IMAGE_NAME: phucnguyen210/hanoi-pm25-softs-dinov3

jobs:
  ci_test_and_validation:
    name: CI - Model & API Validation
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python 3.10
        uses: actions/setup-python@v5
        with:
          python-version: "3.10"
          cache: "pip"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run Unit & Integration Tests (Pytest)
        run: |
          python -m pytest tests/ -v --tb=short

  cd_docker_hub_publish:
    name: CD - Build & Push Docker Image
    needs: ci_test_and_validation
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Check Docker Credentials Configuration
        run: |
          echo "Target Docker Hub User: ${{ secrets.DOCKERHUB_USERNAME || 'phucnguyen210' }}"
          if [ -z "${{ secrets.DOCKERHUB_TOKEN }}" ]; then
            echo "::error::Docker token is empty!"
            exit 1
          fi

      - name: Log in to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME || 'phucnguyen210' }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Extract metadata (tags, labels)
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.DOCKER_IMAGE_NAME }}
          tags: |
            type=raw,value=latest
            type=sha,format=short
            type=ref,event=branch

      - name: Build and Push Docker Image
        uses: docker/build-push-action@v5
        with:
          context: .
          file: ./Dockerfile
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

---

## PHẦN 2. THIẾT KẾ BỘ KIỂM THỬ TỰ ĐỘNG (UNIT & INTEGRATION TESTS)

Bộ kiểm thử được viết bằng thư viện `pytest`, chia thành 2 module chuyên biệt:

### 2.1. Kiểm thử mô hình AI (`tests/test_model.py`)
1. **`test_model_file_exists`**: Kiểm tra sự tồn tại của file checkpoint `softs_dinov3_hanoi.pt` và dung lượng phải lớn hơn 1.0 MB (tránh trường hợp file bị hỏng hoặc dung lượng 0 byte).
2. **`test_model_initialization`**: Kiểm tra khởi tạo lớp `Model` với cấu hình `ModelConfigs`, đảm bảo mô hình có đầy đủ thuộc tính `encoder` của DINOv3.
3. **`test_checkpoint_loading`**: Kiểm tra tính tương thích khi nạp `state_dict` vào mô hình, đảm bảo không có missing keys trọng số.
4. **`test_model_forward_shape_and_values`**: Kiểm thử suy luận tensor thực tế:
   - Đầu vào giả lập chuỗi 96 giờ x 7 đặc trưng: `torch.randn(1, 96, 7)`.
   - Đầu ra dự báo 24 giờ tiếp theo: xác nhận kích thước chuẩn `(1, 24, 7)`.
   - Xác thực giá trị không được chứa `NaN` hoặc `Inf`.

### 2.2. Kiểm thử API phục vụ (`tests/test_api.py`)
1. **`test_health_check_endpoint`**: Kiểm tra endpoint `GET /health` trả về mã HTTP 200 và chuỗi thông tin `healthy`.
2. **`test_dashboard_homepage`**: Kiểm tra endpoint `GET /` trả về giao diện Dashboard giám sát thời gian thực.
3. **`test_predict_endpoint_with_csv_upload`**: Kiểm tra endpoint `POST /api/predict` suy luận offline từ file CSV 96 giờ, kiểm tra phản hồi JSON chứa đủ mốc 24 giờ trong `forecast_data` và các thông số đánh giá động `mae`, `rmse`.

---

## PHẦN 3. ĐÓNG GÓI DOCKER CONTAINER CHO MÔ HÌNH AI

### 3.1. File cấu hình `Dockerfile`
Sử dụng base image `python:3.10-slim` để tối ưu hóa kích thước image nhưng vẫn đảm bảo tính ổn định và tương thích cao:

```dockerfile
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=7860

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:7860/health || exit 1

CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT:-7860}"]
```

### 3.2. File `.dockerignore`
Loại bỏ các tệp rác, cache kiểm thử và tệp cấu hình không cần thiết khi chạy serving nhằm giảm tối đa dung lượng container:
- `.git`, `.gitignore`, `.github`
- `__pycache__`, `*.pyc`, `.pytest_cache`
- `tests/`, `yeucauTH3.txt`, `*.md`, `*.docx`, `*.pdf`, `*token*.txt`

---

## PHẦN 4. KẾT QUẢ THỰC NGHIỆM & HƯỚNG DẪN TÁI HIỆN (STEP-BY-STEP)

### 4.1. Kết quả GitHub Actions Pipeline Run #6
- **Giai đoạn CI (`CI - Model & API Validation`)**:
  - Thời gian thực thi: **45 giây**.
  - Kết quả: **`7 passed, 1 warning in 9.75s`** (100% Passed).
- **Giai đoạn CD (`CD - Build & Push Docker Image`)**:
  - Thời gian thực thi: **1 phút 12 giây**.
  - Trạng thái đăng nhập Docker Hub: `Log in to Docker Hub => completed success`.
  - Kết quả xuất bản: Image được build và push thành công lên Docker Hub với 3 tags:
    - `phucnguyen210/hanoi-pm25-softs-dinov3:latest` (Dung lượng nén: **448.14 MB**)
    - `phucnguyen210/hanoi-pm25-softs-dinov3:sha-8ee8988`
    - `phucnguyen210/hanoi-pm25-softs-dinov3:main`

### 4.2. Hướng dẫn Kéo và Chạy Container từ Docker Hub

Bất kỳ máy trạm hoặc máy chủ nào có cài đặt Docker đều có thể vận hành hệ thống dự báo AI chỉ với 2 câu lệnh:

#### Bước 1: Kéo Image từ Docker Hub
```bash
docker pull phucnguyen210/hanoi-pm25-softs-dinov3:latest
```

#### Bước 2: Khởi chạy Container
```bash
docker run -d --name hanoi_pm25_service -p 7860:7860 phucnguyen210/hanoi-pm25-softs-dinov3:latest
```

#### Bước 3: Nghiệm thu dịch vụ
- Truy cập Dashboard giao diện người dùng: [http://localhost:7860](http://localhost:7860)
- Kiểm tra Endpoint giám sát trạng thái hệ thống:
  ```bash
  curl http://localhost:7860/health
  ```
  *Kết quả trả về:*
  ```json
  {
    "status": "healthy",
    "service": "Hanoi PM2.5 Air Quality Forecasting",
    "model": "SOFTS with DINOv3 ViT Backbone",
    "backend": "FastAPI + PyTorch CPU",
    "stations_count": 10,
    "platform": "OnRender / Cloud"
  }
  ```

---

## PHẦN 5. KẾT LUẬN

Bài thực hành 3 đã hoàn thành xuất sắc toàn bộ các mục tiêu đặt ra:
1. Đã thiết kế và chuẩn hóa quy trình **CI/CD hoàn chỉnh cho mô hình AI** thông qua GitHub Actions, tự động kiểm thử toàn diện từ checkpoint trọng số đến suy luận tensor và API serving.
2. Đã đóng gói thành công **Docker Image chuẩn MLOps**, tối ưu dung lượng (448.14 MB) với `python:3.10-slim` và PyTorch CPU, tự động build & push lên **Docker Hub công khai**.
3. Hệ thống có khả năng chuyển giao và triển khai tức thì trên bất kỳ môi trường đám mây hoặc máy chủ biên (Edge Server) nào chỉ qua lệnh `docker run`.
