@echo off
:: 检测是否为管理员权限，自动升权
fltmc >nul 2>&1 || (
    :: 非管理员则自动升权
    powershell -Command "Start-Process '%0' -Verb RunAs" >nul 2>&1
    exit /b
)

:: 1. 禁用开始菜单/系统菜单的关机选项
reg add "HKLM\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer" /v NoClose /t REG_DWORD /d 1 /f >nul 2>&1

:: 2. 禁用Alt+F4弹出的关机对话框
reg add "HKLM\Software\Microsoft\Windows\CurrentVersion\Policies\System" /v DisableCloseDialog /t REG_DWORD /d 1 /f >nul 2>&1

:: 刷新策略，立即生效
::taskkill /f /im explorer.exe >nul 2>&1
::start explorer.exe >nul 2>&1

exit