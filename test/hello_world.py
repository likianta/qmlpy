from qmlpy import Application
from qmlpy.widgets import *


with Application() as app:
    with Windows() as win:
        win.width = 400
        win.height = 300
        
        with Text() as txt:
            txt.anchors.center = win
            txt.text = 'hello world'
            
        app.build()
        # app.run()
