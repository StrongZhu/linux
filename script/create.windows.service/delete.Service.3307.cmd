@ECHO OFF



SET SERVICE_NAME=MySQL80_3307


ECHO ==== stoping service [%SERVICE_NAME%] ...
sc stop  %SERVICE_NAME%


ECHO ==== deleteing service [%SERVICE_NAME%] ...
sc delete %SERVICE_NAME%


ECHO 3...
ping 127.1 -n 2 >nul
ECHO 2...
ping 127.1 -n 2 >nul
ECHO 1...
ping 127.1 -n 2 >nul


ECHO ==== query config of service [%SERVICE_NAME%] ...
sc qc     %SERVICE_NAME%


ECHO ON

