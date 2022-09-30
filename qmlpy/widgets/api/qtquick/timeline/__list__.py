from .__base__ import *


class Keyframe(QtObject, W.PsKeyframe):
    pass


class KeyframeGroup(QtObject, W.PsKeyframeGroup):
    pass


class Timeline(QtObject, W.PsTimeline):
    pass


class TimelineAnimation(NumberAnimation, W.PsTimelineAnimation):
    pass
