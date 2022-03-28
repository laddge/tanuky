import os
import copy
import shutil
import re
import tempfile
import glob
import tqdm
import yaml
import markdown
import jinja2


class RenderingErr(Exception):
    """RenderingErr.
    """

    pass


class MdDoc:
    """MdDoc.
    """

    def __init__(self, path):
        """__init__.

        Parameters
        ----------
        path :
            path
        """
        self.path = path
        with open(path) as f:
            s = f.read()

        yml = s.split("---")[1]
        self.config = yaml.safe_load(yml)

        self.body = s.split("---")[2].strip()


class Tanuky:
    """Tanuky.
    """

    def __init__(self, srcdir="./src", tpldir="./templates", distdir="./dist"):
        """__init__.

        Parameters
        ----------
        srcdir :
            srcdir
        tpldir :
            tpldir
        distdir :
            distdir
        """
        self.srcdir = srcdir
        self.tpldir = tpldir
        self.distdir = distdir
        self.env = jinja2.Environment(loader=jinja2.FileSystemLoader(tpldir))
        self.mdlist = []
        self.globals = {}

    def mkhtml(self, mdbody):
        """mkhtml.

        Parameters
        ----------
        mdbody :
            mdbody
        """
        return markdown.markdown(mdbody)

    def generate(self):
        """generate.
        """
        print(f"srcdir = '{self.srcdir}'")
        print(f"tpldir = '{self.tpldir}'")
        print(f"distdir = '{self.distdir}'")
        files = glob.glob(os.path.join(self.srcdir, "**"), recursive=True)
        with tempfile.TemporaryDirectory() as tmpdir:
            print(" - Scanning...")
            for path in tqdm.tqdm(files):
                saveto = os.path.join(tmpdir, re.sub(f"^{self.srcdir}/?", "", path))
                os.makedirs(os.path.dirname(saveto), exist_ok=True)
                if path[-3:] == ".md":
                    self.mdlist.append(MdDoc(path))
                else:
                    if os.path.isfile(path):
                        shutil.copy(path, saveto)

            print(" - Rendering...")
            for mddoc in tqdm.tqdm(self.mdlist):
                params = copy.deepcopy(self.globals)
                params.update(mddoc.config)
                params["Body"] = self.mkhtml(mddoc.body)

                if "Template" not in params.keys():
                    raise RenderingErr("No template specified")
                tplname = mddoc.config["Template"] + ".html"
                tpl = self.env.get_template(tplname)

                saveto = os.path.join(tmpdir, re.sub(f"^{self.srcdir}/?", "", mddoc.path))
                saveto = saveto[:-3] + ".html"
                with open(saveto, "w") as f:
                    f.write(tpl.render(params))

            if os.path.isfile(self.distdir):
                os.remove(self.distdir)
            if os.path.isdir(self.distdir):
                shutil.rmtree(self.distdir)
            shutil.copytree(tmpdir, self.distdir)
            print(" - Done.")
