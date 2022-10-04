from lk_utils import relpath

from qmlpy import Application
from qmlpy.widgets import *

with Application() as app:
    
    with Window() as win:
        win.title = 'Hello World'
        win.width = 400
        win.height = 300
        win.visible = True
        
        with Rectangle() as rct:
            rct.width = 100
            rct.height = 100
            rct.color = 'yellow'
        
        with Button() as btn:
            btn.text = 'click me'
    
    app.build(dir_o=relpath('.'))
    print('build done. see result in `./index.qml`')
    # app.run()
