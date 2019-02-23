# C-simple

[![Pull Requests Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)
[![MIT license](https://img.shields.io/github/license/darosior/c-simple.svg)](https://github.com/darosior/c-simple/blob/master/LICENSE)

## :clipboard: Contents

- [Introduction](#introduction)
- [Server installation](#server-configuration)
- [Mobile client](#mobile-client-installation)
- [Licence](#licence)

## 🔍 Introduction

C-simple is an easy-to-use and secure mobile interface to C-lightning. It provides basic functionnalities of a wallet : pay, request payment, balance. A two-way certificate authentication is used to connect the client and the lightning node, the communication is encrypted end-to-end.
> ⚠️ C-simple is still in development and not yet even Beta released. It comes without any warranty
> or guarantee, please use it with care and preferably on testnet or with insignificant amounts.

## :wrench: Server configuration

TODO

## :hammer: Mobile client installation
  
On Debian stretch :
```
git clone https://github.com/darosior/c-simple && cd c-simple/client
python3 -m venv venv && source venv/bin/activate # Not necessary, done in the script
. install.sh
```
Will install C-simple, you will be able to launch it with :
```
python3 main.py
```
To build the apk, just run :
```
pip install buildozer
buildozer android debug [deploy] [run]
```
If an error is raised about the android sdk/ndk not being found :
```
export ANDROIDSDK=$HOME/.buildozer/android/platform/android-sdk # Or the appropriate path
export ANDROIDNDK=$HOME/.buildozer/android/platform/android-ndk-r17c # Or the appropriate path 
```

## :syringe: Dependencies

### Server

- [pyopenssl](https://pypi.org/project/pyOpenSSL/)
- [argparse](https://pypi.org/project/argparse/)
- [RPyC](https://rpyc.readthedocs.io/en/latest/index.html)
- [pylightning](https://github.com/ElementsProject/lightning/tree/master/contrib/pylightning)

### Client

- [Kivy](https://kivy.org/doc/stable/installation/installation-linux.html#installation-in-a-virtual-environment)
- [RPyC](https://rpyc.readthedocs.io/en/latest/index.html)

## 📃 Licence

[MIT](LICENSE)
