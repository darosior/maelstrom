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
	$(PIP) install https://github.com/darosior/python-for-android/archive/03770626d7a7e8692b6bae442c5387086b2e3ec3.zip
	$(PIP) install buildozer
	export ANDROIDNDK=$$HOME/.buildozer/android/platform/android-ndk-r17c
	export ANDROIDSDK=$$HOME/.buildozer/android/platform/android-sdk
	. $(VENVDIR)/bin/activate && python3 -m buildozer android debug deploy run

clean:
	rm -rf venv __pycache__ libs/garden/garden.zbarcam
