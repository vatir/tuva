@echo off

rem Set Starting Conditions
SET OLDPATH=%PATH%
SET SUBDIR=%CD%

rem Setup and run GeneralTesting

cd /d "%~dp0\GeneralTesting"
call ..\set_env.bat

@echo on
call ..\Python27\python.exe InsertData.py -host=localhost -port=9489 -db=MainData -user=postgre -file="data/ISWI DNA Binding 3 30 2012.dat" -runs=5000 -data_type=50 -schema=public %1
@echo off

PAUSE

rem Cleanup

cd %SUBDIR%
PATH %OLDPATH%

@echo on
