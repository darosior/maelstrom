#!/bin/bash

[[ "$VIRTUAL_ENV" == "" ]]; INVENV=$?
VENVDIR="./venv/"

if [ ! $INVENV ];then
    if [ ! -d $VENVDIR ];then
        python3 -m venv venv
    else
	source $VENVDIR
    fi
fi

printf "\033[1;33m- Installing Cython (v0.28.2)\033[0m\n"
pip install -U Cython==0.28.2

printf "\033[1;33m- I will install the libzbar-dev and cmake packages, I need privileges...\033[0m\n"
su -c "apt update && apt install -y libzbar-dev cmake"

printf "\033[1;33m- I will install the Kivy dependencies and I need privileges once again...\033[0m\n"  
# Copy/pasted from Kivy doc
# Install necessary system packages
su -c "apt install -y python3-pip build-essential git python3 python3-dev ffmpeg libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev zlib1g-dev libgstreamer1.0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good"

printf "\033[1;33m- Installing requirements\033[0m\n"
pip install -r requirements.txt

printf "\033[1;33m- Installing Kivy modules\033[0m\n"
#cd "libs/garden/"
#printf "\033[1;33m- Building zbarcam (with OpenCV)\033[0m\n"
#git clone "https://github.com/darosior/garden.zbarcam"
#cd "garden.zbarcam/" && make opencv_build
printf "Installing opencv-python"
pip install -U opencv-python

