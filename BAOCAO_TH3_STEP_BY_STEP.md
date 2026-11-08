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

---

## PHẦN 2. CÁC BƯỚC THỰC HIỆN STEP-BY-STEP TRIỂN KHAI CI/CD & BUILD DOCKER IMAGE

Dưới đây là đặc tả chi tiết toàn bộ tiến trình kỹ thuật gồm 8 bước tuần tự mà sinh viên đã thực hiện từ khâu chuẩn bị mã nguồn đến khi xuất bản thành công hệ thống lên Docker Hub:

### Bước 1: Chuẩn bị mã nguồn và checkpoint mô hình AI
- Kế thừa và chuẩn hóa cấu trúc thư mục từ mô hình AI đã hoàn thiện:
  - `models/SOFTS.py`: Định nghĩa kiến trúc mô hình tổng thể.
  - `layers/DINOv3Encoder.py`: Backbone thị giác ViT-S/16 (12 block Attention, 2D Axial RoPE, 4 Register Tokens).
  - `app.py`: Backend serving viết bằng FastAPI, phục vụ suy luận thời gian thực cho 10 trạm quan trắc tại Hà Nội và kiểm tra sức khỏe `/health`.
  - `index.html`: Giao diện Dashboard trực quan hóa chuỗi thời gian 24 giờ và giải thích mô hình XAI (Explainable AI).
  - `softs_dinov3_hanoi.pt`: Tệp trọng số mô hình đã huấn luyện (dung lượng 3.84 MB, nạp được trực tiếp vào Git).

### Bước 2: Thiết kế và kiểm định bộ kiểm thử tự động (Unit & Integration Tests)
- Để đảm bảo mã nguồn và trọng số không bị lỗi trước khi đóng gói, sinh viên đã xây dựng bộ kiểm thử bằng thư viện `pytest`:
  - `tests/test_model.py`:
    1. `test_model_file_exists`: Xác thực tệp `softs_dinov3_hanoi.pt` tồn tại và dung lượng > 1 MB.
    2. `test_model_initialization`: Kiểm tra khởi tạo lớp `Model` với `ModelConfigs`.
    3. `test_checkpoint_loading`: Kiểm tra tính tương thích của `state_dict`, bảo đảm không thiếu trọng số.
    4. `test_model_forward_shape_and_values`: Truyền tensor giả lập `(1, 96, 7)` và xác nhận đầu ra chuẩn `(1, 24, 7)` không chứa giá trị `NaN` hay `Inf`.
  - `tests/test_api.py`:
    5. `test_health_check_endpoint`: Kiểm tra `GET /health` trả về HTTP 200 và trạng thái `healthy`.
    6. `test_dashboard_homepage`: Kiểm tra `GET /` tải thành công giao diện web.
    7. `test_predict_endpoint_with_csv_upload`: Kiểm tra `POST /api/predict` suy luận ngoại tuyến từ tệp CSV giả lập, trả về đủ 24 điểm mốc thời gian kèm MAE, RMSE.
- Thực thi kiểm thử cục bộ:
  ```bash
  python -m pytest tests/ -v
  # Kết quả: 7 passed in 9.75s (100% Passed)
  ```

### Bước 3: Đóng gói Docker Container và Tối ưu hóa kích thước Image
- Viết tệp `Dockerfile` tối ưu hóa:
  - Sử dụng base image `python:3.10-slim` thay cho bản full nhằm cắt giảm hơn 800 MB dung lượng hệ điều hành.
  - Trong `requirements.txt`, sử dụng cờ `--extra-index-url https://download.pytorch.org/whl/cpu` để chỉ tải bản PyTorch CPU (~180 MB), tránh tải gói CUDA GPU (> 2.5 GB) vốn không cần thiết cho máy chủ suy luận chuỗi thời gian nhẹ.
  - Tách riêng bước cài đặt dependencies trước khi sao chép toàn bộ mã nguồn nhằm tận dụng triệt để cơ chế **Docker Layer Caching**.
  - Thiết lập lệnh kiểm tra định kỳ `HEALTHCHECK --interval=30s --timeout=5s CMD curl -f http://localhost:7860/health || exit 1`.
- Viết tệp `.dockerignore`:
  - Loại bỏ các tệp rác và tệp bảo mật: `.git`, `__pycache__`, `.pytest_cache`, `tests/`, `*.docx`, `*.pdf`, `*token*.txt`.

### Bước 4: Tạo tài khoản và Cấu hình Secrets trên Docker Hub & GitHub
- Đăng nhập Docker Hub với tài khoản `phucnguyen210`.
- Tạo Personal Access Token (PAT) tại `Account Settings -> Personal Access Tokens` với tên `github-actions-cicd`, cấp quyền **Read & Write**.
- Trong repository GitHub [nguyenphuc210/hanoi-pm25-ai-cicd](https://github.com/nguyenphuc210/hanoi-pm25-ai-cicd), vào mục `Settings -> Secrets and variables -> Actions` và cấu hình 2 biến bí mật:
  1. `DOCKERHUB_USERNAME`: `phucnguyen210`
  2. `DOCKERHUB_TOKEN`: `dckr_pat_***********************************` (Personal Access Token đã cấp)

### Bước 5: Viết kịch bản tự động hóa GitHub Actions (`.github/workflows/ci_cd.yml`)
- Thiết lập tệp cấu hình pipeline hoàn chỉnh gồm 2 giai đoạn:
  - **CI (Model & API Validation):** Tự động kích hoạt khi có commit đẩy lên nhánh `main`. Kéo mã nguồn, cài đặt Python 3.10, cài dependencies và thực thi lệnh `pytest tests/ -v`.
  - **CD (Build & Push Docker Image):** Phụ thuộc vào CI (`needs: ci_test_and_validation`). Khi CI đạt 100%, tự động khởi tạo `docker/setup-buildx-action@v3`, đăng nhập Docker Hub qua secrets, build image và đẩy lên Docker Hub với các nhãn `latest`, `main`, và mã `sha` của commit.

### Bước 6: Khởi tạo Git và Đẩy mã nguồn lên GitHub
- Mở terminal tại thư mục dự án và thực thi chuỗi lệnh:
  ```bash
  git init -b main
  git add .
  git commit -m "feat(mlops): implement CI/CD pipeline and Docker deployment"
  git remote add origin https://github.com/nguyenphuc210/hanoi-pm25-ai-cicd.git
  git push -u origin main
  ```

### Bước 7: Giám sát và Tinh chỉnh Pipeline trên GitHub Actions
- Khi mã nguồn được đẩy lên, GitHub Actions lập tức khởi tạo tiến trình chạy tự động.
- Trong quá trình triển khai, sinh viên đã phát hiện và xử lý kịp thời lỗi sai lệch giữa tên đăng nhập GitHub (`nguyenphuc210`) và Docker ID (`phucnguyen210`) bằng cách chuẩn hóa cấu hình fallback trong `ci_cd.yml`.
- Tại lần chạy **Run #6** (Run ID: `41311841207`), toàn bộ quy trình đã đạt **100% SUCCESS**:
  - Giai đoạn CI: Hoàn thành trong **45 giây** (Passed 7/7 bài test).
  - Giai đoạn CD: Hoàn thành trong **1 phút 12 giây** (Build & Push thành công cả 3 thẻ tag).

### Bước 8: Kiểm thử và Nghiệm thu Docker Image từ xa
- Kiểm tra kho lưu trữ công khai trên Docker Hub: [https://hub.docker.com/r/phucnguyen210/hanoi-pm25-softs-dinov3](https://hub.docker.com/r/phucnguyen210/hanoi-pm25-softs-dinov3), xác nhận image có dung lượng nén tối ưu **448.14 MB**.
- Thực hiện nghiệm thu bằng cách kéo image từ xa và khởi chạy container cục bộ:
  ```bash
  docker pull phucnguyen210/hanoi-pm25-softs-dinov3:latest
  docker run -d --name hanoi_pm25_service -p 7860:7860 phucnguyen210/hanoi-pm25-softs-dinov3:latest
  ```
- Mở trình duyệt tại `http://localhost:7860`, xác nhận giao diện Web Dashboard hiển thị mượt mà, đường đồ thị dự báo 24 giờ liên tục theo giờ chẵn và kiểm tra endpoint `/health` phản hồi trạng thái `healthy`.

---

## PHẦN 3. CHI TIẾT MÃ NGUỒN CẤU HÌNH HỆ THỐNG

### 3.1. Mã nguồn GitHub Actions Workflow (`.github/workflows/ci_cd.yml`)
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

### 3.2. Mã nguồn `Dockerfile`
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

---

## PHẦN 4. HƯỚNG DẪN STEP-BY-STEP ĐỂ CLONE VÀ CHẠY DỰ ÁN (FOR USERS & REVIEWERS)

Để người khác (thầy cô chấm bài, người đánh giá hoặc người dùng mới) có thể chạy thử nghiệm dự án sau khi clone về máy, dự án hỗ trợ 3 phương thức vận hành linh hoạt:

### Cách 1: Chạy trực tiếp từ Docker Hub (Nhanh nhất — Không cần cài Python)
Không cần tải mã nguồn hay cài đặt môi trường lập trình, chỉ cần máy có Docker:
```bash
# 1. Kéo image chính thức từ Docker Hub
docker pull phucnguyen210/hanoi-pm25-softs-dinov3:latest

# 2. Khởi chạy container phục vụ dự báo trên cổng 7860
docker run -d --name hanoi_pm25_service -p 7860:7860 phucnguyen210/hanoi-pm25-softs-dinov3:latest

# 3. Mở trình duyệt web truy cập: http://localhost:7860
```

### Cách 2: Clone repository về máy và Tự đóng gói Docker Image
Dành cho người muốn kiểm chứng mã nguồn và tự đóng gói container tại chỗ:
```bash
# Bước 1: Clone kho lưu trữ từ GitHub
git clone https://github.com/nguyenphuc210/hanoi-pm25-ai-cicd.git
cd hanoi-pm25-ai-cicd

# Bước 2: Tự build Docker Image cục bộ
docker build -t hanoi-pm25-local:latest .

# Bước 3: Khởi chạy container từ image vừa build
docker run -d --name hanoi_pm25_local_service -p 7860:7860 hanoi-pm25-local:latest

# Bước 4: Mở trình duyệt web truy cập: http://localhost:7860
```

### Cách 3: Clone repository về máy và Chạy trực tiếp với Python (Virtual Environment)
Dành cho lập trình viên muốn xem mã nguồn, chạy kiểm thử hoặc chỉnh sửa thuật toán:
```bash
# Bước 1: Clone kho lưu trữ
git clone https://github.com/nguyenphuc210/hanoi-pm25-ai-cicd.git
cd hanoi-pm25-ai-cicd

# Bước 2: Tạo và kích hoạt môi trường ảo (Virtualenv)
python -m venv venv

# Kích hoạt trên Windows:
venv\Scripts\activate
# (Hoặc trên Linux/macOS: source venv/bin/activate)

# Bước 3: Cài đặt thư viện phụ thuộc (đã tối ưu PyTorch CPU ~180MB)
pip install --upgrade pip
pip install -r requirements.txt

# Bước 4: Chạy kiểm thử tự động để xác nhận chất lượng mô hình
python -m pytest tests/ -v
# Kết quả: 7 passed in ~10s

# Bước 5: Khởi chạy dịch vụ FastAPI Web Serving
python -m uvicorn app:app --host 0.0.0.0 --port 7860

# Bước 6: Mở trình duyệt web truy cập: http://localhost:7860
```

### Hướng dẫn kiểm tra và nghiệm thu kết quả
1. **Trực quan hóa Web Dashboard:** Mở `http://localhost:7860`, chọn trạm quan trắc (Đống Đa, Cầu Giấy, Hoàn Kiếm, v.v.) và bấm nút **`▶ RUN AI INFERENCE`** để xem đường đồ thị dự báo 24 giờ tiếp theo.
2. **Kiểm tra API giám sát sức khỏe:**
   ```bash
   curl http://localhost:7860/health
   ```
   *Kết quả JSON trả về:*
   ```json
   {
     "status": "healthy",
     "service": "Hanoi PM2.5 Air Quality Forecasting",
     "model": "SOFTS with DINOv3 ViT Backbone",
     "backend": "FastAPI + PyTorch CPU",
     "stations_count": 10
   }
   ```
3. **Tài liệu API tương tác tự động (Swagger UI):** Truy cập `http://localhost:7860/docs` để kiểm tra trực tiếp các schema và endpoint.

---

## PHẦN 5. KẾT LUẬN

Bài thực hành 3 đã hoàn thành xuất sắc toàn bộ các mục tiêu đặt ra:
1. Đã thiết kế và chuẩn hóa quy trình **CI/CD hoàn chỉnh cho mô hình AI** thông qua GitHub Actions, tự động kiểm thử toàn diện từ checkpoint trọng số đến suy luận tensor và API serving.
2. Đã đóng gói thành công **Docker Image chuẩn MLOps**, tối ưu dung lượng (448.14 MB) với `python:3.10-slim` và PyTorch CPU, tự động build & push lên **Docker Hub công khai**.
3. Hệ thống có khả năng chuyển giao và triển khai tức thì trên bất kỳ môi trường đám mây hoặc máy chủ biên (Edge Server) nào chỉ qua lệnh `docker run`.
