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

call bin\psql -h localhost -p 9489 -U postgre -d MainData %*

rem Cleanup

cd %SUBDIR%
PATH %OLDPATH%

@echo on
