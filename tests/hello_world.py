from qmlpy import Application
from qmlpy.widgets import *

with Application() as app:
    with Window() as win:
        win.title = 'Hello World'
        
        with (txt := Text()):
            txt.content_width
            txt.anchors.center = win
            txt.text = 'hello world'
        
        app.build()
        # app.run()
