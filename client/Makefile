SHELL=/bin/bash
ROOTDIR=$(shell pwd)
VENVDIR=$(ROOTDIR)/venv
PIP=$(VENVDIR)/bin/pip
PYTHON=$(VENVDIR)/bin/python # python3

all: desktop apk

remake: clean all
	
desktop:
	. $(ROOTDIR)/install.sh

apk: desktop
	. $(VENVDIR)/bin/activate
	$(PIP) install https://github.com/kivy/python-for-android/archive/84142eb3dcb564b6e577a46304e11d2497af482a.zip
	$(PIP) install https://github.com/darosior/buildozer/archive/b835374910e8019667823b19e07ed3962cdba15d.zip
	export ANDROIDNDK=$$HOME/.buildozer/android/platform/android-ndk-r17c
	export ANDROIDSDK=$$HOME/.buildozer/android/platform/android-sdk
	. $(VENVDIR)/bin/activate && python3 -m buildozer android debug deploy run

clean:
	rm -rf .buildozer $$HOME/.buildozer $$HOME/.android venv __pycache__ libs/garden/garden.zbarcam
