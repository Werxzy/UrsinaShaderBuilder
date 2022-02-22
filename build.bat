cd .\UrsinaShaderBuilder\
python -m ursina.build
cd .\build\python\

set loc=C:\Users\Werxzy\AppData\Local\Programs\Python\Python39

xcopy %loc%\Lib\json\ .\Lib\json\ /E
xcopy %loc%\Lib\tkinter\ .\Lib\tkinter\ /E
xcopy %loc%\tcl\ .\tcl\ /E
copy %loc%\DLLs\_tkinter.pyd .\DLLs\
copy %loc%\DLLs\tk86t.dll .\DLLs\
copy %loc%\DLLs\tcl86t.dll .\DLLs\
