# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


SETUP_DIR = 'G:\\mycode\\opcdaBRGmqtt\\'

a = Analysis(['main.py'],
             pathex=['G:\\mycode\\opcdaBRGmqtt'],
             binaries=[],
             datas=[(SETUP_DIR+'admin\\templates','admin\\templates'),(SETUP_DIR+'admin\\static','admin\\static')],
             hiddenimports=['opcdabrg.app'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True ,
          icon='bitbug_favicon.ico',
          uac_admin=True)
