@echo off

rem Set Starting Conditions
SET OLDPATH=%PATH%
SET SUBDIR=%CD%

rem Setup and run GeneralTesting

cd /d "%~dp0\GeneralTesting"
call ..\set_env.bat

@echo on
call ..\Python27\python.exe InitializeTables.py -host=localhost -port=9489 -db=MainData -user=postgre -file="data\ISWI NCP Binding Double Label All 4 6 2012.dat" -schema=NCP %1
call ..\Python27\python.exe InsertData.py -host=localhost -port=9489 -db=MainData -user=postgre -file="data\ISWI NCP Binding Double Label All 4 6 2012.dat" -runs=10 -data_type=2 -schema=NCP %1
@echo off

PAUSE

rem Cleanup

cd %SUBDIR%
PATH %OLDPATH%

@echo on
