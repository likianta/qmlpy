# 核心设计精髓

## 属性 (Property) 的分类

属性分为三类:

- 基本属性 (basic_properties)
- 组属性 (group_properties)
- 特殊属性 (special_properties)

### 基本属性

基本属性参考了 [all qml basic types](https://doc.qt.io/qt-6/qmlbasictypes.html), 它是 qml 中可以使用的基本属性类型.

它们是一个非常小的列表, 只有十几个类型, 里面有我们非常熟悉的 bool, int, double, string, 以及 color, date, url 等.

但请注意, 我们在设计基本属性时, 只是参考了 qml basic types, 但并没有完全一一对应地封装. 比如, font 是 qml 基本类型, 但是我们并不认为它是 "基本属性", 而是 "组属性" (见下一节的讨论). 所以, 最终我们所认定的基本属性, 以及它们的具体行为, 请以源代码 `qmlpy.property.basic` 为准.

### 组属性

组属性是一个可以通过点号 (.) 来链式访问其子属性的一个属性集合. 例如 `border` 作为组属性, 它有 `border.width`, `border.color` 等子属性; `point` 作为组属性, 它有 `point.x`, `point.y` 等子属性; 同样, `font` 作为组属性, 它有 `font.family`, `font.bold`, `font.pixel_size` 等子属性 (这就是为什么我们认为 font 不是 "基本属性" 的原因).

组属性的列表比较长, 我们使用了 blueprint 工具从 qml 的全部类型中抽取出所有符合上述规则的属性, 并以 "Ps" (Property Set) 为前缀, 作为组属性的名称. 完整的列表可在 `qmlpy.property.group_types.api` 中找到.

备注:

- TODO: 我们正在考虑将 "group" 术语更名. 目前有几个候选: "set", "sheet", "chain". 现在仍处于提案状态; 当新的术语确认后, 本条备忘将被删除.

相关阅读:

- 组属性是如何生成的: `~/blueprint/run.py : def list_all_group_properties`

### 特殊属性

TODO

## 为什么设计 PropSheet, 它是用来做什么的?

TODO

## 说一下 prop_sheet 和 widget_props 的区别和联系

TODO
