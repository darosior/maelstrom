# C-simple

[![Pull Requests Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)
[![MIT license](https://img.shields.io/github/license/darosior/c-simple.svg)](https://github.com/darosior/c-simple/blob/master/LICENSE)

## :clipboard: Contents

- [Introduction](#introduction)
- [Server installation](#server-configuration)
- [Mobile client](#mobile-client-installation)
- [Licence](#licence)

## 🔍 Introduction

C-simple is an easy-to-use and secure mobile interface to C-lightning. It provides basic functionnalities of a wallet : pay, request payment, balance. A TLS mutual authentication is used to connect the client and the lightning node, the communication being thus encrypted end-to-end.
> ⚠️ C-simple is still in development and not yet even Beta released. It comes without any warranty
> or guarantee, please use it with care and preferably on testnet or with insignificant amounts.

## :wrench: Server configuration

TODO

## :hammer: Mobile client installation
  
```
git clone https://github.com/darosior/c-simple && cd c-simple/client
make [all|desktop|apk]
```
To run the desktop application, type `python3 main.py`. If a mobile phone is connected to the computer and in debug mode, the application will be installed and launched automatically when running `make apk`. In any case it will be built and available in the `bin/` repository.

## :syringe: Dependencies

### Server

- [pyopenssl](https://pypi.org/project/pyOpenSSL/)
- [RPyC](https://rpyc.readthedocs.io/en/latest/index.html)
- [pylightning](https://github.com/ElementsProject/lightning/tree/master/contrib/pylightning)

### Client

- [Kivy](https://kivy.org/doc/stable/installation/installation-linux.html#installation-in-a-virtual-environment)
- [RPyC](https://rpyc.readthedocs.io/en/latest/index.html)
- [ZBarCam](https://github.com/kivy-garden/garden.zbarcam)

## 📃 Licence

[MIT](LICENSE)
