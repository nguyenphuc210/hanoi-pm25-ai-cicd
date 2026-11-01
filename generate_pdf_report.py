"""
Script tạo file PDF Báo cáo Bài thực hành 3 (CI/CD & Docker Hub)
Sinh viên: Nguyễn Hồng Phúc - MSSV: 2351260680 - Lớp: 65TTNT
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Đăng ký font tiếng Việt Unicode Times New Roman
pdfmetrics.registerFont(TTFont('Times', 'C:/Windows/Fonts/times.ttf'))
pdfmetrics.registerFont(TTFont('Times-Bold', 'C:/Windows/Fonts/timesbd.ttf'))
pdfmetrics.registerFont(TTFont('Times-Italic', 'C:/Windows/Fonts/timesi.ttf'))
pdfmetrics.registerFont(TTFont('Times-BoldItalic', 'C:/Windows/Fonts/timesbi.ttf'))
pdfmetrics.registerFontFamily('Times', normal='Times', bold='Times-Bold', italic='Times-Italic', boldItalic='Times-BoldItalic')

pdfmetrics.registerFont(TTFont('Courier-New', 'C:/Windows/Fonts/cour.ttf'))
pdfmetrics.registerFont(TTFont('Courier-New-Bold', 'C:/Windows/Fonts/courbd.ttf'))


class NumberedCanvas(canvas.Canvas):
    """Canvas hỗ trợ Header và Footer kèm tổng số trang động (Page X of Y)"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        self.saveState()
        self.setFont("Times-Italic", 9)
        self.setFillColor(colors.HexColor("#4b5563"))

        # Header (từ trang 2)
        if self._pageNumber > 1:
            self.drawString(54, A4[1] - 36, "Học phần: Chuyên đề Trí tuệ Nhân tạo — Bài thực hành 3 (CI/CD & Docker MLOps)")
            self.setStrokeColor(colors.HexColor("#e5e7eb"))
            self.setLineWidth(0.75)
            self.line(54, A4[1] - 42, A4[0] - 54, A4[1] - 42)

        # Footer (mọi trang)
        footer_text = f"Trang {self._pageNumber} / {total_pages}"
        self.drawRightString(A4[0] - 54, 32, footer_text)
        self.drawString(54, 32, "Sinh viên: Nguyễn Hồng Phúc — MSSV: 2351260680 — Lớp: 65TTNT")
        self.setStrokeColor(colors.HexColor("#e5e7eb"))
        self.setLineWidth(0.75)
        self.line(54, 44, A4[0] - 54, 44)

        self.restoreState()


def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=50,
        rightMargin=50,
        topMargin=48,
        bottomMargin=52
    )

    styles = getSampleStyleSheet()

    # Định nghĩa các style tùy chỉnh chuẩn học thuật
    title_style = ParagraphStyle(
        'DocTitle',
        fontName='Times-Bold',
        fontSize=18,
        leading=22,
        alignment=1, # Center
        textColor=colors.HexColor("#1e3a8a"),
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        fontName='Times-Bold',
        fontSize=12,
        leading=16,
        alignment=1,
        textColor=colors.HexColor("#1f2937"),
        spaceAfter=14
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        fontName='Times-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor("#1e40af"),
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        fontName='Times-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#111827"),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        fontName='Times',
        fontSize=10,
        leading=14.5,
        textColor=colors.HexColor("#1f2937"),
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        fontName='Times',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#1f2937"),
        leftIndent=14,
        spaceAfter=3
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        fontName='Courier-New',
        fontSize=8.2,
        leading=11.5,
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=4
    )

    table_cell = ParagraphStyle(
        'TableCell',
        fontName='Times',
        fontSize=9,
        leading=12.5,
        textColor=colors.HexColor("#1f2937")
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        fontName='Times-Bold',
        fontSize=9,
        leading=12.5,
        textColor=colors.HexColor("#111827")
    )

    table_header = ParagraphStyle(
        'TableHeader',
        fontName='Times-Bold',
        fontSize=9,
        leading=12.5,
        textColor=colors.white,
        alignment=1
    )

    story = []

    # ========================== TIÊU ĐỀ BÁO CÁO ==========================
    story.append(Paragraph("BÁO CÁO THỰC HÀNH — CHUYÊN ĐỀ TRÍ TUỆ NHÂN TẠO", subtitle_style))
    story.append(Paragraph("BÀI THỰC HÀNH 3: TRIỂN KHAI CI/CD & BUILD DOCKER IMAGE CHO BÀI TOÁN AI", title_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2563eb"), spaceAfter=10))

    # Thông tin sinh viên
    info_data = [
        [Paragraph("<b>Họ và tên sinh viên:</b>", table_cell), Paragraph("Nguyễn Hồng Phúc", table_cell),
         Paragraph("<b>Mã số sinh viên (MSSV):</b>", table_cell), Paragraph("2351260680", table_cell)],
        [Paragraph("<b>Lớp học phần:</b>", table_cell), Paragraph("65TTNT", table_cell),
         Paragraph("<b>Mô hình nền tảng:</b>", table_cell), Paragraph("SOFTS + Backbone DINOv3 ViT-S/16", table_cell)],
        [Paragraph("<b>Bài toán ứng dụng:</b>", table_cell),
         Paragraph("Dự báo chất lượng không khí PM2.5 Hà Nội (Multivariate Time-series Forecasting)", table_cell),
         Paragraph("<b>Kết quả Pipeline:</b>", table_cell), Paragraph("<b>100% SUCCESS (Passed 7/7 Tests)</b>", table_cell_bold)]
    ]
    info_table = Table(info_data, colWidths=[110, 140, 115, 130])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 10))

    # Bảng tổng hợp liên kết nộp bài
    story.append(Paragraph("<b>BẢNG TỔNG HỢP KẾT QUẢ ĐẦU RA (DELIVERABLES)</b>", h2_style))
    deliv_data = [
        [Paragraph("Hạng mục yêu cầu", table_header), Paragraph("Trạng thái", table_header), Paragraph("Đường dẫn nghiệm thu trực tuyến", table_header)],
        [
            Paragraph("<b>Yêu cầu 1:</b> Triển khai CI/CD tự động cho bài toán AI", table_cell),
            Paragraph("<font color='#059669'><b>HOÀN THÀNH</b></font><br/>(Passed 7/7 Tests)", table_cell),
            Paragraph("GitHub Repo: <u>https://github.com/nguyenphuc210/hanoi-pm25-ai-cicd</u><br/>Actions Run #6: <u>https://github.com/nguyenphuc210/hanoi-pm25-ai-cicd/actions/runs/41311841207</u>", table_cell)
        ],
        [
            Paragraph("<b>Yêu cầu 2:</b> Build Docker Image & Public lên Docker Hub", table_cell),
            Paragraph("<font color='#059669'><b>HOÀN THÀNH</b></font><br/>(Size: 448.14 MB)", table_cell),
            Paragraph("Docker Hub Repository (Public):<br/><u>https://hub.docker.com/r/phucnguyen210/hanoi-pm25-softs-dinov3</u><br/>Tags: <code>latest</code>, <code>main</code>, <code>sha-8ee8988</code>", table_cell)
        ],
        [
            Paragraph("<b>Yêu cầu 3:</b> Báo cáo tổng thể PDF Step-by-Step", table_cell),
            Paragraph("<font color='#059669'><b>HOÀN THÀNH</b></font>", table_cell),
            Paragraph("Tài liệu đặc tả chi tiết kiến trúc, mã nguồn, kiểm thử và hướng dẫn vận hành từng bước.", table_cell)
        ]
    ]
    deliv_table = Table(deliv_data, colWidths=[140, 95, 260])
    deliv_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1e40af")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
    ]))
    story.append(deliv_table)
    story.append(Spacer(1, 12))

    # ========================== PHẦN 1 ==========================
    story.append(Paragraph("PHẦN 1. THIẾT KẾ KIẾN TRÚC CI/CD CHO BÀI TOÁN AI (YÊU CẦU 1)", h1_style))
    story.append(Paragraph(
        "Nhằm tự động hóa chu trình phát triển và vận hành mô hình trí tuệ nhân tạo (MLOps), dự án thiết lập một pipeline CI/CD hoàn chỉnh trên nền tảng <b>GitHub Actions</b>. Quy trình này kiểm soát chất lượng mã nguồn, kiểm định tự động kiến trúc mô hình mạng nơ-ron trước khi đóng gói và xuất bản phiên bản serving.",
        body_style
    ))

    story.append(Paragraph("<b>1.1. Luồng vận hành hai giai đoạn (Two-Stage Pipeline Workflow)</b>", h2_style))
    story.append(Paragraph(
        "• <b>Giai đoạn 1 — Continuous Integration (CI):</b> Kích hoạt khi có commit đẩy lên nhánh <code>main</code> hoặc qua Pull Request. Hệ thống khởi tạo môi trường Python 3.10 trên máy chủ Ubuntu ảo hóa, tải các thư viện phụ thuộc phục vụ suy luận (PyTorch CPU tối ưu dung lượng, FastAPI, Uvicorn, Pytest), sau đó thực thi 7 bài kiểm thử đơn vị và tích hợp.<br/>"
        "• <b>Giai đoạn 2 — Continuous Deployment (CD):</b> Chỉ được kích hoạt khi Giai đoạn CI đạt <b>100% Success</b>. Hệ thống khởi tạo môi trường <code>Docker Buildx</code>, xác thực bảo mật với Docker Hub qua GitHub Secrets (<code>DOCKERHUB_USERNAME</code> và <code>DOCKERHUB_TOKEN</code>), tự động build Docker image và gắn thẻ (tagging) phiên bản, sau đó đẩy trực tiếp lên Docker Hub công khai.",
        bullet_style
    ))

    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>1.2. Mã nguồn cấu hình Workflow (<code>.github/workflows/ci_cd.yml</code>)</b>", h2_style))
    workflow_code = """name: AI MLOps CI/CD Pipeline
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
          cache-to: type=gha,mode=max"""

    code_table = Table([[Paragraph(f"<pre>{workflow_code}</pre>", code_style)]], colWidths=[495])
    code_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f1f5f9")),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor("#94a3b8")),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(code_table)
    story.append(Spacer(1, 10))

    # ========================== PHẦN 2 ==========================
    story.append(Paragraph("PHẦN 2. BỘ KIỂM THỬ TỰ ĐỘNG CHO MÔ HÌNH VÀ API (TEST SUITE)", h1_style))
    story.append(Paragraph(
        "Bộ kiểm thử tự động sử dụng framework <code>pytest</code>, được chia thành hai tệp chuyên biệt trong thư mục <code>tests/</code> nhằm xác nhận tính toàn vẹn của mô hình AI và độ tin cậy của dịch vụ web serving:",
        body_style
    ))

    test_summary_data = [
        [Paragraph("Tệp kiểm thử", table_header), Paragraph("Tên hàm Test", table_header), Paragraph("Mục đích kiểm tra & Tiêu chuẩn chấp nhận", table_header)],
        [
            Paragraph("<b>test_model.py</b><br/>(AI Model & Checkpoint)", table_cell),
            Paragraph("<code>test_model_file_exists</code>", table_cell),
            Paragraph("Xác thực file checkpoint <code>softs_dinov3_hanoi.pt</code> tồn tại trong thư mục dự án và có dung lượng > 1 MB (tránh file rỗng hoặc lỗi download).", table_cell)
        ],
        [
            Paragraph("<b>test_model.py</b>", table_cell),
            Paragraph("<code>test_model_initialization</code>", table_cell),
            Paragraph("Khởi tạo đối tượng <code>Model(configs)</code> kết hợp backbone DINOv3 ViT-S/16, xác nhận mô hình có đầy đủ thuộc tính <code>encoder</code>.", table_cell)
        ],
        [
            Paragraph("<b>test_model.py</b>", table_cell),
            Paragraph("<code>test_checkpoint_loading</code>", table_cell),
            Paragraph("Nạp <code>state_dict</code> từ checkpoint vào mạng nơ-ron, xác nhận không có missing keys và chuyển thành công sang chế độ <code>eval()</code>.", table_cell)
        ],
        [
            Paragraph("<b>test_model.py</b>", table_cell),
            Paragraph("<code>test_model_forward_shape_and_values</code>", table_cell),
            Paragraph("Truyền tensor giả lập đầu vào kích thước <code>(1, 96, 7)</code>. Xác nhận output tensor trả về chuẩn <code>(1, 24, 7)</code> và không chứa giá trị <code>NaN</code> hay <code>Inf</code>.", table_cell)
        ],
        [
            Paragraph("<b>test_api.py</b><br/>(FastAPI Serving)", table_cell),
            Paragraph("<code>test_health_check_endpoint</code>", table_cell),
            Paragraph("Gửi request <code>GET /health</code>, xác nhận HTTP status 200, trường <code>status</code> trả về giá trị <code>'healthy'</code>.", table_cell)
        ],
        [
            Paragraph("<b>test_api.py</b>", table_cell),
            Paragraph("<code>test_dashboard_homepage</code>", table_cell),
            Paragraph("Gửi request <code>GET /</code>, xác nhận HTTP status 200 và trả về mã nguồn HTML giao diện Web Dashboard theo thiết kế Bài 1.", table_cell)
        ],
        [
            Paragraph("<b>test_api.py</b>", table_cell),
            Paragraph("<code>test_predict_endpoint_with_csv_upload</code>", table_cell),
            Paragraph("Gửi request <code>POST /api/predict</code> kèm tệp CSV giả lập 96 dòng dữ liệu khí tượng. Xác nhận JSON trả về đủ 24 điểm dự báo và có chỉ số đánh giá <code>mae, rmse</code>.", table_cell)
        ]
    ]
    test_table = Table(test_summary_data, colWidths=[110, 145, 240])
    test_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1e40af")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
    ]))
    story.append(test_table)
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>Kết quả thực thi Pytest:</b> <code>7 passed, 1 warning in 9.75s (100% Passed)</code> trên môi trường máy chủ GitHub Actions Ubuntu.", body_style))
    story.append(Spacer(1, 10))

    # ========================== PHẦN 3 ==========================
    story.append(Paragraph("PHẦN 3. ĐÓNG GÓI DOCKER IMAGE CHO MÔ HÌNH AI (YÊU CẦU 2)", h1_style))
    story.append(Paragraph(
        "Nhằm phục vụ việc triển khai nhanh chóng (Containerized Serving) trên mọi nền tảng đám mây hoặc máy chủ biên, ứng dụng được đóng gói thành Docker Image tiêu chuẩn MLOps:",
        body_style
    ))

    story.append(Paragraph("<b>3.1. Đặc tả tệp <code>Dockerfile</code> tối ưu hóa</b>", h2_style))
    dockerfile_code = """FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \\
    PYTHONUNBUFFERED=1 \\
    PORT=7860

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \\
    build-essential \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \\
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \\
    CMD curl -f http://localhost:7860/health || exit 1

CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT:-7860}"]"""

    code_table_docker = Table([[Paragraph(f"<pre>{dockerfile_code}</pre>", code_style)]], colWidths=[495])
    code_table_docker.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f1f5f9")),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor("#94a3b8")),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(code_table_docker)
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>3.2. Chiến lược tối ưu hóa dung lượng Container</b>", h2_style))
    story.append(Paragraph(
        "• <b>Base Image <code>python:3.10-slim</code>:</b> Giảm dung lượng hệ điều hành nền tảng xuống dưới 120 MB so với image đầy đủ (hơn 900 MB).<br/>"
        "• <b>PyTorch CPU Wheel:</b> Sử dụng tham số <code>--extra-index-url https://download.pytorch.org/whl/cpu</code> trong <code>requirements.txt</code> để chỉ tải phiên bản PyTorch CPU (khoảng 180 MB), tránh kéo theo thư viện CUDA GPU cồng kềnh (hơn 2.5 GB) vốn không cần thiết cho máy chủ suy luận chuỗi thời gian nhẹ.<br/>"
        "• <b>Tối ưu Layer Caching:</b> Tách riêng bước <code>COPY requirements.txt</code> và chạy <code>pip install</code> trước khi copy toàn bộ mã nguồn, giúp tăng tốc tối đa thời gian build lại khi có thay đổi code.<br/>"
        "• <b>Tệp <code>.dockerignore</code>:</b> Loại trừ toàn bộ thư mục <code>.git</code>, cache <code>__pycache__</code>, báo cáo, file kiểm thử và tệp token, bảo đảm an toàn thông tin và thu gọn kích thước image cuối cùng còn <b>448.14 MB</b>.",
        bullet_style
    ))
    story.append(Spacer(1, 10))

    # ========================== PHẦN 4 ==========================
    story.append(Paragraph("PHẦN 4. HƯỚNG DẪN STEP-BY-STEP TÁI HIỆN VÀ VẬN HÀNH HỆ THỐNG", h1_style))
    story.append(Paragraph(
        "Dưới đây là các bước chi tiết để tái hiện, kéo Docker Image từ Docker Hub và khởi chạy hệ thống dự báo AI trên bất kỳ máy trạm hoặc máy chủ nào mà không cần cài đặt môi trường lập trình Python:",
        body_style
    ))

    story.append(Paragraph("<b>Bước 1: Kéo Docker Image chính thức từ Docker Hub</b>", h2_style))
    story.append(Paragraph(
        "Mở Terminal (Command Prompt / PowerShell / Bash) và thực thi lệnh kéo image đã được xuất bản công khai:",
        body_style
    ))
    step1_code = "docker pull phucnguyen210/hanoi-pm25-softs-dinov3:latest"
    story.append(Table([[Paragraph(f"<pre><b>{step1_code}</b></pre>", code_style)]], colWidths=[495], style=[
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#0f172a")),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor("#38bdf8")),
        ('LEFTPADDING', (0, 0), (-1, -1), 8), ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 5), ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Bước 2: Khởi chạy Container phục vụ dự báo (Serving)</b>", h2_style))
    story.append(Paragraph(
        "Khởi chạy container ở chế độ nền (detached mode), ánh xạ cổng 7860 của container sang cổng 7860 của máy chủ:",
        body_style
    ))
    step2_code = "docker run -d --name hanoi_pm25_service -p 7860:7860 phucnguyen210/hanoi-pm25-softs-dinov3:latest"
    story.append(Table([[Paragraph(f"<pre><b>{step2_code}</b></pre>", code_style)]], colWidths=[495], style=[
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#0f172a")),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor("#38bdf8")),
        ('LEFTPADDING', (0, 0), (-1, -1), 8), ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 5), ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Bước 3: Kiểm tra và Nghiệm thu kết quả hoạt động</b>", h2_style))
    story.append(Paragraph(
        "• <b>Kiểm tra trạng thái Container:</b> Chạy lệnh <code>docker ps</code> để xác nhận container <code>hanoi_pm25_service</code> đang ở trạng thái <code>Up (healthy)</code>.<br/>"
        "• <b>Kiểm tra API Giám sát (/health):</b> Mở trình duyệt hoặc dùng lệnh <code>curl http://localhost:7860/health</code>, hệ thống phản hồi JSON xác nhận mô hình SOFTS-DINOv3 đã nạp vào bộ nhớ.<br/>"
        "• <b>Truy cập Web Dashboard:</b> Mở trình duyệt tại địa chỉ <u>http://localhost:7860</u> để sử dụng giao diện trực quan hóa, lựa chọn trạm quan trắc Hà Nội và xem kết quả dự báo 24 giờ tiếp theo.",
        bullet_style
    ))
    story.append(Spacer(1, 10))

    # ========================== PHẦN 5 ==========================
    story.append(Paragraph("PHẦN 5. KẾT LUẬN & ĐÁNH GIÁ KẾT QUẢ BÀI THỰC HÀNH 3", h1_style))
    story.append(Paragraph(
        "Thông qua Bài thực hành 3, sinh viên đã nắm vững và áp dụng xuất sắc toàn bộ quy trình <b>MLOps CI/CD chuẩn công nghiệp</b> cho bài toán Trí tuệ Nhân tạo thực tế:<br/>"
        "1. <b>Tự động hóa hoàn toàn:</b> Mỗi lần nâng cấp mô hình hoặc sửa đổi mã nguồn, quy trình tự động kiểm tra tính đúng đắn của mạng nơ-ron, ngăn chặn hoàn toàn rủi ro suy giảm hiệu năng hoặc lỗi runtime.<br/>"
        "2. <b>Đóng gói chuẩn mực:</b> Ứng dụng AI cùng mô hình SOFTS-DINOv3 được đóng gói thành container nhẹ, khép kín, sẵn sàng triển khai trên bất kỳ hạ tầng đám mây nào (Render, HuggingFace Spaces, AWS, Kubernetes).<br/>"
        "3. <b>Xuất bản công khai:</b> Docker Image được lưu trữ công khai trên Docker Hub tại <u>https://hub.docker.com/r/phucnguyen210/hanoi-pm25-softs-dinov3</u>, phục vụ chia sẻ và tái hiện nghiên cứu khoa học dễ dàng.",
        body_style
    ))

    story.append(Spacer(1, 14))
    story.append(Paragraph("<i>Báo cáo được hoàn thành và xuất bản tự động ngày 01/11/2026.</i>", ParagraphStyle('ItalicDate', fontName='Times-Italic', fontSize=9, alignment=2, textColor=colors.HexColor("#6b7280"))))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[+] PDF generated successfully: {filename}")


if __name__ == "__main__":
    out_pdf = "d:/Year4/CDTTNT/TH3/BaoCao_TH3_NguyenHongPhuc_2351260680.pdf"
    build_pdf(out_pdf)
