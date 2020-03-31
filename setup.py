from cx_Freeze import *
import sys
import os

build = {
"path": sys.path + ["app"],
"no_compress": True,
"packages": ["pygame","pytmx","math","random","sys","database"],
"include_files": ['Maps/','Fonts/','Tiles/','Sprites/','SFX/','database.py','icon.ico','readme.txt'],
}

bdist = {
	"initial_target_dir": os.path.expanduser('~') + '/Casa das Máquinas',
	"all_users": False
}

exe = Executable(
	script = r"main.py",
	targetName = "clique_aqui_para_jogar",
	shortcutName = "Casa das Máquinas",
	shortcutDir =  os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'),
	icon = "icon.ico",
    base = "Win32GUI",
)

setup(
	name = "Casa das Máquinas",
	version = "0.0.1",
	description = "casa das máquinas (2020)",
	author = "Matt Kai",
	executables = [exe],
	options = {"build_exe": build}
	)