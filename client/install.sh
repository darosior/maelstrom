#!/bin/bash

[[ "$VIRTUAL_ENV" == "" ]]; INVENV=$?
VENVDIR="./venv"

printf "\033[0;34m- Checking virtual environment.. (\"./venv\")\033[0m\n"
if [ $INVENV -eq 0 ];then
    if [ ! -d $VENVDIR ];then
	    printf "\033[0;34m- 	Creating virtual environment.. (\"./venv\")\033[0m\n"
        python3 -m venv venv
    fi
    printf "\033[0;34m- 	Activating virtual environment.. (\"./venv\")\033[0m\n"
	source "$VENVDIR/bin/activate"
fi


printf "\033[0;34m- Installing Cython (v0.28.2)\033[0m\n"
pip install -U Cython==0.28.2


printf "\033[0;34m- Checking dependencies\033[0m\n"
deactivate
python3 check_dependencies.py
source "$VENVDIR/bin/activate"


printf "\033[0;34m- Installing requirements\033[0m\n"
pip install -r requirements.txt


printf "\033[0;34m- Installing Kivy modules\033[0m\n"
if [ ! -d "./libs/garden/garden.zbarcam" ];then
    cd "./libs/garden/"
    printf "\033[0;32m- Building zbarcam (and OpenCV)\033[0m\n"
    git clone "https://github.com/darosior/garden.zbarcam"
    cd "garden.zbarcam/" && make opencv_build
fi
printf "\033[0;34mCleaning the openCV build directory to erase Python2 code\033[0m\n"
cd libs/garden/garden.zbarcam/opencv-2.4.13.6 && ls |grep -v build | xargs rm -rf && cd ../../../../
printf "\033[0;34m- Installing opencv-python\033[0m\n"
pip install -U opencv-python
