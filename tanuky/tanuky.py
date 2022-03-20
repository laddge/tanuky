import yaml


class MdDoc:
    def __init__(self, path):
        with open(path) as f:
            s = f.read()

        yml = s.split("---")[1]
        self.config = yaml.safe_load(yml)

        self.body = s.split("---")[2].strip()


class Tanuky:
    def __init__(self, srcdir="./src", tpldir="./template", distdir="./dist"):
        self.srcdir = srcdir
        self.tpldir = tpldir
        self.distdir = distdir
