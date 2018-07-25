# -*- mode: python -*-

block_cipher = None

# This is not ideal; I need to manually update this spec file for every new generator
a = Analysis(['updater.spec'],
             hiddenimports=['argparse',
                            'tkinter',
                            'tkinter.filedialog',
                            'tkinter.messagebox',
                            'shutil', 
                            'subprocess',
                            'generators.base_gen',
                            'generators.cpp',
                            'generators.unity',
                            'generators.r',
                            'generators.latex',],
             pathex=['C:\\Program Files (x86)\\Windows Kits\\10\\Redist\\ucrt\\DLLs\\x64'],
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
