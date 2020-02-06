@ECHO OFF

REM =====================================================
REM       'trading'       :   schema name
REM       'md_last_kbar'  :   DB name

REM       --extended-insert=False : one 'INSERT' per line, DISABLE 'multiple-row INSERT syntax' that include several VALUES lists
REM       --skip-add-drop-table   : there is NO 'DROP TABLE' cmd, so we can import again and again.
REM       --where="open < 100"    : WHERE clause

REM       --insert-ignore         : use 'INSERT  IGNORE INTO', (ignore item if existed already), rather than 'INSERT  INTO' (raise error, if existed already)
REM       --replace               : Use 'REPLACE INTO' (delete + insert) instead of 'INSERT INTO'.



REM =====================================================
SET MY_CMD="C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqldump.exe"

SET HOST=localhost
SET PORT=3306

SET USER=zhuqiang
SET PW=zhuqiang

SET DATABASE=trading
SET TABLE=md_last_kbar

SET MY_OPTION=--extended-insert=False --skip-add-drop-table --replace
SET WHERE_OPTION=--where="open < 100"

SET OUTPUT_FILE_PATH=dump.result.sql



ECHO =====================================================
DATE /T && TIME /T
ECHO =====================================================
ECHO ==== WILL RUN BLOW CMD ==============================
ECHO =====================================================
ECHO %MY_CMD%    -h %HOST%    -P %PORT%   -u%USER%    -p%PW%    %DATABASE%  %TABLE%   %MY_OPTION%  %WHERE_OPTION%    ^> %OUTPUT_FILE_PATH%
ECHO =====================================================
     %MY_CMD%    -h %HOST%    -P %PORT%   -u%USER%    -p%PW%    %DATABASE%  %TABLE%   %MY_OPTION%  %WHERE_OPTION%     > %OUTPUT_FILE_PATH%
ECHO =====================================================
ECHO .
ECHO =====================================================
DATE /T && TIME /T
ECHO saved result to file 
ECHO      %OUTPUT_FILE_PATH%
ECHO ==== DONE ===========================================



REM =====================================================
ECHO ON
