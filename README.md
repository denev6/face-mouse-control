# Contactless Computer Interface based on Face Recognition and Eye-blink Detection

We propose a novel contactless input method to enhance web accessibility for people with disabilities. Our system uses **real-time face tracking** and **eye blink detection** to control mouse movements through facial gestures, eliminating the need for traditional input devices. The system achieves high accuracy on basic laptops without requiring GPUs or specialized equipment.

## Installation and Usage

Python 3.10+ is required. **Python 3.12** provides the most stable experience on Windows, with macOS also supported.

```sh
git clone https://github.com/denev6/face-mouse-control.git
pip install -r requirements.txt
python main.py
```

You can customize settings using the GUI provided by `settings.py`.

```sh
python settings.py
```

## User Manual

1. Set up the camera at eye level.
2. Move your head to move the cursor.
3. Click by closing your eyes briefly.
4. To zoom or scroll, click the button on the side and move the cursor over the window you want.
5. Use the pause button to keep the cursor still, useful when watching videos.

## Paper

얼굴 인식과 Pyautogui 마우스 제어 기반의 비접촉식 입력 기법: [한국정보통신학회](https://koreascience.or.kr/article/JAKO202228049092231.page?&lang=ko)

```bibtex
@article{10.6109/JKIICE.2022.26.9.1279,
  author    = {Park Sung-jin and Shin Ye-eun and Lee Byung-joon and Oh Ha-young},
  title     = {Non-contact Input Method based on Face Recognition and Pyautogui Mouse Control},
  journal   = {Journal of the Korea Institute of Information and Communication Engineering},
  publisher = {한국정보통신학회},
  volume    = {26},
  number    = {9},
  pages     = {1279-1292},
  year      = 2022,
  month     = 09
}
```

### Authors

- 박성진 (Sung-jin Park): [github](https://github.com/denev6)
- 신예은 (Ye-eun Shin): [github](https://github.com/Ye-eun-Shin)
- 이병준 (Byung-joon Lee): [github](https://github.com/powerpowe)
- Prof. 오하영 (Ha-young Oh)
