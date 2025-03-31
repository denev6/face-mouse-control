import os
from tkinter import Tk, Toplevel, Scale, IntVar, Button, Label, messagebox
from tkinter.font import Font
from PIL import ImageTk, Image

import numpy as np
import cv2

try:
    from function import Detector
    from constant import CAM_ID, SETTING_FILE, DEFAULT_SETTINGS
except ImportError:
    from module.function import Detector
    from module.constant import CAM_ID, SETTING_FILE, DEFAULT_SETTINGS

_DIR = os.path.dirname(os.path.realpath(__file__))


def load_cam_id():
    """사용 가능한 카메라 정보를 가져온다.

    Returns:
        int: 카메라 정보
    """
    if isinstance(CAM_ID, int):
        return CAM_ID
    return cv2.CAP_ANY


class SettingError(Exception):
    def __init__(self, detail):
        self._detail = detail

    def __str__(self):
        return str(self._detail)


class EARSetter(object):
    """직접 눈의 EAR을 측정해 임계값 설정.

    Function: execute
    """

    def __init__(self):
        self._min_frame = 160
        self._frame_ignore = 10
        self.__frame_counter = 0
        self.__cap = None
        self.__detector = None

    def execute(self, device_id):
        """직접 눈의 EAR을 측정해 임계값을 설정하는 과정을 실행한다.

        Args:
            device_id: 사용할 카메라 정보.

        Returns:
            float: EAR 임계값.
        """
        self.__cap = cv2.VideoCapture(device_id)
        if self.__cap.isOpened():
            sucess, frame = self.__cap.read()
            if sucess:
                self.__detector = Detector(frame)
                threshold = self.__get_ear_threshold()

        cv2.destroyAllWindows()
        self.__cap.release()
        return threshold

    def __get_ear_threshold(self):
        ear_generator = (self.__get_ear_realtime(guide) for guide in ["open", "close"])
        filtered_ears = (self._drop_outliers(data) for data in ear_generator)
        threshold = self._get_ear_threshold(filtered_ears)
        return threshold

    def __get_ear_realtime(self, state):
        ear_list = list()
        while self.__cap.isOpened():
            sucess, frame = self.__cap.read()
            if sucess:
                frame, rgb_frame = self.__detector.convert_frame(frame)
                if self.__frame_counter < self._frame_ignore:
                    cv2.imshow("Detecting", frame)
                    cv2.moveWindow("Detecting", 100, 100)
                    self._show_guideline(
                        f"{state}-{self._frame_ignore - self.__frame_counter}"
                    )
                    cv2.waitKey(1000)
                    self.__frame_counter += 1
                else:
                    is_detected = self.__detector.detect_landmark(rgb_frame)
                    if is_detected:
                        cv2.imshow("Detecting", frame)
                        self._show_guideline(f"{state}-0")
                        cv2.waitKey(1)
                        ear = self.__detector.get_both_eyes_ear()
                        ear_list.append(ear)
                        if self.__frame_counter >= self._min_frame:
                            self.__frame_counter = 0
                            break
                        self.__frame_counter += 1
        return ear_list

    def _show_guideline(self, img_name):
        img = os.path.join(_DIR, "src", "ear", f"{img_name}.png")
        cv2.imshow("Guide", cv2.imread(img))
        cv2.moveWindow("Guide", 400, 400)
        cv2.setWindowProperty("Guide", cv2.WND_PROP_TOPMOST, 1)

    def _drop_outliers(self, data):
        data = np.array(data, dtype=np.float64)
        q3, q1 = np.percentile(data, [75, 25])
        iqr = q3 - q1

        def _not_outlier(x):
            return (q3 + 1.5 * iqr > x) and (x > q1 - 1.5 * iqr)

        normal_value = [value for value in data if _not_outlier(value)]
        if len(normal_value) < self._min_frame * 0.6:
            raise SettingError("Too many abnormal EAR values are included.")
        return normal_value

    def _get_ear_threshold(self, ears):
        single_ear_1, single_ear_2 = [np.mean(data) for data in ears]
        if single_ear_1 < single_ear_2:
            closed = single_ear_1
            opened = single_ear_2
        else:
            closed = single_ear_2
            opened = single_ear_1
        threshold = closed * 0.4 + opened * 0.6
        return np.round(threshold, 2)


class CustomSettingPage(Tk):
    """사용 설정 페이지.

    Example:
    >>> app = CustomSettingPage()
    >>> app.mainloop()
    """

    def __init__(self):
        Tk.__init__(self)
        Tk.title(self, "Settings")
        # Tk.resizable(self, 0, 0)
        Tk.configure(self, bg="white")

        self._SETTING_FILE = os.path.join(_DIR, SETTING_FILE)
        self._DEFAULT = DEFAULT_SETTINGS

        settings = self._get_current_setting()
        self.__blink = IntVar(value=int(settings[0]))
        self.__ear = IntVar(value=int(settings[1] * 100))
        self.__looking_up = IntVar(value=int(settings[2]))
        self.__looking_left = IntVar(value=-int(settings[3]))
        self.__looking_down = IntVar(value=-int(settings[4]))
        self.__looking_right = IntVar(value=int(settings[5]))
        self.__cursor_sensitivity = IntVar(value=int(settings[6]))
        self.__scroll_sensitivity = IntVar(value=int(settings[7] / 100))
        scale_style = {
            "orient": "horizontal",
            "background": "white",
            "foreground": "black",
            "highlightthickness": 0,
            "showvalue": False,
            "length": 900,
            "font": Font(size=12, weight="bold"),
        }
        scale_pack = {"side": "top", "pady": 13}
        Scale(
            self,
            label="Blink Frame Threshold: 값이 클수록 오래 감고 있어야 클릭됩니다.",
            variable=self.__blink,
            tickinterval=3,
            from_=3,
            to=15,
            **scale_style,
        ).pack(**scale_pack)
        self.__scale_ear = Scale(
            self,
            label="Eye Aspect Ratio Threshold (*100): 아래 `EAR 자동 설정`을 사용할 수 있습니다.",
            variable=self.__ear,
            tickinterval=5,
            from_=5,
            to=40,
            **scale_style,
        )
        self.__scale_ear.pack(**scale_pack)
        Scale(
            self,
            label="Looking Up Threshold: 값이 클수록 고개를 많이 들어야 마우스가 이동합니다.",
            variable=self.__looking_up,
            tickinterval=4,
            from_=2,
            to=20,
            **scale_style,
        ).pack(**scale_pack)
        Scale(
            self,
            label="Looking Left Threshold: 값이 클수록 고개를 왼쪽으로 많이 돌려야 마우스가 이동합니다.",
            variable=self.__looking_left,
            tickinterval=4,
            from_=2,
            to=20,
            **scale_style,
        ).pack(**scale_pack)
        Scale(
            self,
            label="Looking Down Threshold: 값이 클수록 고개를 많이 숙여야 마우스가 이동합니다.",
            variable=self.__looking_down,
            tickinterval=4,
            from_=2,
            to=20,
            **scale_style,
        ).pack(**scale_pack)
        Scale(
            self,
            label="Looking Right Threshold: 값이 클수록 고개를 오른쪽으로 많이 돌려야 마우스가 이동합니다.",
            variable=self.__looking_right,
            tickinterval=4,
            from_=2,
            to=20,
            **scale_style,
        ).pack(**scale_pack)
        Scale(
            self,
            label="Cursor Sensitivity: 값이 클수록 마우스가 많이 이동합니다.",
            variable=self.__cursor_sensitivity,
            tickinterval=5,
            from_=5,
            to=40,
            **scale_style,
        ).pack(**scale_pack)
        Scale(
            self,
            label="Scroll Sensitivity: 값이 클수록 스크롤 시 화면이 많이 이동합니다.",
            variable=self.__scroll_sensitivity,
            tickinterval=1,
            from_=2,
            to=10,
            **scale_style,
        ).pack(**scale_pack)
        Button(self, text="EAR 자동 설정", command=self._set_customed_ear).pack(
            side="left", ipadx=12, ipady=10, padx=50, pady=13
        )
        Button(self, text="설명서 보기", command=self._open_info_page).pack(
            side="left", ipadx=12, ipady=10, padx=50, pady=13
        )
        Button(self, text="저장하기", command=self._save_settings).pack(
            side="left", ipadx=12, ipady=10, padx=50, pady=13
        )

        # Resize window to fit the contents
        self.update_idletasks()
        width = self.winfo_reqwidth()
        height = self.winfo_reqheight()
        self.geometry(f"{width+8}x{height+8}+60+30")

    def _set_customed_ear(self):
        CAM_ID = load_cam_id()
        setter = EARSetter()
        threshold = setter.execute(CAM_ID)
        self.__scale_ear.set(int(threshold * 100))
        messagebox.showinfo(
            "Settings", f"EAR 값이 {int(threshold * 100)}로 설정되었습니다."
        )

    def _get_current_setting(self):
        if os.path.exists(self._SETTING_FILE):
            settings = np.load(self._SETTING_FILE)
        else:
            settings = self._DEFAULT
        return settings

    def _save_settings(self):
        variables = (
            self.__blink,
            self.__ear,
            self.__looking_up,
            self.__looking_left,
            self.__looking_down,
            self.__looking_right,
            self.__cursor_sensitivity,
            self.__scroll_sensitivity,
        )
        settings = [var.get() for var in variables]
        settings[1] = settings[1] / 100  # EAR Threshold
        settings[3] = -settings[3]  # Left Threshold
        settings[4] = -settings[4]  # Down Threshold
        settings[7] = settings[7] * 100  # Scroll Sensitivity
        self._check_data_requirements(settings)
        np.save(self._SETTING_FILE, np.array(settings, dtype=np.float64))
        messagebox.showinfo("Settings", "설정이 정상적으로 완료되었습니다.")

    def _check_data_requirements(self, values):
        data_size = len(values)
        if data_size != len(self._DEFAULT):
            raise SettingError(
                f"Setting requires {len(self._DEFAULT)} values. ({data_size} given)"
            )

        is_type_correct = all((isinstance(value, (int, float)) for value in values))
        if not is_type_correct:
            raise SettingError("Setting values should be 'int' or 'float.")

    def _open_info_page(self):
        self.__info_page = InformationPage(self)
        self.__info_page.grab_set()


class InformationPage(Toplevel):
    """사용 설명서 페이지."""

    def __init__(self, master):
        super().__init__(master)
        self._frame = None
        self.title("Information")
        self.geometry("1000x649+300+100")
        self.resizable(0, 0)
        self.configure(bg="white")
        self.__info = self._img("instruction.png")
        Label(self, image=self.__info, bd=0).pack()

    def _img(self, *paths):
        path = os.path.join(_DIR, "src", "gui", *paths)
        return ImageTk.PhotoImage(Image.open(path))


if __name__ == "__main__":
    setting = CustomSettingPage()
    setting.mainloop()
