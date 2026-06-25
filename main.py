import cv2
import numpy as np
import time
from HandTrackingModule import HandDetector

# Cấu hình
WEBCAM_ID = 0
WINDOW_NAME = "AirDraw - Ve tranh trong khong khi"
CANVAS_ALPHA = 0.5  # Độ trong suốt khi blend canvas với camera

# Màu vẽ
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255), (255, 0, 255)]
color_index = 0
brush_color = colors[color_index]
brush_thickness = 4
eraser_thickness = 40  # kích thước cục tẩy khi xóa từng phần (không dùng trong chế độ đơn giản, ta dùng nút clear toàn bộ)

# Biến trạng thái
prev_x, prev_y = 0, 0
drawing = False
clear_cooldown = 0  # thời gian chờ giữa các lần clear

# Khởi tạo detector
detector = HandDetector(max_hands=1, detection_con=0.85, track_con=0.5)

# Mở webcam
cap = cv2.VideoCapture(WEBCAM_ID)
cap.set(3, 1280)
cap.set(4, 720)

# Canvas vẽ
canvas = None

while True:
    success, img = cap.read()
    if not success:
        break

    # Lật ảnh để giống gương
    img = cv2.flip(img, 1)

    # Khởi tạo canvas nếu chưa có
    if canvas is None:
        canvas = np.zeros_like(img)

    # Phát hiện bàn tay
    img = detector.find_hands(img, draw=True)
    lm_list, bbox = detector.find_position(img, draw=False)

    fingers = detector.fingers_up()

    # Xác định trạng thái cử chỉ
    # Chế độ vẽ: chỉ ngón trỏ giơ (index=1, các ngón còn lại=0)
    if len(fingers) == 5:
        if fingers[1] == 1 and sum(fingers[0:2]) == 1 and sum(fingers[2:]) == 0:
            # Ngón trỏ giơ
            if lm_list:
                x, y = lm_list[8][1], lm_list[8][2]  # đầu ngón trỏ
                if drawing and prev_x != 0 and prev_y != 0:
                    cv2.line(canvas, (prev_x, prev_y), (x, y), brush_color, brush_thickness)
                prev_x, prev_y = x, y
                drawing = True
            else:
                drawing = False
        else:
            drawing = False
            prev_x, prev_y = 0, 0

        # Clear toàn bộ canvas: mở cả bàn tay (tất cả ngón giơ)
        if all(f == 1 for f in fingers) and time.time() - clear_cooldown > 2:
            canvas = np.zeros_like(img)
            clear_cooldown = time.time()

        # Đổi màu: ký hiệu peace (ngón trỏ + ngón giữa giơ, các ngón khác co)
        if fingers[1] == 1 and fingers[2] == 1 and sum(fingers) == 2:
            color_index = (color_index + 1) % len(colors)
            brush_color = colors[color_index]
            # Thêm delay nhỏ tránh đổi màu liên tục
            time.sleep(0.2)

        # Chế độ cục tẩy cục bộ (xóa vùng tròn) - có thể thêm nếu muốn, nhưng tạm giữ đơn giản
        # Nếu nắm tay (tất cả co) thì chỉ dừng vẽ, không xóa
    else:
        drawing = False
        prev_x, prev_y = 0, 0

    # Blend canvas lên ảnh gốc
    img_gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, img_inv = cv2.threshold(img_gray, 50, 255, cv2.THRESH_BINARY_INV)
    img_inv = cv2.cvtColor(img_inv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, img_inv)
    img = cv2.bitwise_or(img, canvas)

    # Hiển thị hướng dẫn
    cv2.putText(img, "Index: Draw | Open Palm: Clear | Peace: Change Color", 
                (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(img, f"Color: {brush_color}", (20, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, brush_color, 2, cv2.LINE_AA)

    cv2.imshow(WINDOW_NAME, img)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC thoát
        break
    elif key == ord('c'):
        canvas = np.zeros_like(img)
    elif key == ord('+') or key == ord('='):
        brush_thickness = min(brush_thickness + 1, 20)
    elif key == ord('-'):
        brush_thickness = max(brush_thickness - 1, 1)

cap.release()
cv2.destroyAllWindows()
