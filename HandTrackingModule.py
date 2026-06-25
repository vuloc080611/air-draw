import cv2
import mediapipe as mp
import math


class HandDetector:
    def __init__(self, mode=False, max_hands=1, detection_con=0.7, track_con=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.detection_con = detection_con
        self.track_con = track_con

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.max_hands,
            min_detection_confidence=self.detection_con,
            min_tracking_confidence=self.track_con
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.tip_ids = [4, 8, 12, 16, 20]  # đầu ngón: cái, trỏ, giữa, nhẫn, út

    def find_hands(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        if self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(
                        img, hand_lms, self.mp_hands.HAND_CONNECTIONS,
                        self.mp_draw.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2),
                        self.mp_draw.DrawingSpec(color=(0, 255, 0), thickness=2)
                    )
        return img

    def find_position(self, img, hand_no=0, draw=True):
        self.lm_list = []
        x_list, y_list = [], []
        bbox = []
        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[hand_no]
            for id, lm in enumerate(my_hand.landmark):
                h, w, _ = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lm_list.append([id, cx, cy])
                x_list.append(cx)
                y_list.append(cy)
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

            x_min, x_max = min(x_list), max(x_list)
            y_min, y_max = min(y_list), max(y_list)
            bbox = x_min, y_min, x_max, y_max
            if draw:
                cv2.rectangle(img, (x_min - 20, y_min - 20),
                              (x_max + 20, y_max + 20), (0, 255, 0), 2)
        return self.lm_list, bbox

    def fingers_up(self):
        fingers = []
        # Kiểm tra ngón cái (cần biết tay trái/phải)
        if self.lm_list:
            # Xác định hướng bàn tay từ wrist và middle mcp
            # Dùng classification label nếu có
            hand_label = ""
            if self.results.multi_handedness:
                hand_label = self.results.multi_handedness[0].classification[0].label

            # Ngón cái: dùng toạ độ x
            if hand_label == "Right":
                # Tay phải: ngón cái giơ khi tip.x < ip.x
                if self.lm_list[self.tip_ids[0]][1] < self.lm_list[self.tip_ids[0] - 1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            else:  # Left hoặc không rõ
                if self.lm_list[self.tip_ids[0]][1] > self.lm_list[self.tip_ids[0] - 1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            # 4 ngón còn lại: tip.y < pip.y (vì trục y hướng xuống)
            for id in range(1, 5):
                if self.lm_list[self.tip_ids[id]][2] < self.lm_list[self.tip_ids[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

        return fingers  # [thumb, index, middle, ring, pinky]
