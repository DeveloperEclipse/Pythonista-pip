Pythonista-pip downloads a Python library and all its dependencies into a lib folder in your project. Allowing use of packages that arent natively built into Pythonista.

Simple installer:
Create a file named install.py, paste the contents and run it.
```py
import urllib.request
urllib.request.urlretrieve("https://raw.githubusercontent.com/DeveloperEclipse/Pythonista-pip/refs/heads/main/src/pyistapip.py", "pyistapip.py")
print(f"Run pyistapip.py to begin")
```

Usage:
1.	Run the script.
2.	Enter the package name.
3.	Pythonista-pip downloads the package and all of its dependencies (even sub-dependencies).

Then, when using the library in Pythonista:

```python
import sys
sys.path.insert(0, r'./lib')
import your_package
```

* Some libraries use subprocess, which Pythonista doesn't support.
* Pythonista-pip downloads sdist only, not wheels.
* Not all libraries may work as expected.

![Image](https://github.com/DeveloperEclipse/Pythonista-pip/blob/main/assets/IMG_1226.jpeg?raw=true![image](https://github.com/user-attachments/assets/db4027af-81b0-40f3-a26b-59bdc045cfa4)
)
