@echo off

rem Set Starting Conditions
SET OLDPATH=%PATH%
SET SUBDIR=%CD%

rem Setup main env

cd /d %~dp0..\..
call set_env.bat

cd /d %~dp0..

rem Setup local env
rem call set_env_local.bat

start bin\pgsql\bin\pg_ctl stop -D DatabaseData

rem Cleanup

cd %SUBDIR%
PATH %OLDPATH%

@echo on
