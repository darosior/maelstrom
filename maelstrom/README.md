We use [Kivy](https://github.com/kivy/)

Debian instructions, otherwise see [install
doc](https://kivy.org/doc/stable/installation/installation-linux.html)
```bash
apt install -y build-essential git ffmpeg libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev zlib1g-dev python3-venv
```

```bash
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```
