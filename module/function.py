import os
import platform
from time import time

import cv2
import mediapipe as mp
import numpy as np
import pyautogui

try:
    from constant import SETTING_FILE, DEFAULT_SETTINGS
except ImportError:
    from module.constant import SETTING_FILE, DEFAULT_SETTINGS

_DIR = os.path.dirname(os.path.realpath(__file__))
_SETTING_FILE = os.path.join(_DIR, SETTING_FILE)
# pyautogui.FAILSAFE = False
# pyautogui.PAUSE = 0.03

if os.path.exists(_SETTING_FILE):
    SETTINGS = np.load(_SETTING_FILE)
else:
    SETTINGS = DEFAULT_SETTINGS
(
    BLINK_FRAME_THRESHOLD,
    EAR_THRESHOLD,
    UP_THRESHOLD,
    LEFT_THRESHOLD,
    DOWN_THRESHOLD,
    RIGHT_THRESHOLD,
    CURSOR_SENSITIVITY,
    SCROLL_SENSITIVITY,
) = SETTINGS


class Detector(object):
    """얼굴 방향 인식 및 눈 깜빡임 인식을 수행

    Detecting Model:
        mediapipe - Face Mesh

    Functions:
        convert_frame
        detect_landmark
        get_face_direction
        update_blink_count
        get_both_eyes_ear
    """

    def __init__(self, frame):
        self._face_indexs = (1, 33, 61, 199, 263, 291)
        self._eye_indexs = (
            ((160, 144), (158, 153), (33, 133)),
            ((385, 380), (387, 373), (362, 263)),
        )
        w, h = self._set_frame_size(frame)
        self._w = w
        self._h = h
        self._cam_matrix = self._init_camera_matrix(w, h)
        self._dist_matrix = self._init_distortion_matrix()
        self._face_mesh = self._init_face_mesh()
        self._blink_frame_thre = int(BLINK_FRAME_THRESHOLD)
        self._ear_thre = EAR_THRESHOLD
        self._up_thre = int(UP_THRESHOLD)
        self._left_thre = int(LEFT_THRESHOLD)
        self._down_thre = int(DOWN_THRESHOLD)
        self._right_thre = int(RIGHT_THRESHOLD)
        self.__prev_y_angle = 0
        self.__prev_x_angle = 0
        self.__landmarks = None
        self.__blink_counter = 0

    def _set_frame_size(self, image):
        expected_w = 480
        img_h, img_w, _ = image.shape

        if img_w <= expected_w:
            return img_w, img_h
        else:
            img_h = int(expected_w * img_h / img_w)
            return expected_w, img_h

    def _init_camera_matrix(self, img_w, img_h):
        return np.array(
            [
                [img_w, 0, img_h / 2],
                [0, img_w, img_h / 2],
                [0, 0, 1],
            ],
            dtype=np.int32,
        )

    def _init_distortion_matrix(self):
        return np.zeros((4, 1), dtype=np.float64)

    def _init_face_mesh(self):
        return mp.solutions.face_mesh.FaceMesh(
            refine_landmarks=True,
            static_image_mode=False,
            max_num_faces=1,
        )

    def _rescale_x(self, x):
        return int(x * self._w)

    def _rescale_y(self, y):
        return int(y * self._h)

    def convert_frame(self, frame):
        """입력된 프레임(이미지)의 전처리를 수행한다.

        Args:
            frame (image, ndarray): 얼굴 탐지에 사용할 이미지.

        Returns:
            ndarray: 원본 이미지에서 좌우반전, 크기 조정을 수행한 이미지.
            ndarray: 얼굴 탐지에 사용할 수 있는 이미지.
        """
        bgr_frame = cv2.flip(cv2.resize(frame, (self._w, self._h)), 1)
        rgb_frame = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB)
        rgb_frame.flags.writeable = False
        return bgr_frame, rgb_frame

    def detect_landmark(self, frame):
        """mediapipe Face Mesh를 활용해 랜드마크를 탐지한다.

        Args:
            frame (image, ndarray): RGB 상태의 이미지.

        Returns:
            bool: 랜드마크 탐지 성공 여부.
        """
        results = self._face_mesh.process(frame)
        landmarks = results.multi_face_landmarks
        if landmarks:
            self.__landmarks = landmarks[0].landmark
        return bool(landmarks)

    def get_face_direction(self):
        """얼굴 방향을 계산해 방향 정보를 리스트로 반환한다.

        Returns:
            list: 방향 정보가 담긴 리스트.

            리스트에 담긴 요소의 의미는 다음과 같다.
            *Controller._cursor_의 인덱스와 동일하다.

            - 0: 위 (Up)
            - 1: 아래 (Down)
            - 2: 왼쪽 (Left)
            - 3: 오른쪽 (Right)
        """
        x_angle, y_angle, z_angle = self._get_face_angles()
        directions = []
        if self._is_up(x_angle) and self._moved_vertically(x_angle):
            directions.append(0)
        elif self._is_down(x_angle) and self._moved_vertically(x_angle):
            directions.append(1)
        if self._is_left(y_angle) and self._moved_horizontally(y_angle):
            directions.append(2)
        elif self._is_right(y_angle) and self._moved_horizontally(y_angle):
            directions.append(3)

        self.__prev_x_angle = x_angle
        self.__prev_y_angle = y_angle

        return directions

    def _moved_vertically(self, x):
        if int(x) ^ int(self.__prev_x_angle) <= 0:
            return True
        else:
            return abs(x) >= abs(self.__prev_x_angle) - 3

    def _moved_horizontally(self, y):
        if int(y) ^ int(self.__prev_y_angle) <= 0:
            return True
        else:
            return abs(y) >= abs(self.__prev_y_angle) - 3

    def _is_up(self, x):
        return x > self._up_thre

    def _is_down(self, x):
        return x < self._down_thre

    def _is_left(self, y):
        return y < self._left_thre

    def _is_right(self, y):
        return y > self._right_thre

    def _get_face_angles(self):
        object_points = np.array(
            [self._get_face_points(id) for id in self._face_indexs], dtype=np.float64
        )
        image_points = np.array(object_points[:, :2], dtype=np.float64)

        _, rotation_vector, _ = cv2.solvePnP(
            object_points, image_points, self._cam_matrix, self._dist_matrix
        )
        rotation_matrix, _ = cv2.Rodrigues(rotation_vector)
        angles, *_ = cv2.RQDecomp3x3(rotation_matrix)
        angles = [angle * 360 for angle in angles]
        return angles

    def _get_face_points(self, id):
        landmark = self.__landmarks[id]
        return [self._rescale_x(landmark.x), self._rescale_y(landmark.y), landmark.z]

    def update_blink_count(self):
        """눈 깜빡임을 탐지해 눈 깜빡임 정보를 업데이트한다.

        Returns:
            bool: 임계값(프레임) 이상의 눈 깜빡임 여부.
        """
        ear = self.get_both_eyes_ear()
        if ear <= self._ear_thre:
            if self.__blink_counter >= self._blink_frame_thre:
                self.__blink_counter = 0
                return True
            self.__blink_counter += 1
        else:
            self.__blink_counter = 0
        return False

    def get_both_eyes_ear(self):
        """양쪽 눈의 EAR(Eye Aspect Ratio)을 반환한다.

        Returns:
            float: 양쪽 눈의 EAR 평균.
        """
        ears = [
            self._get_single_eye_ear(single_eye_ids)
            for single_eye_ids in self._eye_indexs
        ]
        mean_ear = np.mean(ears)
        return mean_ear

    def _get_single_eye_ear(self, eye_landmark_ids):
        ear_ys = [self._get_y_dist(ids) for ids in eye_landmark_ids[:2]]
        ear_x = self._get_x_dist(eye_landmark_ids[2])
        ear = np.sum(ear_ys) / (2 * ear_x)
        return ear

    def _get_x_dist(self, landmark_ids):
        landmarks = [self._rescale_x(self.__landmarks[id].x) for id in landmark_ids]
        return abs(landmarks[0] - landmarks[1])

    def _get_y_dist(self, landmark_ids):
        landmarks = [self._rescale_y(self.__landmarks[id].y) for id in landmark_ids]
        return abs(landmarks[0] - landmarks[1])


class Controller(object):
    """입력장치를 활용한 동작 수행.

    Functions:
        move_cursor_by_face
        click
        add_command
        count_btn_command
        has_command
    """

    def __init__(self):
        self.__cursor_ = (
            self._cursor_up,
            self._cursor_down,
            self._cursor_left,
            self._cursor_right,
        )
        self.__btn_command_ = {
            "zoom-in": self._zoom_in,
            "zoom-out": self._zoom_out,
            "scroll-up": self._scroll_up,
            "scroll-down": self._scroll_down,
        }
        self._dist = int(CURSOR_SENSITIVITY)
        self._scroll_height = int(SCROLL_SENSITIVITY)
        self._ctrl_key = "ctrl"

        if platform.system() == "Darwin":  # for MacOS
            self._scroll_height = int(SCROLL_SENSITIVITY / 50)
            self._ctrl_key = "command"

        self.__command = None
        self.__command_counter = 0

    def _cursor_up(self, x, y):
        return x, y - self._dist

    def _cursor_down(self, x, y):
        return x, y + self._dist

    def _cursor_left(self, x, y):
        return x - self._dist, y

    def _cursor_right(self, x, y):
        return x + self._dist, y

    def move_cursor_by_face(self, directions):
        """방향 정보를 받아 마우스 커서를 이동한다.

        Args:
            directions: 방향 정보가 담긴 리스트.
        """
        cursor = pyautogui.position()
        for direction in directions:
            cursor = self.__cursor_[direction](*cursor)
        pyautogui.moveTo(*cursor)

    def click(self):
        """마우스 커서에서 클릭을 수행한다."""
        pyautogui.click()

    def _with_focus(function):
        def focus(self):
            pyautogui.doubleClick()
            function(self)

        return focus

    @_with_focus
    def _zoom_in(self):
        pyautogui.hotkey(self._ctrl_key, "+")

    @_with_focus
    def _zoom_out(self):
        pyautogui.hotkey(self._ctrl_key, "-")

    @_with_focus
    def _scroll_up(self):
        pyautogui.scroll(self._scroll_height)

    @_with_focus
    def _scroll_down(self):
        pyautogui.scroll(-self._scroll_height)

    def add_command(self, command):
        """객체의 __command 값을 추가한다.

        Args:
            command (str): 객체에서 수행한 명령 정보.
            *Controller.__btn_command_ 참고.
        """
        self.__command = self.__btn_command_[command]

    def count_btn_command(self):
        """객체의 __command가 특정 프레임 후에 실행될 수 있도록 카운트한다."""
        if self.__command_counter > 30:
            self.__command()
            self.__command = None
            self.__command_counter = 0
        else:
            self.__command_counter += 1

    def has_command(self):
        """객체의 __command 값 존재 여부를 반환한다.

        Returns:
            bool: 객체의 __command 값 존재 여부.
        """
        return self.__command is not None


class Process(object):
    """프로그램의 실행 객체

    Function: run
    """

    def __init__(self, capture):
        self._cap = capture
        self._max_frame_rate = 60
        self.__controller = Controller()
        self.__detector = None
        self.__prev_time = 0
        self.__prev_allow_showing_frame = False
        self.__is_cv_inited = False

    def run(self, command, allow_showing_frame, allow_detecting_direction):
        """프로그램을 수행한다.

        Args:
            command (str): tkinter 버튼으로부터 입력된 명령 정보.
            allow_showing_frame (bool): 화면에 실시간 프레임을 보여줄 지 여부.
            allow_detecting_direction (bool): 얼굴 방향 계산 수행 여부.
        """
        success, frame = self._cap.read()
        current_time = time() - self.__prev_time

        if not success or (current_time < 1 / self._max_frame_rate):
            # Limit the frame rate to prevent overhead
            # when it exceeds the maximum.
            return

        self.__prev_time = time()
        if self.__detector is None:
            self.__detector = Detector(frame)

        frame, rgb_frame = self.__detector.convert_frame(frame)
        is_detected = self.__detector.detect_landmark(rgb_frame)

        if command:
            self.__controller.add_command(command)

        if is_detected:
            if allow_detecting_direction:
                directions = self.__detector.get_face_direction()
                if directions:
                    self.__controller.move_cursor_by_face(directions)

            is_blinked = self.__detector.update_blink_count()
            if is_blinked:
                self.__controller.click()

            if self.__controller.has_command():
                self.__controller.count_btn_command()

        if allow_showing_frame:
            cv2.imshow("Frame", frame)
            cv2.setWindowProperty("Frame", cv2.WND_PROP_TOPMOST, 1)
            if not self.__prev_allow_showing_frame or not self.__is_cv_inited:
                # (Handling transition from pause) or (Initial position)
                self._move_frame_window()
                self.__is_cv_inited = True
        self.__prev_allow_showing_frame = allow_showing_frame

    def _move_frame_window(self):
        full_w, full_h = pyautogui.size()
        x = full_w - self.__detector._w - 10
        y = full_h - self.__detector._h - 10
        cv2.moveWindow("Frame", x, y)
