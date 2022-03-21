import os
import copy
import shutil
import re
import tempfile
import glob
import yaml
import markdown
import jinja2


class RenderingErr(Exception):
    pass


class MdDoc:
    def __init__(self, path):
        self.path = path
        with open(path) as f:
            s = f.read()

        yml = s.split("---")[1]
        self.config = yaml.safe_load(yml)

        self.body = s.split("---")[2].strip()


class Tanuky:
    def __init__(self, srcdir="./src", tpldir="./templates", distdir="./dist"):
        self.srcdir = srcdir
        self.tpldir = tpldir
        self.distdir = distdir
        self.mdlist = []
        self.globals = {}

    def mkhtml(self, mdbody):
        return markdown.markdown(mdbody)

    def generate(self):
        files = glob.glob(os.path.join(self.srcdir, "**"), recursive=True)
        with tempfile.TemporaryDirectory() as tmpdir:
            for path in files:
                saveto = os.path.join(tmpdir, re.sub(f"^{self.srcdir}/?", "", path))
                os.makedirs(os.path.dirname(saveto), exist_ok=True)
                if path[-3:] == ".md":
                    self.mdlist.append(MdDoc(path))
                else:
                    if os.path.isfile(path):
                        shutil.copy(path, saveto)

            for mddoc in self.mdlist:
                params = copy.deepcopy(self.globals)
                params.update(mddoc.config)
                params["Body"] = self.mkhtml(mddoc.body)

                if "Template" not in params.keys():
                    raise RenderingErr("No template specified")
                tplpath = os.path.join(self.tpldir, mddoc.config["Template"] + ".html")
                if not os.path.exists(tplpath):
                    raise RenderingErr("Template not found")
                with open(tplpath) as f:
                    tpl = jinja2.Template(f.read())

                saveto = os.path.join(tmpdir, re.sub(f"^{self.srcdir}/?", "", mddoc.path))
                saveto = saveto[:-3] + ".html"
                with open(saveto, "w") as f:
                    f.write(tpl.render(params))

            if os.path.isfile(self.distdir):
                os.remove(self.distdir)
            if os.path.isdir(self.distdir):
                shutil.rmtree(self.distdir)
            shutil.copytree(tmpdir, self.distdir)
