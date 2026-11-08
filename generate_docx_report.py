"""
Tạo file Word .docx Báo cáo Bài thực hành 3 (Bổ sung phần 8 bước triển khai chi tiết)
Sinh viên: Nguyễn Hồng Phúc - MSSV: 2351260680 - Lớp: 65TTNT
"""

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn


def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)


def build_docx(filename):
    doc = docx.Document()
    for section in doc.sections:
        section.top_margin = Inches(0.7)
        section.bottom_margin = Inches(0.7)
        section.left_margin = Inches(0.7)
        section.right_margin = Inches(0.7)

    # Tiêu đề
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run("BÁO CÁO THỰC HÀNH — CHUYÊN ĐỀ TRÍ TUỆ NHÂN TẠO")
    r_sub.font.name = "Times New Roman"
    r_sub.font.size = Pt(11.5)
    r_sub.font.bold = True
    r_sub.font.color.rgb = RGBColor(0x37, 0x41, 0x51)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("BÀI THỰC HÀNH 3: TRIỂN KHAI CI/CD & BUILD DOCKER IMAGE CHO BÀI TOÁN AI")
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(15)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(0x1e, 0x3a, 0x8a)

    # Thông tin sinh viên
    table_info = doc.add_table(rows=3, cols=2)
    table_info.alignment = WD_TABLE_ALIGNMENT.CENTER
    info_rows = [
        ("Họ và tên sinh viên: Nguyễn Hồng Phúc", "Mã số sinh viên (MSSV): 2351260680"),
        ("Lớp học phần: 65TTNT", "Mô hình: SOFTS + Backbone DINOv3 ViT-S/16"),
        ("Bài toán: Dự báo ô nhiễm PM2.5 Hà Nội", "Kết quả Pipeline: 100% SUCCESS (Passed 7/7 Tests)")
    ]
    for row_idx, (c0, c1) in enumerate(info_rows):
        row = table_info.rows[row_idx]
        row.cells[0].text = c0
        row.cells[1].text = c1
        for cell in row.cells:
            set_cell_background(cell, "F8FAFC")
            for p in cell.paragraphs:
                for r in p.runs:
                    r.font.name = "Times New Roman"
                    r.font.size = Pt(10)

    doc.add_paragraph()

    # Bảng kết quả nộp bài
    h_sum = doc.add_heading("BẢNG TỔNG HỢP KẾT QUẢ ĐẦU RA (DELIVERABLES)", level=2)
    for r in h_sum.runs:
        r.font.name = "Times New Roman"
        r.font.color.rgb = RGBColor(0x1e, 0x40, 0xaf)

    table_res = doc.add_table(rows=4, cols=3)
    table_res.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Hạng mục yêu cầu", "Trạng thái", "Đường dẫn nghiệm thu trực tuyến"]
    for i, h in enumerate(headers):
        cell = table_res.rows[0].cells[i]
        cell.text = h
        set_cell_background(cell, "1E40AF")
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.font.name = "Times New Roman"
                r.font.bold = True
                r.font.color.rgb = RGBColor(0xff, 0xff, 0xff)

    items = [
        ("Yêu cầu 1: Triển khai CI/CD tự động cho bài toán AI", "HOÀN THÀNH (100% Tests Passed)",
         "GitHub Repo: https://github.com/nguyenphuc210/hanoi-pm25-ai-cicd\nActions Run #6: https://github.com/nguyenphuc210/hanoi-pm25-ai-cicd/actions/runs/41311841207"),
        ("Yêu cầu 2: Build Docker Image & Public lên Docker Hub", "HOÀN THÀNH (Dung lượng: 448.14 MB)",
         "Docker Hub Public Repository:\nhttps://hub.docker.com/r/phucnguyen210/hanoi-pm25-softs-dinov3\nTags: latest, main, sha-8ee8988"),
        ("Yêu cầu 3: Báo cáo PDF Step-by-Step", "HOÀN THÀNH",
         "Tài liệu đặc tả chi tiết kiến trúc, các bước kỹ thuật thực tế và hướng dẫn vận hành.")
    ]
    for row_idx, (c0, c1, c2) in enumerate(items, start=1):
        row = table_res.rows[row_idx]
        row.cells[0].text = c0
        row.cells[1].text = c1
        row.cells[2].text = c2
        bg = "FFFFFF" if row_idx % 2 == 1 else "F8FAFC"
        for cell in row.cells:
            set_cell_background(cell, bg)
            for p in cell.paragraphs:
                for r in p.runs:
                    r.font.name = "Times New Roman"
                    r.font.size = Pt(9.5)

    doc.add_paragraph()

    # PHẦN 2 MỚI: 8 BƯỚC TRIỂN KHAI STEP-BY-STEP
    h_steps = doc.add_heading("PHẦN 2. CÁC BƯỚC THỰC HIỆN STEP-BY-STEP TRIỂN KHAI CI/CD & DOCKER", level=1)
    for r in h_steps.runs:
        r.font.name = "Times New Roman"
        r.font.size = Pt(13)
        r.font.color.rgb = RGBColor(0x1e, 0x40, 0xaf)

    steps_list = [
        ("Bước 1: Chuẩn bị mã nguồn & mô hình AI",
         "Tập hợp cấu trúc mạng models/SOFTS.py, backbone layers/DINOv3Encoder.py, backend app.py (FastAPI) và file checkpoint trọng số softs_dinov3_hanoi.pt (3.84 MB, đẩy được trực tiếp vào Git)."),
        ("Bước 2: Thiết kế Test Suite (Pytest)",
         "Xây dựng tests/test_model.py (kiểm tra tồn tại weights, khởi tạo mạng, nạp state_dict, suy luận tensor shape 96h -> 24h) và tests/test_api.py (kiểm tra endpoint /health, /, /api/predict). Nghiệm thu cục bộ đạt 7/7 bài test passed."),
        ("Bước 3: Viết Dockerfile & Tối ưu dung lượng",
         "Sử dụng base image python:3.10-slim. Trong requirements.txt trỏ link PyTorch CPU Wheel để giảm dung lượng từ >2.5 GB xuống còn 448.14 MB. Viết .dockerignore loại trừ file rác và token."),
        ("Bước 4: Cấu hình Secrets trên Docker Hub & GitHub",
         "Đăng nhập Docker Hub với tài khoản phucnguyen210, tạo Personal Access Token (PAT) quyền Read & Write. Cấu hình 2 biến bí mật DOCKERHUB_USERNAME và DOCKERHUB_TOKEN trong GitHub Repository Secrets."),
        ("Bước 5: Viết Workflow GitHub Actions (.github/workflows/ci_cd.yml)",
         "Thiết lập pipeline tự động 2 giai đoạn: CI (chạy pytest trên Ubuntu sạch) và CD (dùng Docker Buildx đóng gói và tự động đẩy image lên Docker Hub khi CI vượt qua 100%)."),
        ("Bước 6: Khởi tạo Git & Đẩy code lên GitHub",
         "Thực hiện git init -b main, commit mã nguồn, kết nối remote origin trỏ về repo nguyenphuc210/hanoi-pm25-ai-cicd và đẩy lên bằng git push -u origin main."),
        ("Bước 7: Giám sát & Xử lý lỗi trong CI/CD",
         "Theo dõi tiến trình chạy trên GitHub Actions. Khắc phục sai lệch Docker ID, điều chỉnh fallback an toàn trong workflow. Đợt chạy Run #6 đạt 100% SUCCESS cả 2 giai đoạn CI (45s) và CD (1m12s)."),
        ("Bước 8: Kiểm thử & Nghiệm thu từ xa",
         "Kiểm tra image công khai trên Docker Hub với 3 tags (latest, main, sha). Kéo image về máy trạm bằng docker pull, khởi chạy container cổng 7860 và xác nhận dashboard hoạt động mượt mà.")
    ]

    for title_s, desc_s in steps_list:
        p_s = doc.add_paragraph()
        r_title_s = p_s.add_run(f"• {title_s}: ")
        r_title_s.font.name = "Times New Roman"
        r_title_s.font.size = Pt(10.5)
        r_title_s.font.bold = True
        r_desc_s = p_s.add_run(desc_s)
        r_desc_s.font.name = "Times New Roman"
        r_desc_s.font.size = Pt(10)

    doc.add_paragraph()

    # Các phần lý thuyết và kết luận
    other_sections = [
        ("PHẦN 3. BỘ KIỂM THỬ TỰ ĐỘNG (UNIT & INTEGRATION TESTS)", [
            "Bộ kiểm thử được viết bằng pytest gồm 2 module kiểm tra toàn vẹn trọng số nơ-ron, forward pass tensor và serving API. Kết quả: 7 passed in 9.75s trên môi trường Ubuntu của GitHub Actions."
        ]),
        ("PHẦN 4. ĐÓNG GÓI DOCKER IMAGE CHO MÔ HÌNH AI", [
            "Ứng dụng được đóng gói qua Dockerfile chuẩn MLOps, sử dụng python:3.10-slim và PyTorch CPU, tối ưu layer caching và tích hợp HEALTHCHECK định kỳ."
        ]),
        ("PHẦN 5. HƯỚNG DẪN STEP-BY-STEP ĐỂ CLONE VÀ CHẠY DỰ ÁN", [
            "Người khác (thầy cô, người phản biện hoặc người dùng mới) có thể vận hành hệ thống theo 1 trong 3 phương thức linh hoạt:",
            "• Phương thức 1: Chạy trực tiếp từ Docker Hub (Nhanh nhất — Không cần cài Python):",
            "     docker pull phucnguyen210/hanoi-pm25-softs-dinov3:latest",
            "     docker run -d --name hanoi_pm25_service -p 7860:7860 phucnguyen210/hanoi-pm25-softs-dinov3:latest",
            "• Phương thức 2: Clone repository và Tự build Docker Image cục bộ:",
            "     git clone https://github.com/nguyenphuc210/hanoi-pm25-ai-cicd.git",
            "     cd hanoi-pm25-ai-cicd",
            "     docker build -t hanoi-pm25-local:latest .",
            "     docker run -d --name hanoi_local_app -p 7860:7860 hanoi-pm25-local:latest",
            "• Phương thức 3: Clone repository và Chạy với môi trường Python cục bộ:",
            "     git clone https://github.com/nguyenphuc210/hanoi-pm25-ai-cicd.git",
            "     cd hanoi-pm25-ai-cicd",
            "     python -m venv venv && venv\\Scripts\\activate",
            "     pip install -r requirements.txt",
            "     python -m pytest tests/ -v",
            "     python -m uvicorn app:app --host 0.0.0.0 --port 7860",
            "• Truy cập Web Dashboard: http://localhost:7860",
            "• Kiểm tra API Healthcheck: curl http://localhost:7860/health"
        ]),
        ("PHẦN 6. KẾT LUẬN", [
            "Bài thực hành 3 đã hoàn thành xuất sắc 100% mục tiêu: tự động hóa CI/CD cho mô hình AI và đóng gói xuất bản Docker image công khai lên Docker Hub."
        ])
    ]

    for sec_title, sec_paragraphs in other_sections:
        h = doc.add_heading(sec_title, level=1)
        for r in h.runs:
            r.font.name = "Times New Roman"
            r.font.size = Pt(12.5)
            r.font.color.rgb = RGBColor(0x1e, 0x40, 0xaf)
        for p_text in sec_paragraphs:
            p = doc.add_paragraph()
            r = p.add_run(p_text)
            r.font.name = "Times New Roman"
            r.font.size = Pt(10)

    doc.save(filename)
    print(f"[+] DOCX generated successfully: {filename}")


if __name__ == "__main__":
    out_docx = "d:/Year4/CDTTNT/TH3/BaoCao_TH3_NguyenHongPhuc_2351260680_StepByStep.docx"
    build_docx(out_docx)
    try:
        import shutil
        shutil.copyfile(out_docx, "d:/Year4/CDTTNT/TH3/BaoCao_TH3_NguyenHongPhuc_2351260680.docx")
        print("[+] Also updated BaoCao_TH3_NguyenHongPhuc_2351260680.docx")
    except Exception as e:
        print("[i] Main docx is currently open in Word, saved to StepByStep docx successfully!")
