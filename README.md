# Assistive Mouse Control Through Face Detection: Enhancing Web Accessibility for Users with Limited Upper Limb Mobility

We propose a novel contactless computer interface to enhance web accessibility for individuals with limited upper limb mobility. Our system leverages **real-time face tracking** and **eye-blink detection** to enable hands-free mouse control through facial gestures, eliminating the need for a physical mouse. Designed for accessibility, it operates with high accuracy on standard laptops without requiring GPUs or specialized hardware.

## 🛠️ Installation and Usage

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

## 🎬 User Manual

<video src="https://private-user-images.githubusercontent.com/75429815/429830501-8b51e391-7c63-49dc-920b-28960477943e.mp4?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NDM3NDMzMDIsIm5iZiI6MTc0Mzc0MzAwMiwicGF0aCI6Ii83NTQyOTgxNS80Mjk4MzA1MDEtOGI1MWUzOTEtN2M2My00OWRjLTkyMGItMjg5NjA0Nzc5NDNlLm1wND9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNTA0MDQlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjUwNDA0VDA1MDMyMlomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTg4NmI1YTA0YzdmMWM0OTRmNDNiZmUzNDMxNTQ3NjVkZjU4YzNlZThjNjhjYjY5MjMwMzJlOThkZjkzOGYwMjYmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.FAjPGLGxEp_WzZwEgLI6jgcd_Noi56NsHWjAKPjqpcI" controls muted></video>

1. Set up the camera at eye level.
2. Move your head to move the cursor.
3. Click by closing your eyes briefly.
4. To zoom or scroll, click the button on the side and move the cursor over the window you want.
5. Use the pause button to keep the cursor still, useful when watching videos.

## 📄 Paper

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
