export LOG_FILE=start.gogs.sh.log

# MUST set this, to solve issie : [FATAL] [...g/setting/setting.go:591 NewContext()] Expect user 'MY_USER1' but current user is:
# either set in here, or set in crontab job
# e.g. 
# 0 8 * * * "$(command -v bash)" -c 'export USER=MY_USER1 ; gogs.bak.sh  1>gogs.bak.sh...1.log  2>gogs.bak.sh...2.log'
# 0 8 * * * export USER=MY_USER1 ; gogs.bak.sh  1>gogs.bak.sh...1.log  2>gogs.bak.sh...2.log

#export USER=MY_USER1


cd ~/gogs

echo '====================' >>  $LOG_FILE
echo '=== BEGIN ==========' >>  $LOG_FILE
echo '====================' >>  $LOG_FILE

echo '====================' >>  $LOG_FILE
date +'%Y%m%d_%H%M%S'       >>  $LOG_FILE
echo '====================' >>  $LOG_FILE

echo 'pwd'                  >>  $LOG_FILE
pwd                         >>  $LOG_FILE
echo '--------------------' >>  $LOG_FILE

echo 'whoami'               >>  $LOG_FILE
whoami                      >>  $LOG_FILE
echo '--------------------' >>  $LOG_FILE

./gogs web                  >>  $LOG_FILE

echo '--------------------' >>  $LOG_FILE


