@echo off

rem Set Starting Conditions
SET OLDPATH=%PATH%
SET SUBDIR=%CD%

rem Setup and run GeneralTesting

cd /d "%~dp0\GeneralTesting"
call ..\set_env.bat

@echo on
rem call ..\Python27\python.exe -m cProfile -o profileoutput DataAnalyzer.py -host=localhost -port=9489 -db=MainData -user=postgre -start_num=1 -end_num=10001 %1
rem start ..\Python27\python.exe DataAnalyzer.py -host=localhost -port=9489 -db=MainData -user=postgre -start_num=2 -end_num=5000 -analysis_type=1 -schema=batch %1
rem start ..\Python27\python.exe DataAnalyzer.py -host=localhost -port=9489 -db=MainData -user=postgre -start_num=5000 -end_num=10001 -analysis_type=2 -schema=batch %1
rem start ..\Python27\python.exe DataAnalyzer.py -host=localhost -port=9489 -db=MainData -user=postgre -start_num=2 -end_num=5000 -analysis_type=1 -schema=batch %1


rem call ..\Python27\python.exe DataAnalyzer.py -host=localhost -port=9489 -db=MainData -user=postgre -start_num=1 -end_num=5000 -analysis_type=20 -schema=public %1
rem start ..\Python27\python.exe DataAnalyzer.py -host=localhost -port=9489 -db=MainData -user=postgre -start_num=1 -end_num=1000 -analysis_type=50 -schema=public %1
rem start ..\Python27\python.exe DataAnalyzer.py -host=localhost -port=9489 -db=MainData -user=postgre -start_num=1001 -end_num=2000 -analysis_type=51 -schema=public %1
rem start ..\Python27\python.exe DataAnalyzer.py -host=localhost -port=9489 -db=MainData -user=postgre -start_num=2001 -end_num=3000 -analysis_type=52 -schema=public %1
rem start ..\Python27\python.exe DataAnalyzer.py -host=localhost -port=9489 -db=MainData -user=postgre -start_num=3001 -end_num=4000 -analysis_type=53 -schema=public %1
rem start ..\Python27\python.exe DataAnalyzer.py -host=localhost -port=9489 -db=MainData -user=postgre -start_num=4001 -end_num=5000 -analysis_type=54 -schema=public %1

start ..\Python27\python.exe DataAnalyzer.py -host=localhost -port=9489 -db=MainData -user=postgre -start_num=20002 -end_num=22500 -analysis_type=55 -schema=public %1
start ..\Python27\python.exe DataAnalyzer.py -host=localhost -port=9489 -db=MainData -user=postgre -start_num=22501 -end_num=24995 -analysis_type=56 -schema=public %1

rem 20002 24995
@echo off
PAUSE
rem Cleanup

cd %SUBDIR%
PATH %OLDPATH%

@echo on
