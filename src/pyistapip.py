# Pythonista pip written by Eclipse
# https://github.com/DeveloperEclipse

# Some libraries may not work as expected

import urllib.request
import json
import os
import zipfile
import tarfile
import tempfile
import shutil
import re

dl = set()
libfolder = os.path.join(os.getcwd(), "lib")
os.makedirs(libfolder, exist_ok=True)

def cleandeps(d):
    if not d:
        return None
    d = d.strip()
    if "extra ==" in d or ";" in d:
        return None
    d = d.split("[")[0]
    d = re.split(r"[<>=!~]", d)[0].strip()
    return d or None

def getsetupdeps(p):
    res = []
    with open(p, encoding="utf-8") as f:
        c = f.read()
        m = re.search(r"install_requires\s*=\s*\[([^\]]*)\]", c, re.DOTALL)
        if m:
            for i in m.group(1).split(","):
                dep = cleandeps(i.strip().strip("'\""))
                if dep:
                    res.append(dep)
    return res

def grab(pkg):
    lcpkg = pkg.lower()
    if lcpkg in dl:
        return
    print("\n--- Downloading", pkg, "---")
    try:
        with urllib.request.urlopen(f"https://pypi.org/pypi/{pkg}/json") as r:
            j = json.load(r)
    except:
        print("Failed to get info for", pkg)
        dl.add(lcpkg)
        return

    urls = j.get("urls", [])
    sdist = next((u["url"] for u in urls if u["packagetype"] == "sdist"), None)
    if not sdist:
        print("no sdist for", pkg)
        dl.add(lcpkg)
        return

    fn = sdist.split("/")[-1]
    if not os.path.exists(fn):
        print("DL", fn)
        urllib.request.urlretrieve(sdist, fn)
    else:
        print("Using cached", fn)

    tmp = tempfile.mkdtemp()
    try:
        if fn.endswith(".zip"):
            with zipfile.ZipFile(fn) as z:
                z.extractall(tmp)
        elif fn.endswith((".tar.gz", ".tgz")):
            with tarfile.open(fn, "r:gz") as t:
                t.extractall(tmp)

        for r, _, fs in os.walk(tmp):
            for f in fs:
                if f in ("METADATA","PKG-INFO"):
                    with open(os.path.join(r,f), encoding="utf-8") as x:
                        for line in x:
                            if line.startswith("Requires-Dist:"):
                                d = cleandeps(line.split(":",1)[1])
                                if d and d.lower() not in dl:
                                    grab(d)

        for r, _, fs in os.walk(tmp):
            if "setup.py" in fs:
                for d in getsetupdeps(os.path.join(r,"setup.py")):
                    if d.lower() not in dl:
                        grab(d)

        moved = False
        for r, dirs, files in os.walk(tmp):
            for d in dirs:
                path = os.path.join(r,d)
                if "__init__.py" in os.listdir(path):
                    dest = os.path.join(libfolder, d)
                    if os.path.exists(dest):
                        shutil.rmtree(dest)
                    shutil.copytree(path, dest)
                    moved = True
            for f in files:
                if f.endswith(".py"):
                    dest_dir = os.path.join(libfolder, f)
                    shutil.copy2(os.path.join(r,f), dest_dir)
                    moved = True
        if not moved:
            print("nothing to move for", pkg)

    finally:
        shutil.rmtree(tmp)
        if os.path.exists(fn):
            os.remove(fn)

    dl.add(lcpkg)
    print("done", pkg)

root = input("pip install: ")
grab(root)
print("\nWhen importing, use:\n\n")
print("import sys")
print(f"sys.path.insert(0,r'{libfolder}')")
print("import", root, "\n"*2)
print("Note that some modules use subprocess, which isnt supported on Pythonista. Some libraries might not work as expected.")