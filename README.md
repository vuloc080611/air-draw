# ✋🎨 AirDraw – Vẽ tranh trong không khí bằng cử chỉ tay

![Demo](demo.gif)

> **Không cần bút, không cần chuột – chỉ cần đưa tay lên và vẽ!**  
> Dự án sử dụng webcam và trí tuệ nhân tạo để biến bàn tay bạn thành cây cọ kỹ thuật số.

[![Stars](https://img.shields.io/github/stars/vuloc080611/air-draw?style=social)](https://github.com/vuloc080611/air-draw)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

---

## 🌟 Tính năng nổi bật

| Cử chỉ | Hành động |
|--------|-----------|
| ☝️ **Giơ ngón trỏ** | Vẽ tự do trên màn hình |
| 🖐️ **Xòe 5 ngón tay** (giữ 2 giây) | Xoá toàn bộ canvas |
| ✌️ **Ký hiệu peace (trỏ + giữa)** | Đổi màu vẽ (5 màu sặc sỡ) |
| ⌨️ **Phím tắt** | C: Xoá, +/-: Chỉnh nét, ESC: Thoát |

- 🖥️ Chạy trực tiếp trên webcam, phản hồi cực nhanh (realtime)
- 🎨 Hỗ trợ thay đổi màu sắc và độ dày nét vẽ ngay khi đang vẽ
- 💡 Giao diện thân thiện, hiển thị hướng dẫn trực tiếp trên màn hình
- 🧠 Nhận diện tay cực kỳ chính xác nhờ MediaPipe + OpenCV

---

## ⚙️ Yêu cầu

- Python 3.9 trở lên
- Webcam (tích hợp sẵn hoặc rời)
- Hệ điều hành: Windows, macOS, Linux

---

## 🚀 Cài đặt cực kỳ đơn giản

```bash
# Clone repository
git clone https://github.com/vuloc080611/air-draw.git
cd air-draw

# Cài đặt các gói cần thiết
pip install -r requirements.txt

# Chạy chương trình
python main.py
