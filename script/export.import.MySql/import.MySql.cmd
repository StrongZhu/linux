@ECHO OFF

REM =====================================================
REM       'trading'       :   schema name

REM       -f              :   by force, i.e. ignore error, and go on 



REM =====================================================
SET MY_CMD="C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe"

SET HOST=localhost
SET PORT=3307

SET USER=zhuqiang
SET PW=zhuqiang

SET DATABASE=trading
REM SET TABLE=

SET MY_OPTION=-f
REM SET WHERE_OPTION=

SET INPUT_FILE_PATH=dump.result.sql




ECHO =====================================================
DATE /T && TIME /T
ECHO =====================================================
ECHO ==== WILL RUN BLOW CMD ==============================
ECHO =====================================================
ECHO %MY_CMD%    -h %HOST%    -P %PORT%   -u%USER%    -p%PW%    %DATABASE%   %MY_OPTION%      ^<  %INPUT_FILE_PATH%
ECHO =====================================================
     %MY_CMD%    -h %HOST%    -P %PORT%   -u%USER%    -p%PW%    %DATABASE%   %MY_OPTION%      <  %INPUT_FILE_PATH%
ECHO =====================================================
ECHO .
ECHO =====================================================
DATE /T && TIME /T
ECHO ==== DONE ===========================================



REM =====================================================
ECHO ON

