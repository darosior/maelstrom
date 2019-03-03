#!/bin/bash

ROOTDIR=$(pwd)
[[ "$VIRTUAL_ENV" == "" ]]; INVENV=$?
VENVDIR="$ROOTDIR/venv"

printf "\033[0;34m- Checking virtual environment.. (\"./venv\")\033[0m\n"
if [ $INVENV -eq 0 ];then
    if [ ! -d $VENVDIR ];then
	    printf "\033[0;34m- 	Creating virtual environment.. (\"./venv\")\033[0m\n"
        python3 -m venv $VENVDIR
    fi
    printf "\033[0;34m- 	Activating virtual environment.. (\"./venv\")\033[0m\n"
	source "$VENVDIR/bin/activate"
fi

# Now that we are in the venv
MINOR_V=$(python -c 'import sys;print(sys.version_info[1])')

printf "\033[0;34m- Installing Cython (v0.28.2)\033[0m\n"
pip install -U Cython==0.28.2


printf "\033[0;34m- Checking dependencies\033[0m\n"
deactivate
python3 "$ROOTDIR/check_dependencies.py"
source "$VENVDIR/bin/activate"


printf "\033[0;34m- Installing requirements\033[0m\n"
pip install -r requirements.txt


printf "\033[0;34m- Installing Kivy modules\033[0m\n"
if [ ! -d "$ROOTDIR/libs/garden/garden.zbarcam" ];then
    cd "$ROOTDIR/libs/garden/"
    printf "\033[0;32m- Building zbarcam (and OpenCV)\033[0m\n"
    git clone "https://github.com/darosior/garden.zbarcam" && cd "garden.zbarcam/" && make opencv PYTHON_MINOR_VERSION=$MINOR_V
    cp $ROOTDIR/libs/garden/garden.zbarcam/opencv*/build/lib/cv2.so $VENVDIR/lib/python3.$MINOR_V/site-packages/
    cp $ROOTDIR/libs/garden/garden.zbarcam/opencv*/build/lib/python3/cv2*.so $VENVDIR/lib/python3.$MINOR_V/site-packages/
    cd $ROOTDIR
fi
printf "\033[0;34mCleaning the openCV directory\033[0m\n"
rm -rf $ROOTDIR/libs/garden/garden.zbarcam/opencv-*

printf "\033[0;34m- Installing opencv-python\033[0m\n"
pip install -U opencv-python
