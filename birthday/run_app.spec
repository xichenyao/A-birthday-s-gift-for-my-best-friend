# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.utils.hooks import copy_metadata

datas = [
    ("D:/python/Lib/site-packages/streamlit/runtime", "./streamlit/runtime"),
    ("D:/python/Lib/site-packages/streamlit/static", "./streamlit/static"),  # 添加这一行
]
datas+=collect_data_files("streamlit")
datas += collect_data_files("langchain") + copy_metadata("langchain") 
datas += copy_metadata("streamlit")

block_cipher = None


a = Analysis(
    ['run_app.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=['langchain.memory', 'langchain.prompts','langchain.chains'],
    hookspath=['./hooks'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='run_app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
