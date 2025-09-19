@echo off
:: 检测是否为管理员权限，自动升权
fltmc >nul 2>&1 || (
    :: 非管理员则自动升权
    powershell -Command "Start-Process '%0' -Verb RunAs" >nul 2>&1
    exit /b
)

:: 1. 恢复开始菜单/系统菜单关机
reg add "HKLM\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer" /v NoClose /t REG_DWORD /d 0 /f >nul 2>&1

:: 2. 恢复Alt+F4关机功能
reg add "HKLM\Software\Microsoft\Windows\CurrentVersion\Policies\System" /v DisableCloseDialog /t REG_DWORD /d 0 /f >nul 2>&1

:: 刷新策略
::taskkill /f /im explorer.exe >nul 2>&1
::start explorer.exe >nul 2>&1

exit