"""
Tạo file Word .docx Báo cáo Bài thực hành 3
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
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    # Tiêu đề
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run("BÁO CÁO THỰC HÀNH — CHUYÊN ĐỀ TRÍ TUỆ NHÂN TẠO")
    r_sub.font.name = "Times New Roman"
    r_sub.font.size = Pt(12)
    r_sub.font.bold = True
    r_sub.font.color.rgb = RGBColor(0x37, 0x41, 0x51)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("BÀI THỰC HÀNH 3: TRIỂN KHAI CI/CD & BUILD DOCKER IMAGE CHO BÀI TOÁN AI")
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(16)
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
        ("Yêu cầu 2: Build Docker Image & Public lên Docker Hub", "HOÀN THÀNH (Dung lượng: 448 MB)",
         "Docker Hub Public Repository:\nhttps://hub.docker.com/r/phucnguyen210/hanoi-pm25-softs-dinov3\nTags: latest, main, sha-8ee8988"),
        ("Yêu cầu 3: Báo cáo PDF Step-by-Step", "HOÀN THÀNH",
         "Tài liệu đặc tả kiến trúc, mã nguồn, kiểm thử và hướng dẫn vận hành từng bước.")
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

    # Nội dung chi tiết các phần
    sections_text = [
        ("PHẦN 1. THIẾT KẾ KIẾN TRÚC CI/CD CHO BÀI TOÁN AI (YÊU CẦU 1)", [
            "Hệ thống MLOps CI/CD được xây dựng hoàn toàn tự động dựa trên GitHub Actions và Docker Hub:",
            "• Giai đoạn 1 — Continuous Integration (CI): Tự động kiểm thử mô hình mạng nơ-ron (SOFTS + DINOv3 ViT-S/16) và API serving trên môi trường Ubuntu sạch với Python 3.10 và PyTorch CPU. Chạy bộ kiểm thử 7/7 bài test.",
            "• Giai đoạn 2 — Continuous Deployment (CD): Chỉ chạy khi CI vượt qua 100%. Tự động kết nối Docker Hub bằng Personal Access Token, build Docker image và gắn nhãn (latest, git sha), sau đó xuất bản công khai lên Docker Hub."
        ]),
        ("PHẦN 2. BỘ KIỂM THỬ TỰ ĐỘNG (UNIT & INTEGRATION TESTS)", [
            "Bộ kiểm thử được viết bằng thư viện pytest gồm 2 module:",
            "1. tests/test_model.py: Xác thực sự tồn tại của file checkpoint softs_dinov3_hanoi.pt (> 1 MB), kiểm tra khởi tạo mô hình với DINOv3Encoder, nạp state_dict không lỗi, và suy luận forward pass tensor đầu vào (1, 96, 7) cho ra đúng output (1, 24, 7) không chứa NaN hay Inf.",
            "2. tests/test_api.py: Kiểm tra endpoint GET /health trả về trạng thái healthy, endpoint GET / trả về dashboard, và endpoint POST /api/predict suy luận offline từ file CSV mẫu trả về đủ 24 điểm dự báo cùng các thông số đánh giá động MAE, RMSE."
        ]),
        ("PHẦN 3. ĐÓNG GÓI DOCKER CONTAINER CHO MÔ HÌNH AI (YÊU CẦU 2)", [
            "• Base image: python:3.10-slim tối ưu dung lượng hệ điều hành (< 120 MB).",
            "• PyTorch CPU: Cài đặt qua tham số --extra-index-url https://download.pytorch.org/whl/cpu giúp giảm hơn 2.3 GB so với PyTorch GPU CUDA.",
            "• Layer Caching & .dockerignore: Tách biệt COPY requirements.txt để cache dependencies, loại trừ các file rác và token bảo mật, giúp image cuối cùng có dung lượng nén chỉ 448.14 MB.",
            "• Healthcheck: Tích hợp lệnh curl định kỳ tới /health đảm bảo container luôn sẵn sàng phục vụ."
        ]),
        ("PHẦN 4. HƯỚNG DẪN STEP-BY-STEP TÁI HIỆN VÀ VẬN HÀNH HỆ THỐNG", [
            "Bất kỳ máy tính hoặc máy chủ nào có Docker đều có thể vận hành hệ thống chỉ với 2 lệnh:",
            "Bước 1: Kéo Image từ Docker Hub:",
            "   docker pull phucnguyen210/hanoi-pm25-softs-dinov3:latest",
            "Bước 2: Khởi chạy Container phục vụ:",
            "   docker run -d --name hanoi_pm25_service -p 7860:7860 phucnguyen210/hanoi-pm25-softs-dinov3:latest",
            "Bước 3: Truy cập nghiệm thu:",
            "   - Web Dashboard: http://localhost:7860",
            "   - Endpoint kiểm tra sức khỏe: http://localhost:7860/health"
        ]),
        ("PHẦN 5. KẾT LUẬN", [
            "Bài thực hành 3 đã hoàn thành xuất sắc 100% mục tiêu: triển khai thành công CI/CD pipeline tự động hóa cho mô hình AI và đóng gói xuất bản Docker image công khai lên Docker Hub. Toàn bộ mã nguồn, workflow và image đều sẵn sàng phục vụ kiểm thử và triển khai thực tế."
        ])
    ]

    for sec_title, sec_paragraphs in sections_text:
        h = doc.add_heading(sec_title, level=1)
        for r in h.runs:
            r.font.name = "Times New Roman"
            r.font.size = Pt(13)
            r.font.color.rgb = RGBColor(0x1e, 0x40, 0xaf)
        for p_text in sec_paragraphs:
            p = doc.add_paragraph()
            r = p.add_run(p_text)
            r.font.name = "Times New Roman"
            r.font.size = Pt(10.5)

    doc.save(filename)
    print(f"[+] DOCX generated successfully: {filename}")


if __name__ == "__main__":
    out_docx = "d:/Year4/CDTTNT/TH3/BaoCao_TH3_NguyenHongPhuc_2351260680.docx"
    build_docx(out_docx)
