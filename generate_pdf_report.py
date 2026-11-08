"""
Script tạo file PDF Báo cáo Bài thực hành 3 (CI/CD & Docker Hub)
Sinh viên: Nguyễn Hồng Phúc - MSSV: 2351260680 - Lớp: 65TTNT
Bổ sung mục: "CÁC BƯỚC TRIỂN KHAI STEP-BY-STEP CHI TIẾT"
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
        leftMargin=48,
        rightMargin=48,
        topMargin=46,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        fontName='Times-Bold',
        fontSize=17,
        leading=21,
        alignment=1, # Center
        textColor=colors.HexColor("#1e3a8a"),
        spaceAfter=5
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        fontName='Times-Bold',
        fontSize=11.5,
        leading=15,
        alignment=1,
        textColor=colors.HexColor("#1f2937"),
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        fontName='Times-Bold',
        fontSize=12.5,
        leading=16,
        textColor=colors.HexColor("#1e40af"),
        spaceBefore=11,
        spaceAfter=5,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        fontName='Times-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#111827"),
        spaceBefore=7,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        fontName='Times',
        fontSize=9.5,
        leading=13.8,
        textColor=colors.HexColor("#1f2937"),
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        fontName='Times',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#1f2937"),
        leftIndent=12,
        spaceAfter=3
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        fontName='Courier-New',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=3
    )

    table_cell = ParagraphStyle(
        'TableCell',
        fontName='Times',
        fontSize=8.8,
        leading=12,
        textColor=colors.HexColor("#1f2937")
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        fontName='Times-Bold',
        fontSize=8.8,
        leading=12,
        textColor=colors.HexColor("#111827")
    )

    table_header = ParagraphStyle(
        'TableHeader',
        fontName='Times-Bold',
        fontSize=8.8,
        leading=12,
        textColor=colors.white,
        alignment=1
    )

    story = []

    # ========================== TIÊU ĐỀ BÁO CÁO ==========================
    story.append(Paragraph("BÁO CÁO THỰC HÀNH — CHUYÊN ĐỀ TRÍ TUỆ NHÂN TẠO", subtitle_style))
    story.append(Paragraph("BÀI THỰC HÀNH 3: TRIỂN KHAI CI/CD & BUILD DOCKER IMAGE CHO BÀI TOÁN AI", title_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2563eb"), spaceAfter=8))

    # Thông tin sinh viên
    info_data = [
        [Paragraph("<b>Họ và tên sinh viên:</b>", table_cell), Paragraph("Nguyễn Hồng Phúc", table_cell),
         Paragraph("<b>Mã số sinh viên (MSSV):</b>", table_cell), Paragraph("2351260680", table_cell)],
        [Paragraph("<b>Lớp học phần:</b>", table_cell), Paragraph("65TTNT", table_cell),
         Paragraph("<b>Mô hình nền tảng:</b>", table_cell), Paragraph("SOFTS + Backbone DINOv3 ViT-S/16", table_cell)],
        [Paragraph("<b>Bài toán ứng dụng:</b>", table_cell),
         Paragraph("Dự báo ô nhiễm không khí PM2.5 Hà Nội (Multivariate Time-series Forecasting)", table_cell),
         Paragraph("<b>Kết quả Pipeline:</b>", table_cell), Paragraph("<b>100% SUCCESS (Passed 7/7 Tests)</b>", table_cell_bold)]
    ]
    info_table = Table(info_data, colWidths=[110, 140, 115, 134])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 8))

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
            Paragraph("Tài liệu đặc tả chi tiết kiến trúc, các bước kỹ thuật thực tế và hướng dẫn vận hành.", table_cell)
        ]
    ]
    deliv_table = Table(deliv_data, colWidths=[140, 95, 264])
    deliv_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1e40af")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
    ]))
    story.append(deliv_table)
    story.append(Spacer(1, 10))

    # ========================== PHẦN 1 ==========================
    story.append(Paragraph("PHẦN 1. THIẾT KẾ KIẾN TRÚC CI/CD CHO BÀI TOÁN AI (YÊU CẦU 1)", h1_style))
    story.append(Paragraph(
        "Nhằm tự động hóa toàn diện chu trình phát triển và vận hành mô hình học sâu (MLOps), dự án xây dựng một pipeline CI/CD hai giai đoạn trên nền tảng <b>GitHub Actions</b> kết hợp <b>Docker Hub</b>:",
        body_style
    ))
    story.append(Paragraph(
        "• <b>Giai đoạn 1 — Continuous Integration (CI):</b> Kích hoạt tự động khi có mã nguồn mới đẩy lên nhánh <code>main</code>. Môi trường Ubuntu ảo hóa nạp Python 3.10, cài đặt thư viện phụ thuộc tối ưu PyTorch CPU và thực thi 7 bài kiểm thử đơn vị, kiểm tra sự toàn vẹn của mô hình nơ-ron trước khi xuất bản.<br/>"
        "• <b>Giai đoạn 2 — Continuous Deployment (CD):</b> Kích hoạt khi CI đạt 100% Success. Hệ thống nạp chứng chỉ Docker Hub bí mật (GitHub Secrets), dùng <code>Docker Buildx</code> đóng gói container và tự động gắn nhãn (tags), sau đó đẩy trực tiếp lên kho lưu trữ Docker Hub công khai.",
        bullet_style
    ))
    story.append(Spacer(1, 8))

    # ========================== PHẦN 2 (MỚI: CÁC BƯỚC TRIỂN KHAI STEP-BY-STEP) ==========================
    story.append(Paragraph("PHẦN 2. CÁC BƯỚC THỰC HIỆN STEP-BY-STEP TRIỂN KHAI CI/CD & DOCKER", h1_style))
    story.append(Paragraph(
        "Dưới đây là chi tiết 8 bước kỹ thuật tuần tự mà sinh viên đã trực tiếp thực hiện để hoàn thiện toàn bộ hệ sinh thái CI/CD và Docker Hub cho bài toán AI:",
        body_style
    ))

    steps_data = [
        [Paragraph("Bước thực hiện", table_header), Paragraph("Thao tác kỹ thuật chi tiết & Công cụ áp dụng", table_header), Paragraph("Kết quả nghiệm thu", table_header)],
        [
            Paragraph("<b>Bước 1</b><br/>Chuẩn bị mã nguồn & mô hình AI", table_cell),
            Paragraph("Tập hợp cấu trúc mạng <code>models/SOFTS.py</code>, backbone thị giác <code>layers/DINOv3Encoder.py</code>, API engine <code>app.py</code> (FastAPI) và checkpoint trọng số <code>softs_dinov3_hanoi.pt</code> (3.84 MB).", table_cell),
            Paragraph("Mã nguồn sẵn sàng, tệp trọng số nhẹ nạp trực tiếp vào Git an toàn.", table_cell)
        ],
        [
            Paragraph("<b>Bước 2</b><br/>Thiết kế Test Suite (Pytest)", table_cell),
            Paragraph("Viết 4 hàm test kiểm tra mô hình trong <code>test_model.py</code> (sự tồn tại file, khởi tạo kiến trúc, nạp state_dict, suy luận tensor 96h -> 24h) và 3 hàm test API trong <code>test_api.py</code> (endpoint /health, /, /api/predict).", table_cell),
            Paragraph("Chạy lệnh <code>pytest tests/ -v</code> trên máy đạt <b>7/7 Passed</b> trong 9.75 giây.", table_cell)
        ],
        [
            Paragraph("<b>Bước 3</b><br/>Viết Dockerfile & Tối ưu dung lượng", table_cell),
            Paragraph("Sử dụng base image <code>python:3.10-slim</code>. Trong <code>requirements.txt</code> trỏ link PyTorch CPU Wheel. Thiết lập tệp <code>.dockerignore</code> loại trừ file tạm và token bảo mật. Cấu hình <code>HEALTHCHECK</code> gọi <code>/health</code>.", table_cell),
            Paragraph("Giảm kích thước image từ >2.5 GB xuống còn <b>448.14 MB</b>, tăng tốc tải kéo.", table_cell)
        ],
        [
            Paragraph("<b>Bước 4</b><br/>Cấu hình Secrets trên Docker Hub & GitHub", table_cell),
            Paragraph("Đăng nhập Docker Hub (tài khoản <code>phucnguyen210</code>), tạo Personal Access Token (PAT) quyền Read & Write. Thêm 2 secret trong GitHub Repository: <code>DOCKERHUB_USERNAME</code> và <code>DOCKERHUB_TOKEN</code>.", table_cell),
            Paragraph("Xác thực CI/CD bảo mật tuyệt đối, không lộ mật khẩu cá nhân.", table_cell)
        ],
        [
            Paragraph("<b>Bước 5</b><br/>Viết Workflow GitHub Actions", table_cell),
            Paragraph("Tạo <code>.github/workflows/ci_cd.yml</code> gồm 2 job: <code>ci_test_and_validation</code> (chạy pytest) và <code>cd_docker_hub_publish</code> (dùng Docker Buildx đóng gói và push image khi CI xanh lá).", table_cell),
            Paragraph("Tự động hóa hoàn toàn quy trình đóng gói sau mỗi lần commit.", table_cell)
        ],
        [
            Paragraph("<b>Bước 6</b><br/>Khởi tạo Git & Đẩy code lên GitHub", table_cell),
            Paragraph("Thực hiện <code>git init -b main</code>, commit toàn bộ mã nguồn và liên kết remote <code>origin https://github.com/nguyenphuc210/hanoi-pm25-ai-cicd.git</code>, sau đó chạy <code>git push -u origin main</code>.", table_cell),
            Paragraph("Kho lưu trữ GitHub công khai được tạo lập và kích hoạt pipeline.", table_cell)
        ],
        [
            Paragraph("<b>Bước 7</b><br/>Giám sát & Xử lý lỗi trong CI/CD", table_cell),
            Paragraph("Theo dõi tiến trình chạy trên tab Actions. Xử lý kịp thời sai lệch Docker ID, điều chỉnh tham số fallback trong workflow. Đợt chạy <b>Run #6</b> đạt trạng thái <b>100% Success</b> ở cả 2 giai đoạn.", table_cell),
            Paragraph("CI hoàn thành trong 45s; CD build & push hoàn thành trong 1m12s.", table_cell)
        ],
        [
            Paragraph("<b>Bước 8</b><br/>Kiểm thử & Nghiệm thu từ xa", table_cell),
            Paragraph("Kiểm tra image trên Docker Hub (3 tags: latest, main, sha). Kéo image về máy trạm bằng <code>docker pull</code>, chạy container với <code>docker run -d -p 7860:7860</code> và kiểm tra web dashboard.", table_cell),
            Paragraph("Hệ thống hoạt động trơn tru, dự báo 24 giờ liên tục theo giờ chẵn.", table_cell)
        ]
    ]
    steps_table = Table(steps_data, colWidths=[95, 275, 129])
    steps_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1e40af")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
    ]))
    story.append(steps_table)
    story.append(Spacer(1, 10))

    # ========================== PHẦN 3 ==========================
    story.append(Paragraph("PHẦN 3. BỘ KIỂM THỬ TỰ ĐỘNG CHO MÔ HÌNH VÀ API (TEST SUITE)", h1_style))
    story.append(Paragraph(
        "Bộ kiểm thử tự động sử dụng framework <code>pytest</code>, chia thành hai tệp chuyên biệt trong thư mục <code>tests/</code>:",
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
    test_table = Table(test_summary_data, colWidths=[110, 145, 244])
    test_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1e40af")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
    ]))
    story.append(test_table)
    story.append(Spacer(1, 5))
    story.append(Paragraph("<b>Kết quả thực thi Pytest:</b> <code>7 passed, 1 warning in 9.75s (100% Passed)</code> trên máy chủ Ubuntu của GitHub Actions.", body_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Ý nghĩa chung của 7 bài test:</b> Đóng vai trò là <i>Cổng chất lượng tự động (Quality Gate)</i>. Trong Deep Learning, mô hình rất dễ gặp lỗi ngầm (silent bugs: thiếu layers, kích thước tensor sai, tràn số sinh NaN/Inf). 7 bài test này đảm bảo 100% tính toàn vẹn toán học của mô hình và tính sẵn sàng phục vụ thực tế của API.", body_style))
    story.append(Spacer(1, 3))
    story.append(Paragraph("<b>Ý nghĩa cốt lõi của CI/CD cho AI:</b> Tự động hóa hoàn toàn chu trình kiểm thử và đóng gói; xóa bỏ triệt để xung đột môi trường (Environment Parity) giữa máy cá nhân và production; tăng tốc độ chuyển giao (deployment velocity) và bảo đảm độ tin cậy liên tục cho mô hình dự báo.", body_style))
    story.append(Spacer(1, 6))

    # ========================== PHẦN 4 ==========================
    story.append(Paragraph("PHẦN 4. ĐÓNG GÓI DOCKER IMAGE CHO MÔ HÌNH AI (YÊU CẦU 2)", h1_style))
    story.append(Paragraph(
        "Ứng dụng AI được đóng gói thành container nhẹ theo tiêu chuẩn MLOps thông qua tệp <code>Dockerfile</code> tối ưu:",
        body_style
    ))

    dockerfile_code = """FROM python:3.10-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PORT=7860
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends build-essential curl && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 7860
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 CMD curl -f http://localhost:7860/health || exit 1
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT:-7860}"]"""

    code_table_docker = Table([[Paragraph(f"<pre>{dockerfile_code}</pre>", code_style)]], colWidths=[499])
    code_table_docker.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f1f5f9")),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor("#94a3b8")),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(code_table_docker)
    story.append(Spacer(1, 8))

    # ========================== PHẦN 5 ==========================
    story.append(Paragraph("PHẦN 5. HƯỚNG DẪN STEP-BY-STEP ĐỂ CLONE VÀ CHẠY DỰ ÁN", h1_style))
    story.append(Paragraph(
        "Người khác (thầy cô, người phản biện hoặc người dùng mới) có thể clone và vận hành hệ thống theo 1 trong 3 phương thức linh hoạt:",
        body_style
    ))

    story.append(Paragraph("<b>Phương thức 1: Chạy trực tiếp từ Docker Hub (Nhanh nhất — Không cần cài Python)</b>", h2_style))
    p1_code = "docker pull phucnguyen210/hanoi-pm25-softs-dinov3:latest\ndocker run -d --name hanoi_pm25_service -p 7860:7860 phucnguyen210/hanoi-pm25-softs-dinov3:latest"
    story.append(Table([[Paragraph(f"<pre><b>{p1_code}</b></pre>", code_style)]], colWidths=[499], style=[
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#0f172a")),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor("#38bdf8")),
        ('LEFTPADDING', (0, 0), (-1, -1), 7), ('RIGHTPADDING', (0, 0), (-1, -1), 7),
        ('TOPPADDING', (0, 0), (-1, -1), 3), ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>Phương thức 2: Clone repository và Tự build Docker Image cục bộ</b>", h2_style))
    p2_code = "git clone https://github.com/nguyenphuc210/hanoi-pm25-ai-cicd.git\ncd hanoi-pm25-ai-cicd\ndocker build -t hanoi-pm25-local:latest .\ndocker run -d --name hanoi_local_app -p 7860:7860 hanoi-pm25-local:latest"
    story.append(Table([[Paragraph(f"<pre><b>{p2_code}</b></pre>", code_style)]], colWidths=[499], style=[
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#0f172a")),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor("#38bdf8")),
        ('LEFTPADDING', (0, 0), (-1, -1), 7), ('RIGHTPADDING', (0, 0), (-1, -1), 7),
        ('TOPPADDING', (0, 0), (-1, -1), 3), ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>Phương thức 3: Clone repository và Chạy với môi trường Python cục bộ</b>", h2_style))
    p3_code = "git clone https://github.com/nguyenphuc210/hanoi-pm25-ai-cicd.git\ncd hanoi-pm25-ai-cicd\npython -m venv venv && venv\\Scripts\\activate\npip install -r requirements.txt\npython -m pytest tests/ -v\npython -m uvicorn app:app --host 0.0.0.0 --port 7860"
    story.append(Table([[Paragraph(f"<pre><b>{p3_code}</b></pre>", code_style)]], colWidths=[499], style=[
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#0f172a")),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor("#38bdf8")),
        ('LEFTPADDING', (0, 0), (-1, -1), 7), ('RIGHTPADDING', (0, 0), (-1, -1), 7),
        ('TOPPADDING', (0, 0), (-1, -1), 3), ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(Spacer(1, 4))

    story.append(Paragraph(
        "• <b>Nghiệm thu Web Dashboard:</b> Mở trình duyệt tại <u>http://localhost:7860</u> để sử dụng giao diện trực quan hóa, lựa chọn trạm quan trắc Hà Nội và xem kết quả dự báo 24 giờ tiếp theo.<br/>"
        "• <b>Kiểm tra API Sức khỏe:</b> Gọi <code>curl http://localhost:7860/health</code>, hệ thống trả về JSON xác nhận mô hình SOFTS-DINOv3 đang hoạt động ổn định.",
        bullet_style
    ))
    story.append(Spacer(1, 6))

    # ========================== PHẦN 6 ==========================
    story.append(Paragraph("PHẦN 6. KẾT LUẬN & ĐÁNH GIÁ HIỆU QUẢ", h1_style))
    story.append(Paragraph(
        "Bài thực hành 3 đã hoàn thành xuất sắc toàn diện 100% các mục tiêu:<br/>"
        "1. Xây dựng thành công quy trình **CI/CD chuẩn MLOps**, tự động hóa từ kiểm thử mã nguồn đến đóng gói và xuất bản.<br/>"
        "2. Đóng gói thành công **Docker Image gọn nhẹ (448.14 MB)**, phát hành công khai trên Docker Hub tại <u>https://hub.docker.com/r/phucnguyen210/hanoi-pm25-softs-dinov3</u>.<br/>"
        "3. Đảm bảo tính nhất quán giữa lý thuyết nghiên cứu học sâu và năng lực triển khai thực tế trong công nghiệp phần mềm AI.",
        body_style
    ))

    story.append(Spacer(1, 10))
    story.append(Paragraph("<i>Báo cáo được hoàn thành và xuất bản tự động ngày 08/11/2026.</i>", ParagraphStyle('ItalicDate', fontName='Times-Italic', fontSize=8.5, alignment=2, textColor=colors.HexColor("#6b7280"))))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[+] PDF generated successfully: {filename}")


if __name__ == "__main__":
    out_pdf = "d:/Year4/CDTTNT/TH3/BaoCao_TH3_NguyenHongPhuc_2351260680.pdf"
    build_pdf(out_pdf)
