from qmlpy import Application
from qmlpy.widgets import *

with Application() as app:
    with Window() as win:
        win.title = 'Hello World'
        
        with Button() as btn:
            btn.text = ...
        
        with (txt2 := Text()):
            txt2.anchors.center = win
            txt2.text = 'hello world'
        
        app.build()
        # app.run()
