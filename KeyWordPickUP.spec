# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['KeyWordPickUP.py'],
             pathex=['C:\\Users\\Motoki Sato\\cursor-ai-KeyWordPickUP'],
             binaries=[],
             datas=[('C:\\Users\\Motoki Sato\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages\\janome\\sysdic', 'janome\\sysdic')],
             hiddenimports=[],
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
          [],
          exclude_binaries=True,
          name='KeyWordPickUP',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False)

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='KeyWordPickUP')