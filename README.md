# QmlPy

## What

Introduce QML-like declarative structure to Python world. Developer writes only
**pure Python code** for QML.

## Naming convention

QmlPy depends on QtPy, I'd like to use the same naming style.

QmlPy is available across PyQt5, PyQt6, PySide2 and PySide6.

## Install

It's not ready to be published to PyPI. Currently you can install it via github
repo:

```
pip install git+https://github.com/likianta/qmlpy
```

## What it be like

For qmlpy:

```python
from qmlpy import Application
from qmlpy.qtquick import Window, Rectangle, Text
from qmlpy.qtquick.controls import Button
from lambda_ex import xlambda


def main():
    with Application() as app:

        with Window() as win:
            win.title = 'QmlPy Demo App'
            win.width = 800
            win.height = 600

            with Rectangle() as rct:
                rct.anchors.fill = win
                rct.anchors.margins = 24
                rct.color = 'navyblue'

                with Text() as txt:
                    txt.anchors.center_in = rct
                    txt.text = 'Hello, QmlPy!'

                with Button() as btn:
                    btn.anchors = {
                        'horizontal_center': rct.horizontal_center,
                        'bottom': rct.bottom,
                        'margins': 12
                    }
                    btn.text = 'Update Text'
                    btn.clicked.connect(xlambda('event', """
                        txt.text += '!'
                    """)
        app.run()


if __name__ == '__main__':
    main()
```

It can be translated to QML code, like below:

```qml
import QtQuick
import QtQuick.Controls

Window {
    id: win
    title: 'QmlPy Demo App'
    width: 800
    height: 600
    visible: true

    Rectangle {
        id: rct
        anchors.fill: win
        anchors.margins: 24
        color: 'navyblue'

        Text {
            id: txt
            anchors.centerIn: rct
            text: 'Hello, QmlPy!'
        }

        Button {
            id: btn
            anchors {
                horizontalCenter: rct.horizontalCenter
                bottom: rct.bottom
                margins: 12
            }
            text: 'Update Text'
            onClicked: (event) => {
                txt.text += '!'
            }
        }
    }
}
```
