pyinstaller -F -i icon.ico ^
-n "casa_das_maquinas" ^
--add-data "C:/Users/Kai_Xtr/Documents/'Casa das Máquinas'/Maps/*;." ^
--add-data "C:/Users/Kai_Xtr/Documents/'Casa das Máquinas'/Fonts/*;." ^
--add-data "C:/Users/Kai_Xtr/Documents/'Casa das Máquinas'/Tiles/*;." ^
--add-data "C:/Users/Kai_Xtr/Documents/'Casa das Máquinas'/SFX/*;." ^
--add-data "C:/Users/Kai_Xtr/Documents/'Casa das Máquinas'/Sprites/*;." ^
--add-data "database.py;." ^
--add-data "icon.ico;." ^
main.py