from .__base__ import *


class Item(QtObject, W.PsItem):
    pass


class Animation(W.PsAnimation, C):
    pass


class PointerHandler(W.PsPointerHandler, C):
    pass


class PointerDeviceHandler(PointerHandler, W.PsPointerDeviceHandler):
    pass


class Animator(Animation, W.PsAnimator):
    pass


class PropertyAnimation(Animation, W.PsPropertyAnimation):
    pass


class SinglePointHandler(PointerDeviceHandler, W.PsSinglePointHandler):
    pass


class Flickable(Item, W.PsFlickable):
    pass


class MultiPointHandler(PointerDeviceHandler, W.PsMultiPointHandler):
    pass


class NumberAnimation(PropertyAnimation, W.PsNumberAnimation):
    pass


class Image(Item, W.PsImage):
    pass


class Accessible(W.PsAccessible, C):
    pass


class AnchorAnimation(Animation, W.PsAnchorAnimation):
    pass


class AnchorChanges(W.PsAnchorChanges, C):
    pass


class AnimatedImage(Image, W.PsAnimatedImage):
    pass


class AnimatedSprite(Item, W.PsAnimatedSprite):
    pass


class AnimationController(W.PsAnimationController, C):
    pass


class Behavior(W.PsBehavior, C):
    pass


class BorderImage(Item, W.PsBorderImage):
    pass


class BorderImageMesh(W.PsBorderImageMesh, C):
    pass


class Canvas(Item, W.PsCanvas):
    pass


class CanvasGradient(W.PsCanvasGradient, C):
    pass


class CanvasImageData(W.PsCanvasImageData, C):
    pass


class CanvasPixelArray(W.PsCanvasPixelArray, C):
    pass


class ColorAnimation(PropertyAnimation, W.PsColorAnimation):
    pass


class ColorGroup(QtObject, W.PsColorGroup):
    pass


class Column(Item, W.PsColumn):
    pass


class Context2D(W.PsContext2D, C):
    pass


class DoubleValidator(W.PsDoubleValidator, C):
    pass


class Drag(W.PsDrag, C):
    pass


class DragEvent(W.PsDragEvent, C):
    pass


class DragHandler(MultiPointHandler, W.PsDragHandler):
    pass


class DropArea(Item, W.PsDropArea):
    pass


class EnterKey(W.PsEnterKey, C):
    pass


class Flipable(Item, W.PsFlipable):
    pass


class Flow(Item, W.PsFlow):
    pass


class FocusScope(Item, W.PsFocusScope):
    pass


class FontLoader(W.PsFontLoader, C):
    pass


class FontMetrics(W.PsFontMetrics, C):
    pass


class GestureEvent(W.PsGestureEvent, C):
    pass


class Gradient(W.PsGradient, C):
    pass


class GradientStop(W.PsGradientStop, C):
    pass


class GraphicsInfo(W.PsGraphicsInfo, C):
    pass


class Grid(Item, W.PsGrid):
    pass


class GridMesh(W.PsGridMesh, C):
    pass


class GridView(Flickable, W.PsGridView):
    pass


class HandlerPoint(W.PsHandlerPoint, C):
    pass


class HoverHandler(SinglePointHandler, W.PsHoverHandler):
    pass


class IntValidator(W.PsIntValidator, C):
    pass


class ItemGrabResult(QtObject, W.PsItemGrabResult):
    pass


class KeyEvent(W.PsKeyEvent, C):
    pass


class KeyNavigation(W.PsKeyNavigation, C):
    pass


class Keys(W.PsKeys, C):
    pass


class LayoutMirroring(W.PsLayoutMirroring, C):
    pass


class ListView(Flickable, W.PsListView):
    pass


class Loader(Item, W.PsLoader):
    pass


class Matrix4x4(W.PsMatrix4x4, C):
    pass


class MouseArea(Item, W.PsMouseArea):
    pass


class MouseEvent(W.PsMouseEvent, C):
    pass


class MultiPointTouchArea(Item, W.PsMultiPointTouchArea):
    pass


class OpacityAnimator(Animator, W.PsOpacityAnimator):
    pass


class Palette(W.PsPalette, C):
    pass


class ParallelAnimation(Animation, W.PsParallelAnimation):
    pass


class ParentAnimation(Animation, W.PsParentAnimation):
    pass


class ParentChange(W.PsParentChange, C):
    pass


class Path(W.PsPath, C):
    pass


class PathAngleArc(W.PsPathAngleArc, C):
    pass


class PathAnimation(Animation, W.PsPathAnimation):
    pass


class PathArc(W.PsPathArc, C):
    pass


class PathAttribute(W.PsPathAttribute, C):
    pass


class PathCubic(W.PsPathCubic, C):
    pass


class PathCurve(W.PsPathCurve, C):
    pass


class PathElement(W.PsPathElement, C):
    pass


class PathInterpolator(W.PsPathInterpolator, C):
    pass


class PathLine(W.PsPathLine, C):
    pass


class PathMove(W.PsPathMove, C):
    pass


class PathMultiline(W.PsPathMultiline, C):
    pass


class PathPercent(W.PsPathPercent, C):
    pass


class PathPolyline(W.PsPathPolyline, C):
    pass


class PathQuad(W.PsPathQuad, C):
    pass


class PathSvg(W.PsPathSvg, C):
    pass


class PathText(W.PsPathText, C):
    pass


class PathView(Item, W.PsPathView):
    pass


class PauseAnimation(Animation, W.PsPauseAnimation):
    pass


class PinchArea(Item, W.PsPinchArea):
    pass


class PinchEvent(W.PsPinchEvent, C):
    pass


class PinchHandler(MultiPointHandler, W.PsPinchHandler):
    pass


class PointHandler(SinglePointHandler, W.PsPointHandler):
    pass


class Positioner(W.PsPositioner, C):
    pass


class PropertyAction(Animation, W.PsPropertyAction):
    pass


class PropertyChanges(W.PsPropertyChanges, C):
    pass


class Rectangle(Item, W.PsRectangle):
    pass


class RegularExpressionValidator(W.PsRegularExpressionValidator, C):
    pass


class Repeater(Item, W.PsRepeater):
    pass


class Rotation(W.PsRotation, C):
    pass


class RotationAnimation(PropertyAnimation, W.PsRotationAnimation):
    pass


class RotationAnimator(Animator, W.PsRotationAnimator):
    pass


class Row(Item, W.PsRow):
    pass


class Scale(W.PsScale, C):
    pass


class ScaleAnimator(Animator, W.PsScaleAnimator):
    pass


class ScriptAction(Animation, W.PsScriptAction):
    pass


class SequentialAnimation(Animation, W.PsSequentialAnimation):
    pass


class ShaderEffect(Item, W.PsShaderEffect):
    pass


class ShaderEffectSource(Item, W.PsShaderEffectSource):
    pass


class Shortcut(W.PsShortcut, C):
    pass


class SmoothedAnimation(NumberAnimation, W.PsSmoothedAnimation):
    pass


class SpringAnimation(NumberAnimation, W.PsSpringAnimation):
    pass


class Sprite(W.PsSprite, C):
    pass


class SpriteSequence(Item, W.PsSpriteSequence):
    pass


class State(W.PsState, C):
    pass


class StateChangeScript(W.PsStateChangeScript, C):
    pass


class StateGroup(W.PsStateGroup, C):
    pass


class SystemPalette(W.PsSystemPalette, C):
    pass


class TableView(Flickable, W.PsTableView):
    pass


class TapHandler(SinglePointHandler, W.PsTapHandler):
    pass


class Text(Item, W.PsText):
    pass


class TextEdit(Item, W.PsTextEdit):
    pass


class TextInput(Item, W.PsTextInput):
    pass


class TextMetrics(W.PsTextMetrics, C):
    pass


class TouchPoint(W.PsTouchPoint, C):
    pass


class Transform(W.PsTransform, C):
    pass


class Transition(W.PsTransition, C):
    pass


class Translate(W.PsTranslate, C):
    pass


class UniformAnimator(Animator, W.PsUniformAnimator):
    pass


class Vector3dAnimation(PropertyAnimation, W.PsVector3dAnimation):
    pass


class ViewTransition(W.PsViewTransition, C):
    pass


class WheelEvent(W.PsWheelEvent, C):
    pass


class WheelHandler(SinglePointHandler, W.PsWheelHandler):
    pass


class Window(W.PsWindow):
    
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class XAnimator(Animator, W.PsXAnimator):
    pass


class YAnimator(Animator, W.PsYAnimator):
    pass
