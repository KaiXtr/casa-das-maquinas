pyinstaller \
--clean \
--onefile \
--noconfirm \
--windowed \
--workpath "./build" \
--distpath "./dist" \
--add-data "./Fonts:./Fonts" \
--add-data "./Maps:./Maps" \
--add-data "./SFX:./SFX" \
--add-data "./Sprites:./Sprites" \
--add-data "./Tiles:./Tiles" \
--add-data "./icon.ico:." \
--name "Casa das Máquinas" \
--icon "icon.ico" \
main.py
