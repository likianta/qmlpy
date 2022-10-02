# PyCharm 类型检查和代码补全功能测试及备忘

## 类型检查

cast 需要用等号连接, 才能被正确推断:

```python
from typing import cast

# == wrong ==
width: cast(int, [])
#   width 被识别为 Any 类型.

width += 1  # 无警告, 也无智能提示.
width.append(1)  # 无警告, 也无智能提示.

# == correct ==
width = cast(int, [])
#   width 被识别为 int 类型.

width += 1  # 会给出 int 相关的补全提示.
width.append(1)  # 虽然不会给出 list 的补全提示, 但也不会给出警告.
```

应用:

在 `qmlpy.widgets.widget_props` 中, 我们把诸如 `width: cast(int, Number)` 之类的代码改成了 `width = cast(int, 'Number')`. 即, 告诉 ide 这是一个 int 类型, 但其实是一个字符串 (这样效率比较高, 而且更安全), 再在初始化阶段由 `qmlpy.properties.core.prop_sheet` 内部进行转译, 变成真正的 Number 对象.

## 代码补全

~~如果 class 实现了 `__enter__` 和 `__exit__` 方法, 但 pycharm 可能仍然无法正确处理它, 导致代码补全失效. 例如, 下面是一段没有问题的代码...~~
