# C-simple

[![Pull Requests Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)
[![MIT license](https://img.shields.io/github/license/darosior/c-simple.svg)](https://github.com/darosior/c-simple/blob/master/LICENSE)

## :clipboard: Contents

- [Introduction](#introduction)
- [Getting started](#getting-started)
- [Doing more](#more)
- [Licence, donations, other](#licence)

## 🔍 Introduction
\
C-simple is a basic and easy-to-use ("c-simple" means phonetically "it's easy !" in french) mobile and desktop interface to the [C-lightning](https://github.com/ElementsProject/lightning) Lightning Network daemon. It uses an API hosted on top of the daemon and a mutual authentication with x509 certificates, to make a secure connection possible from a mobile application.\
You can find the API code (made with [RPyC](https://github.com/tomerfiliba/rpyc)) in the [c-simple/](https://github.com/darosior/c-simple/tree/master/c-simple) directory, and the application code (made with [Kivy](https://github.com/kivy/)) int [client/](https://github.com/darosior/c-simple/tree/master/client) directory. Both are entirely written in Python.  
  
## :walking: Getting started
  
C-simple is composed of two parts : an access point running on-top-of your node, and an application (a mobile one, most of the time). In order to initiate the connection between these two parts, the certificate (equivalent of a public key) of each side is uploaded to [Pixeldrain](https://pixeldrain.com/). At the first start you will have to enter a code on the computer running the node, then another on the phone so that each device can download each other certificate from Pixeldrain. Here is now how to install each part :  
  
### :computer: Node side
#### First method : with pip
Dependencies : `python3`, `python3-venv`.  
```shell
python3 -m venv venv && . venv/bin/activate
python3 -m c-simple -i 0.0.0.0
```
#### Second method : from source
Dependencies : `python3`, `python3-venv`.  
```shell
git clone https://github.com/darosior/c-simple && cd c-simple/c-simple/
python3 -m venv venv && . venv/bin/activate
pip install -r requirements
python3 c-simple.py -i 0.0.0.0
```
  
### :iphone: Client side
#### First method : from apk
  
#### Second method : build with Docker
You can build the apk yourself, but please note that it will take some time (and even more with Docker).
```shell
mkdir apk_dir
docker run --name c-simple-client --rm -v $PWD/apk_dir/:/opt/c-simple/client/bin darosior/c-simple-client:0.0.1 /bin/bash -c 'cd /opt/c-simple/client && make apk'
```
You will find the apk in `apk_dir/`.  
#### Third method : build from source
The installation script will take care of dependencies if you are running a Debian OS (or a similar one) using the `apt` module. Only `python3-apt` is required under this conditions. If you are not running a Debian OS here is a list of dependencies : `'libzbar-dev', 'cmake', 'python3-pip', 'build-essential', 'git', 'python3', 'python3-dev', 'ffmpeg', 'libsdl2-dev', 'libsdl2-image-dev', 'libsdl2-mixer-dev', 'libsdl2-ttf-dev', 'libportmidi-dev', 'libswscale-dev', 'libavformat-dev', 'libavcodec-dev', 'zlib1g-dev', 'libgstreamer1.0-0', 'gstreamer1.0-plugins-base', 'gstreamer1.0-plugins-good', 'xclip', 'xsel'`.  
```shell
git clone https://github.com/darosior/c-simple && cd c-simple/client
make [all|apk|desktop]
```
  
  
## :running: More
The `-i 0.0.0.0` option is to listen on all interfaces.  
You can specify a directory to store the certificates on the node with 
```shell
python3 -m csimple -i 0.0.0.0 --certdir /path/to/the/certdir
```
You can generate new certificates (you will need to reconnect the phone after that)
```shell
python3 -m csimple -i 0.0.0.0 --new-certs
```
If you don't use the lightning home default directory, specify it with
```shell
python3 -m csimple -i 0.0.0.0 --lightning-dir /path/to/lightning
```
More to come..
  
  
## 📃 Licence, donations
  
[MIT](LICENSE)  
[1Lgswwuq7gzfVtjbs5EKg1YZvistSV3Z6Q](bitcoin:1Lgswwuq7gzfVtjbs5EKg1YZvistSV3Z6Q)\
If you are looking for a Lightning Network node to connect to : [02a447fd201226f0bf6421c356f9d2117b0fb05ccc0858dd2b20589b9edb488f67@82.245.113.89:9735](https://1ml.com/node/02a447fd201226f0bf6421c356f9d2117b0fb05ccc0858dd2b20589b9edb488f67)
