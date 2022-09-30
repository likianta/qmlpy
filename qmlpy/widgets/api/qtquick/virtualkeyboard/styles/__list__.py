from .__base__ import *


class KeyboardStyle(QtObject, W.PsKeyboardStyle):
    pass


class KeyIcon(Item, W.PsKeyIcon):
    pass


class KeyPanel(Item, W.PsKeyPanel):
    pass


class SelectionListItem(Item, W.PsSelectionListItem):
    pass


class TraceCanvas(Canvas, W.PsTraceCanvas):
    pass


class TraceInputKeyPanel(Item, W.PsTraceInputKeyPanel):
    pass
