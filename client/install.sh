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

echo "- Installing Cython (v0.28.2)"
pip install -U Cython==0.28.2

echo "- I will install the libzbar-dev package, I need privileges"
su -c "apt update && apt install -y libzbar-dev"

echo "- Installing requirements"
pip install -r requirements.txt
