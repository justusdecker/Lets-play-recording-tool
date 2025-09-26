# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['../main.py'],
    pathex=['.'],
    binaries=[],
    datas=[],
    hiddenimports=['sqlalchemy.dialects.sqlite'],
    hookspath=['.'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['sqlalchemy.dialects.postgresql',
              'sqlalchemy.dialects.mysql'],
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
    name='lprt',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['..\\bin\\data\\img\\logo.ico'],
)
