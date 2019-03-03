SHELL=/bin/bash
all: desktop apk

remake: clean all
	
desktop:
	source install.sh

apk: desktop
	. venv/bin/activate
	pip install python-for-android
	pip install buildozer
	export ANDROIDNDK=$HOME/.buildozer/android/platform/android-ndk-r17c
	export ANDROIDSDK=$HOME/.buildozer/android/platform/android-sdk
	buildozer android debug deploy run

clean:
	rm -rf venv __pycache__ libs/garden/garden.zbarcam
