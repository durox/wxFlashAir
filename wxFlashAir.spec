# -*- mode: python -*-
a = Analysis(['gui.py'],
             pathex=['/home/durox/repos/wxflashair'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
a.datas += [('save.dat', 'save.dat' ,'DATA')]
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='wxFlashAir',
          debug=False,
          strip=None,
          upx=True,
          console=True )
