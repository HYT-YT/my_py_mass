@echo off
:: ����Ƿ�Ϊ����ԱȨ�ޣ��Զ���Ȩ
fltmc >nul 2>&1 || (
    :: �ǹ���Ա���Զ���Ȩ
    powershell -Command "Start-Process '%0' -Verb RunAs" >nul 2>&1
    exit /b
)

:: 1. ���ÿ�ʼ�˵�/ϵͳ�˵��Ĺػ�ѡ��
reg add "HKLM\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer" /v NoClose /t REG_DWORD /d 1 /f >nul 2>&1

:: 2. ����Alt+F4�����Ĺػ��Ի���
reg add "HKLM\Software\Microsoft\Windows\CurrentVersion\Policies\System" /v DisableCloseDialog /t REG_DWORD /d 1 /f >nul 2>&1

:: ˢ�²��ԣ�������Ч
::taskkill /f /im explorer.exe >nul 2>&1
::start explorer.exe >nul 2>&1

exit