@echo off

rem Set Starting Conditions
SET OLDPATH=%PATH%
SET SUBDIR=%CD%

rem Setup main env

cd /d %~dp0..\..
call set_env.bat


rem cd /d %~dp0

rem Setup local env
rem call set_env_local.bat

cd /d %~dp0..

cd /d %~dp0\pgsql

start bin\pgAdmin3.exe

rem Cleanup

cd %SUBDIR%
PATH %OLDPATH%

@echo on
