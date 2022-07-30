# The Study on Alternative Input Method Using Real-Time Face Recognition

We propose an alternative input technique using real-time image recognition technology as a system that
can help users who have difficulty using input devices such as conventional mouse due to physical
discomfort. After detecting the landmark of the face using Face Mesh, eye opening ratio (EAR), the gaze
direction and angle of the face are calculated using solvePnP. We use pyautogui to manipulate the mouse
cursor according to the calculated information. In addition, various set values can be adjusted in consideration
of individual physical differences. This study includes features that help web surfing more conveniently,
especially screen zoom, and also solves the problem of eye fatigue, which has been suggested as a limitation
in existing systems. In addition, no high-performance CPU or GPU environment is required, and no separate
tracker devices or high-performance cameras are required.


## 실시간 얼굴 인식을 활용한 대체 입력 기법에 관한 연구


신체적 불편함으로 인해 기존의 마우스와 같은 입력 장치의 사용이 힘든 사용자에게 도
움이 될 수 있는 시스템으로 실시간 영상 인식 기술을 활용한 대체 입력 기법을 제안한다.
Face Mesh를 이용하여 얼굴의 랜드마크를 검출한 뒤, 프레임별 눈 뜨는 비율(EAR)과
solvePnP를 이용하여 얼굴의 주시 방향 및 각도를 계산한다. 계산한 정보에 따라 pyautogui
를 이용하여 마우스 커서를 조작한다. 또한 개인의 신체적 차이를 고려해 여러 설정값을
조정할 수 있도록 하였다. 본 연구는 특히 화면 확대/축소와 같이 웹 서핑을 보다 편리하게
돕는 기능이 포함되어 있으며, 기존의 시스템에서 한계점으로 제시되었던 눈 피로도에 대
한 문제도 해결하였다. 추가로 고성능 CPU나 GPU 환경이 요구되지 않고 별도의 트래커 장
치나 고성능 카메라 또한 필요하지 않다.


# Contributors

- [박성진 (Sung-jin Park)](https://github.com/Denev6)
- [신예은 (Ye-eun Shin)](https://github.com/Ye-eun-Shin)
- [이병준 (Byungjoon Lee)](https://github.com/powerpowe)
- Prof. 오하영 (Hayoung Oh)


# OPEN SOURCE LIBRARIES

Check `NOTICE` and `requirements.txt` for details.

