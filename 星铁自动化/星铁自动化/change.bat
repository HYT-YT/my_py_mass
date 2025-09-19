@echo off
set /a i=0

:n1
set /a i=i+1
if exist ".\plan\need_%i%.txt" goto n2
if %i% gtr 10 goto n3
goto n1

:n2
copy ".\plan\plan_%i%.txt" ".\plan.txt"
copy ".\plan_use_exe\exe_%i%.txt" ".\plan_use_exe.txt"
del /s /q ".\plan\need_%i%.txt"
del /s /q ".\plan_use_exe\need_%i%.txt"
exit

:n3
exit