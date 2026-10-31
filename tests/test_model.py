"""
Unit Tests for SOFTS-DINOv3 AI Model Checkpoint and Inference
Author: Nguyen Hong Phuc (2351260680 - 65TTNT)
"""

import os
import pytest
import torch
import numpy as np

from models.SOFTS import Model


class ModelConfigs:
    seq_len = 96
    pred_len = 24
    d_model = 128
    d_core = 32
    d_ff = 256
    dropout = 0.05
    e_layers = 2
    activation = "gelu"
    use_norm = True
    dinov3_pretrained = False
    dinov3_layers = 2
    dinov3_dim = 192
    dinov3_heads = 6
    dinov3_mlp_ratio = 4.0
    dinov3_registers = 4


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "softs_dinov3_hanoi.pt")


def test_model_file_exists():
    """Kiểm tra file trọng số mô hình softs_dinov3_hanoi.pt tồn tại"""
    assert os.path.exists(MODEL_PATH), f"Model checkpoint không tồn tại tại {MODEL_PATH}"
    file_size_mb = os.path.getsize(MODEL_PATH) / (1024 * 1024)
    assert file_size_mb > 1.0, f"Dung lượng checkpoint quá nhỏ ({file_size_mb:.2f} MB), có thể bị lỗi"


def test_model_initialization():
    """Kiểm tra khởi tạo kiến trúc mô hình SOFTS tích hợp DINOv3 Backbone"""
    cfg = ModelConfigs()
    model = Model(cfg)
    assert model is not None, "Khởi tạo Model thất bại"
    assert hasattr(model, "encoder"), "Model thiếu thành phần encoder DINOv3"


def test_checkpoint_loading():
    """Kiểm tra nạp weights từ checkpoint vào kiến trúc nơ-ron"""
    cfg = ModelConfigs()
    model = Model(cfg)
    ckpt = torch.load(MODEL_PATH, map_location="cpu", weights_only=False)
    assert "state_dict" in ckpt, "Checkpoint thiếu key 'state_dict'"
    
    missing, unexpected = model.load_state_dict(ckpt["state_dict"], strict=False)
    assert len(missing) == 0, f"Có missing keys khi nạp checkpoint: {missing[:5]}"
    model.eval()


def test_model_forward_shape_and_values():
    """
    Kiểm thử suy luận mô hình (Forward Pass):
    - Input shape: (Batch=1, Seq_len=96, Features=7)
    - Output shape mong muốn: (Batch=1, Pred_len=24, Features=7)
    - Giá trị dự báo không được chứa NaN hoặc Inf
    """
    cfg = ModelConfigs()
    model = Model(cfg)
    ckpt = torch.load(MODEL_PATH, map_location="cpu", weights_only=False)
    model.load_state_dict(ckpt["state_dict"])
    model.eval()

    # Tạo batch giả lập 96 giờ với 7 đặc trưng khí tượng/ô nhiễm
    dummy_input = torch.randn(1, 96, 7, dtype=torch.float32)
    
    with torch.no_grad():
        output = model(dummy_input, None, None, None)

    assert output.shape == (1, 24, 7), f"Output shape không khớp: {output.shape} != (1, 24, 7)"
    assert not torch.isnan(output).any(), "Kết quả dự báo có chứa giá trị NaN!"
    assert not torch.isinf(output).any(), "Kết quả dự báo có chứa giá trị vô cực Inf!"
