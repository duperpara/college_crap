import PyInstaller.__main__
import os
from pathlib import Path

exe_name = "exe_name"

PyInstaller.__main__.run([  # Creates exe
    'main.py',  # uncoment for first run
    '.\\main.spec',
    '--onefile',
    # '--console',
])

# Rename/Replace
rename_exe_path = os.path.join(os.getcwd(), "dist\\" + exe_name + ".exe")
if Path(rename_exe_path).is_file():
    os.remove(rename_exe_path)
os.rename(os.path.join(os.getcwd(), "dist/main.exe"), rename_exe_path)

