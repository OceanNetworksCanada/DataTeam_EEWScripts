set root=C:\Users\jkukovic\AppData\Local\Continuum\anaconda3
call %root%\Scripts\activate.bat %root%
call conda activate obspy
:loop
python C:\Users\jkukovic\PythonScripts\DMASMonitorCheck_v2.py
timeout /t 10
goto loop
