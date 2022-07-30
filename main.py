"""실행파일

python: 3.8.13
- mediapipe: 0.8.10
- numpy: 1.22.3
- opencv: 4.5.5
- pillow: 9.0.1
- pyautogui: 0.9.53
- scipy: 1.7.3
"""

import cv2

from module.function import Process
from module.gui import App
from module.settings import load_cam_id

CAM_ID = load_cam_id()

cap = cv2.VideoCapture(CAM_ID)
process = Process(cap)

app = App(process.run)
app.wm_attributes("-topmost", 1)
app.mainloop()

cv2.destroyAllWindows()
cap.release()
