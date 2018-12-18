#!/bin/bash

[[ "$VIRTUAL_ENV" == "" ]]; INVENV=$?
VENVDIR="./venv/"

printf "\033[0;34m- Checking virtual environment.. (\"./venv\")\033[0m\n"
if [ ! $INVENV ];then
    if [ ! -d $VENVDIR ];then
	printf "\033[0;34m- 	Creating virtual environment.. (\"./venv\")\033[0m\n"
        python3 -m venv venv
    else
	printf "\033[0;34m- 	Activating virtual environment.. (\"./venv\")\033[0m\n"
	source $VENVDIR
    fi
fi

printf "\033[0;34m- Installing Cython (v0.28.2)\033[0m\n"
pip install -U Cython==0.28.2

printf "\033[0;34m- I will install the libzbar-dev, cmake, and Kivy dependencies packages, therefore I need privileges...\033[0m\n"
printf "\033[0;34mKivy dependencies package list : \033[1;33mpython3-pip build-essential git python3 python3-dev ffmpeg libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev zlib1g-dev libgstreamer1.0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good xclip xsel\033[0m\n"
su -c "apt update && apt install -y libzbar-dev cmake python3-pip build-essential git python3 python3-dev ffmpeg libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev zlib1g-dev libgstreamer1.0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good xclip xsel"

printf "\033[0;34m- Installing requirements\033[0m\n"
pip install -r requirements.txt

printf "\033[0;34m- Installing Kivy modules\033[0m\n"
if [ ! -d "./libs/garden/garden.zbarcam" ];then
    cd "./libs/garden/"
    printf "\033[0;32m- Building zbarcam (and OpenCV)\033[0m\n"
    git clone "https://github.com/darosior/garden.zbarcam"
    cd "garden.zbarcam/" && make opencv_build
fi
printf "\033[0;34mInstalling opencv-python\033[0m\n"
pip install -U opencv-python

