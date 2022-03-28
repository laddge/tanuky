![DB69894C-2EEF-4D2F-AFB8-028A4D9DE74A](https://user-images.githubusercontent.com/67098414/159828477-68bba999-b4dc-4249-94e0-5ad594627d6d.png)

# tanuky: simple &amp; flexible SSG

## Description
This is a simple SSG (Static Site Generator) written in Python.  
Unlike other common SSGs, this tool provides only minimal functionality.  
It generates a site based on a template and markdown, that's all.  
Therefore, all the possibilities of the site that can be created are left to the designer.

## Installation
From pypi (recommended):
```
pip install tanuky
```

If you want the latest commit:
```
pip install git+https://github.com/laddge/tanuky
```

From source:
```
git clone https://github.com/laddge/tanuky ./tanuky
cd tanuky
python setup.py install
```

## Usage
### File placement
```
.
├── dist # distdir
├── src # srcdir
│   ├── css
│   │   └── style.css
│   ├── images
│   │   └── dog.jpeg
│   ├── js
│   │   └── main.js
│   ├── pages
│   │   └── example.md
│   └── index.html
├── templates # tpldir
│   └── hoge.html
└── generate.py
```

* distdir (default: ./dist)  
Generated files are placed here.  
Overwritten each times.

* srcdir (default: ./src)  
Put source files here.

* tpldir (default: ./templates)  
Put templates here.  
Template files must be named ```{template_name}.html```.

After generated:
```
./dist # distdir
├── css
│   └── style.css
├── images
│   └── dog.jpeg
├── js
│   └── main.js
├── pages
│   └── example.html
└── index.html
```
Like this, Markdown is converted to HTML and other files are copied exactly as they are.

### How to write Markdown
ex:
```
---
Template: hoge
Title: Hoge Fuga
Desc: test page
---

# Test page
hoge...
```

* Front matter  
Write page config between "---" in Yaml.  
Its value passed to the template.

* Template name  
Template name must be defined in Front matter.  
And, respective template file must be in tpldir.

* Markdown sentences  
Markdown sentences are convert to HTML and passed to template as "Body".

### How to write templates
ex:
```
<!DOCTYPE html>
<html>
    <head>
        <meta name="description" content="{{ Desc }}">
        <title>{{ Title }}</title>
    </head>
    <body>
        {{ Body }}
    </body>
</html>
```
Tanuky uses template engine [Jinja2](https://jinja.palletsprojects.com/).  
Variables defined in Front matter can be used in template.  
```{{ Body }}``` shows contents which is converted from Markdown.

### Generate script
```
# generate.py
import tanuky

tnk = tanuky.Tanuky()
tnk.generate()
```
The generator works with just this script.

* ```tnk = tanuky.Tanuky()```  
Define the generator object.  
You can specify srcdir, tpldir, distdir like this:  
```tnk = tanuky.Tanuky(srcdir="./src", tpldir="./templates", distdir="./dist")```

* ```tnk.generate()```  
Start generate process.

### Advanced
#### Define globals
ex:
```
# generate.py
import tanuky

tnk = tanuky.Tanuky()


def func(arg):
    return f"Arg: {arg}"


hoge = "test var"
tnk.globals.update(func=func)
tnk.globals.update(hoge=hoge)
tnk.generate()
```
You can define global variables or functions using ```tnk.globals.update()```.  
They are refered in templates like variables defined in Front matter, and they have lower priority than Front matter.

#### Custom Markdown converter
By default, tanuky uses [Python-Markdown](https://github.com/Python-Markdown/markdown) as Markdown converter.  
If you want to use another converter, use this:
```
# generate.py
import tanuky


class MyTanuky(tanuky.Tanuky):
    def mkhtml(self, mdbody):
        # convert mdbody to html
        return html


tnk = MyTanuky()
tnk.generate()
```

## Example
An example is available on [laddge/tanuky-example](https://github.com/laddge/tanuky-example).

## Release Note
### [v1.0.3](https://github.com/laddge/tanuky/releases/tag/v1.0.3) (2022/03/28)
Move example tree to another repo

### [v1.0.2](https://github.com/laddge/tanuky/releases/tag/v1.0.2) (2022/03/25)
Add example tree

### [v1.0.1](https://github.com/laddge/tanuky/releases/tag/v1.0.1) (2022/03/24)
Fix install bug

### [v1.0.0](https://github.com/laddge/tanuky/releases/tag/v1.0.0) (2022/03/24)
First release

## License
This plugin is under the MIT-License.  
See also [LICENSE](LICENSE).

## Author
Laddge
