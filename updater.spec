# -*- mode: python -*-

block_cipher = None


a = Analysis(['updater.py', 'updater.spec'],
             paths=['generators'],
             hiddenimports=['argparse', 'shutil', 'subprocess', 'base_gen'],
             binaries=[],
             datas=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='updater',
          debug=False,
          strip=False,
          upx=True,
          console=True)
app = BUNDLE(exe,
         name='Updater.app',
         icon=None,
         bundle_identifier=None)
