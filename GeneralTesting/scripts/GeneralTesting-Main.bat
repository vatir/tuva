@echo off

rem Set Starting Conditions
SET OLDPATH=%PATH%
SET SUBDIR=%CD%

rem Setup and run GeneralTesting

cd /d "%~dp0\GeneralTesting"
call ..\set_env.bat

start ..\Python27\pythonw.exe main.py %1

rem wscript.exe ..\bin\invis.vbs ..\Python27\python.exe main.py %*

rem Cleanup

cd %SUBDIR%
PATH %OLDPATH%

@echo on
