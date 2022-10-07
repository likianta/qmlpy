# Notice

The "blueprint" project is partially come from my former project: *pyml*.

For some history reasons, "blueprint" remains the old-style code, which is not
much compilant with current one.

I'm working on to update this project to follow the new guidelines. But before
this work is done, be notice that there are some inconviniences listed below:

- Most comments were written in Chinese.
- Its parser was focus on parsing Qt 5.15, which is slightly incompatible with
  Qt 6.
- Many terms and descriptions were referred to the old project, so you may see
  the word "pyml" in many occurances.

# Requirements

## Python

Required python 3.8+ (recommend 3.10) and pip install...

- argsense
- bs4
- lk-logger >= 5.4.0
- lk-utils >= 2.4.0

## Qt Documents

1. Install official Qt 5.15 or Qt 6.x.
    1. Tick the "source" option, that will download Qt documentation resources.
    2. Assumed you haved installed in `d:/programs/qt` (laterly we call it
    `<qt_root>`)
2. Copy `<qt_root>/Docs/Qt-5.15/qtdoc/modules-qml.html` to
   `<project>/blueprint/resources/qtdoc/1_all_qml_modules.html`.
3. Copy `<qt_root>/Docs/Qt-5.15/qtdoc/qmltypes.html` to
   `<project>/blueprint/resources/qtdoc/2_all_qml_types.html`.
4. Edit `<project>/blueprint/src/io.py`, change the value `qt_source = None` to
   the path to your "qtdoc" path, for example:
   `qt_source = 'd:/programs/qt/Docs/Qt-5.15/qtdoc'`.

# Run

```sh
cd blueprint

# Get help
python run.py -h

# Parse html files and generate json files.
python run.py indexing-qml-modules
#   (remember adding '-h' can also get help.)

# Generate basic properties
python run.py generate-basic-properties

# Generate group properties
python run.py generate-group-properties

# Generate widgets api
python run.py generate-widgets-api
```
