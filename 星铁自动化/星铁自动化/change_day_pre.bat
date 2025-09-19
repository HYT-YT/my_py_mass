@echo off
set /a i=0
del /s /q ".\plan.txt"
del /s /q ".\plan_use_exe.txt"
:n1
set /a i=i+1
if exist "./plan/plan_%i%.txt" goto n2
if %i% gtr 10 goto n3
goto n1

:n2
echo yes>"./plan/need_%i%.txt"
echo yes>"./plan_use_exe/need_%i%.txt"
goto n1

:n3
exit