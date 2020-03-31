# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['C:\\Users\\Kai_Xtr\\Documents\\Casa das Máquinas'],
             binaries=[],
             datas=[("C:/Users/Kai_Xtr/Documents/'Casa das M├íquinas'/Maps/*", '.'), ("C:/Users/Kai_Xtr/Documents/'Casa das M├íquinas'/Fonts/*", '.'), ("C:/Users/Kai_Xtr/Documents/'Casa das M├íquinas'/Tiles/*", '.'), ("C:/Users/Kai_Xtr/Documents/'Casa das M├íquinas'/SFX/*", '.'), ("C:/Users/Kai_Xtr/Documents/'Casa das M├íquinas'/Sprites/*", '.'), ('database.py', '.'), ('icon.ico', '.')],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='casa_das_maquinas',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True , icon='icon.ico')
