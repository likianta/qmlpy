# Notice

The "blueprint" project is partially come from my former project: *pyml*.

For some history reasons, "blueprint" remains the old-style code, which is not
much compilant with current one.

I'm working on to update this project to follow the new guidelines. But before
this work is done, be notice that there are some inconvinience listed below:

- Most comments were written in Chinese.
- Its parser was focus on parsing Qt 5.15, which is slightly incompatible with
  Qt 6.
- Many terms and descriptions were referred to the old project, so you may see
  the word "pyml" in many occurances.

# Requirements

Required python 3.8+ (recommend 3.10) and pip install...

- argsense
- bs4
- lk-logger >= 5.4.0
- lk-utils >= 2.4.0

Resources preparation see `./src/qml_modules_indexing/io.py:docstring`.

# How to use

To generate structured data from `resources/*.html` to `resouces/*.json`, run
this script:

```sh
cd src/qml_modules_indexing
python main.py
```

To generate `qmlpy` modules from `resouces/*.json` to `qmlpy/widgets/*`, run
this script:

```sh
cd src/template_generator
python main.py
```
