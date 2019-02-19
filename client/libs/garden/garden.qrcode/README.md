Module QRCode
=============

<img src="https://github.com/kivy-garden/garden.qrcode/blob/master/screenshot.png" align="right" width="256" />

A QRCode Widget.

Requirements:

    pip install qrcode

Usage::

 Python::

    from kivy.garden.qrcode import QRCodeWidget
    parent.add_widget(QRCodeWidget(data="Kivy Rocks"))

 kv::

    #:import QRCodeWidget kivy.garden.qrcode

    BoxLayout:
        orientation: 'vertical'
        Button:
            text: 'press to change qrcode'
            on_release: qr.data = "Kivy Rocks!"
        QRCodeWidget:
            id: qr
            data: 'Hello World'
