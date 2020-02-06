@ECHO OFF



SET SERVICE_NAME=MySQL80_3307


ECHO ==== creating service [%SERVICE_NAME%] ...
sc create %SERVICE_NAME% binPath= "\"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqld.exe\" --defaults-file=\"c:\ProgramData\MySQL\MySQL Server 8.0\my.3307.ini\" %SERVICE_NAME%"
sc config %SERVICE_NAME% start=auto


ECHO 3...
ping 127.1 -n 2 >nul
ECHO 2...
ping 127.1 -n 2 >nul
ECHO 1...
ping 127.1 -n 2 >nul


ECHO ==== starting service [%SERVICE_NAME%] ...
sc start  %SERVICE_NAME%


ECHO 2...
ping 127.1 -n 2 >nul
ECHO 1...
ping 127.1 -n 2 >nul


ECHO ==== query config of service [%SERVICE_NAME%] ...
sc qc     %SERVICE_NAME%


ECHO ON

