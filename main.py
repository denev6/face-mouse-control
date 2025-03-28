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
