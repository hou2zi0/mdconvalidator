# MDConvalidator

Sample pipeline to create DHConvalidator compatible files from Markdown.

## Requirements

* Python3
    * pypandoc: `pip3 install pypandoc`
    * lxml: `pip3 install lxml`
* pandoc:  `brew install pandoc`
* pandoc-citeproc: `brew install pandoc-citeproc`

## How to use it

### Python

Basic usage:

```python
import mdconvalidator as ConV
MDC = ConV.MDConvalidator('example/1_Digital_Humanities.md', 'convalidator.zip')
MDC.convalidate()
```

Additional outputs:

```python
MDC = ConV.MDConvalidator('example/1_Digital_Humanities.md', 'convalidator.zip')
# Get a pdf as well: possible outputs are html, tei, and pdf
mdc.convalidate(['html','tei','pdf'])
```

Adjust default settings:

```python
# Use pandocs citeproc
MDC.use_citeproc = True
# Get information about your (py)pandoc installation
MDC.get_pandoc_info()
# Set your pandoc path
MDC.set_pandoc_path('/my/local/path/to/pandoc')
# Set additional parameters for PDF output
params = {'pdf': ['-V', 'geometry:margin=1.5cm']}
mdc.convalidate(['html','tei','pdf'], additional=params)
```
