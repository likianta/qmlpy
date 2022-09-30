from .__base__ import *


class AxisHelper(Node, W.PsAxisHelper):
    pass


class DebugView(Rectangle, W.PsDebugView):
    pass


class GridGeometry(Geometry, W.PsGridGeometry):
    pass


class InstanceRange(Object3D, W.PsInstanceRange):
    pass


class RandomInstancing(Instancing, W.PsRandomInstancing):
    pass


class WasdController(Item, W.PsWasdController):
    pass
