@echo off
:: ����Ƿ�Ϊ����ԱȨ�ޣ��Զ���Ȩ
fltmc >nul 2>&1 || (
    :: �ǹ���Ա���Զ���Ȩ
    powershell -Command "Start-Process '%0' -Verb RunAs" >nul 2>&1
    exit /b
)

:: 1. �ָ���ʼ�˵�/ϵͳ�˵��ػ�
reg add "HKLM\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer" /v NoClose /t REG_DWORD /d 0 /f >nul 2>&1

:: 2. �ָ�Alt+F4�ػ�����
reg add "HKLM\Software\Microsoft\Windows\CurrentVersion\Policies\System" /v DisableCloseDialog /t REG_DWORD /d 0 /f >nul 2>&1

:: ˢ�²���
::taskkill /f /im explorer.exe >nul 2>&1
::start explorer.exe >nul 2>&1

exit