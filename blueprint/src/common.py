import re


def camel_2_snake_case(name: str):
    """ 驼峰转下划线式命名.

    Args:
        name:
            name 中只包含: 大小写字母, 数字和点号
            name 中数字不可以出现在开头

    References:
        https://www.yuque.com/tianyunperfect/ygzsw4/av4s8q
    """
    name = (
        name  # 针对一些特殊转换做预处理
        .replace('QtQuick', 'qtquick')
        .replace('QtQml', 'qtqml')
        .replace('Qt.labs', 'qt_labs')
    )
    name = re.sub(r'(?<!\d)([A-Z][A-Z]+)(?=[A-Z][a-z]|$)', r'_\1_', name)
    ''' 将单词中的连续全大写单词 "抽出来". examples:

        1. 'webRTCPublicInterfacesOnly' -> 'web_RTC_PublicInterfacesOnly'
        2. 'webGLEnabled' -> 'web_GL_Enabled'
        3. 'enableXYGrid' -> 'enable_XY_Grid'
        4. 'useOpenGL' -> 'useOpen_GL_'
    '''
    for i in re.findall(r'_[A-Z]+_', name):
        name = name.replace(i, i.lower(), 1)
    ''' examples
        1. 'web_RTC_PublicInterfacesOnly' -> 'web_rtc_PublicInterfacesOnly'
        2. 'web_GL_Enabled' -> 'web_gl_Enabled'
    '''
    name = re.sub(r'(?<![._\d])([A-Z])', r'_\1', name).lower().strip('_')
    ''' examples

        for modules:
            1. 'QtDataVisualization' -> '_Qt_Data_Visualization'
                -> 'qt_data_visualization'
            2. 'QtCharts' -> '_Qt_Charts' -> 'qt_charts'
            3. 'Qt3D' -> '_Qt3D' -> 'qt3d'
            4. 'Qtquick.Scene2D' -> '_Qtquick.Scene2D' -> 'qtquick.scene2d'
            5. 'Qtquick.Controls' -> '_Qtquick.Controls' -> 'qtquick.controls'

        for properties:
            1. 'width' -> 'width'
            2. 'accelerated2dCanvasEnabled' -> 'accelerated2d_Canvas_Enabled'
                -> 'accelerated2d_canvas_enabled'
            3. 'control1X' -> 'control1X' -> 'control1x'
            4. 'relativeControl1X' -> 'relative_Control1X'
                -> 'relative_control1x'
            5. 'flip3DPolicy' -> 'flip3D_Policy' -> 'flip3d_policy'
            6. 'axisXTop' -> 'axis_X_Top' -> 'axis_x_top'
            7. 'enable_XY_Grid' -> 'enable_XY_Grid' -> 'enable_xy_grid'
            8. 'web_RTC_PublicInterfacesOnly'
                -> 'web_RTC_Public_Interfaces_Only'
                -> 'web_rtc_public_interfaces_only'
            9. 'web_GL_Enabled' -> 'web_GL_Enabled' -> 'web_gl_enabled'
            10. 'useOpen_GL_' -> 'use_open_gl'
    '''
    return name


def pascal_to_upper_case(name: str) -> str:
    pattern = re.compile(r'([A-Z][a-z]+)')
    return '_'.join(pattern.findall(name)).upper()
