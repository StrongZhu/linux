#!/bin/bash

# backup file/dir smartly
#   can call this script every N minutes during the day
#   for the first time, backup ALL files
#   then backup 'changed' files only.
#

# -------------
# variables
# DATE and 'DATE_TIME'
export DATE=`date +%Y%m%d`
export DATETIME=`date +%Y%m%d.%H%M%S.%N`

export "
===================================================
===================================================
===================================================
started $0 at $DATETIME
===================================================
===================================================
===================================================
"

export FLAG_FIRST_TIME=

export BACKUP_DIR_FIRST_TIME=
export BACKUP_DIR_THIS_TIME=
export PWD_TMP=`pwd`

# -------------
# usage
function usage() {
  echo "
  Usage :


    # back all files/dirs to DEST_DIR
    `basename $0`      DEST_DIR  dir1 dir2 ...
                  # DEST_DIR          :   save result to DEST_DIR
                  # dir1 dir2         :   backup dir1, dir2, ...

    # zip all files, run it by the end of the day
    `basename $0`      ZIP  DEST_DIR

    # the DEST_DIR is like :
        DEST_DIR/yyyymmdd/                      <-- more files are in here
        DEST_DIR/yyyymmdd/yyyymmdd.hhmmss           save timestamp in this file

        DEST_DIR/yyyymmdd.hhmmss.nnnnnnnnn/     <-- copy all stuff to this folder, then removed un-changed file
        DEST_DIR/yyyymmdd.hhmmss.nnnnnnnnn/         keep symbolic links (as they are of small size)
        DEST_DIR/yyyymmdd.hhmmss.nnnnnnnnn/
        ......

    # will ALL folder to
        DEST_DIR/yyyymmdd.tar.gz

"
  exit 1
}

# -------------
# run command
function runCmd() {
#  echo $*
  eval $*
}

# -------------
# compareTwoFiles
function compareTwoFiles() {
  # echo compareTwoFiles : [$*]
  if [[ $# -ne 2 ]];then
    echo "ERROR : compareTwoFiles need 2 parameter"
    return
  fi
  export FILE1=$1
  export FILE2=$2

  # ls -al $FILE1 $FILE2

  if [ ! -f $FILE1 ]; then
    echo "$FILE1 is NOT FILE"
    continue
  fi
  if [ ! -f $FILE2 ]; then
    echo "$FILE2 is NOT FILE"
    continue
  fi

  diff -q $FILE1 $FILE2 # > /dev/null 2>&1
  DIFF_RESULT=$?
  # echo DIFF_RESULT=$DIFF_RESULT
  if [ $DIFF_RESULT == 0 ] ; then
    # remove file, because it's of the same
    # echo "will remove ../$DATETIME/$line"
    runCmd rm -fr $FILE2
  fi
}


# -------------
# removeDuplicated, !! will change PWD_TMP !!!
function removeDuplicated() {
  # echo removeDuplicated : [$*]
  if [[ $# -ne 2 ]];then
    echo "ERROR : removeDuplicated need 2 parameter"
    return
  fi

  export  DIR_FIRST_TIME=$1
  export  DIR_THIS_TIME=$2

#  echo " removeDuplicated
#      DIR_FIRST_TIME = $DIR_FIRST_TIME
#      DIR_THIS_TIME  = $DIR_THIS_TIME
#
#    will remove files/dir/symbolic in [$DIR_THIS_TIME], if it's the same
#"

  # echo PWD_TMP=$PWD_TMP

  cd $DIR_THIS_TIME
  # echo "changed to $DIR_THIS_TIME, now, pwd=`pwd`"

  find . -type f | while read line
  do
    # echo "checking file [$line]"
    compareTwoFiles ../$DATE/$line ../$DATETIME/$line   # > /dev/null 2>&1
  done

  # echo PWD_TMP=$PWD_TMP
  cd $PWD_TMP
  echo "changed back to pwd=`pwd`"

  # remove empty folder
  find $DIR_THIS_TIME -type d | sort -r | while read line
  do
    rmdir $line > /dev/null 2>&1
  done
}

# -------------
# check paramemter
if [[ $# -lt 2 ]];then
  usage
  exit
fi

# -------------
# zip file
if [ "$1" == "ZIP" ] ; then
  export DEST_DIR=$2
  export DEST_ZIP_FILE=$DEST_DIR/$DATE.tar.gz
  runCmd rm -fr $DEST_ZIP_FILE
  runCmd tar zcf $DEST_ZIP_FILE       $DEST_DIR/$DATE/      $DEST_DIR/$DATE.[0-9][0-9][0-9][0-9][0-9][0-9].*/

  echo "ZIP $DEST_DIR/ to $DEST_DIR/$DATE.tar.gz"
  runCmd ls -al $DEST_DIR/$DATE.tar.gz

  # exit...
  exit
fi

# read parameters...
export DEST_DIR=$1
shift

export SOURCE_FILE_DIR=$*
mkdir -p $DEST_DIR

echo "
will backup files/dirs to
  DEST_DIR      =   [$DEST_DIR]
  DATE          =   $DATE
  DATETIME      =   $DATETIME
"


# -------------
# is it the 1st time to backup?
export BACKUP_DIR_FIRST_TIME=$DEST_DIR/$DATE
export BACKUP_DIR_THIS_TIME=$DEST_DIR/$DATETIME

if [ -d "$BACKUP_DIR_FIRST_TIME" ] ;then
  export FLAG_FIRST_TIME=

  echo "it's NOT the FIRST time to backup, for today...

  mkdir $BACKUP_DIR_THIS_TIME

"
  runCmd mkdir -p $BACKUP_DIR_THIS_TIME
else
  export FLAG_FIRST_TIME=1
  echo "it's the FIRST time to backup, for today...

  mkdir $BACKUP_DIR_FIRST_TIME
"
  runCmd mkdir -p $BACKUP_DIR_FIRST_TIME
  # save timestampl
  runCmd "echo > $BACKUP_DIR_FIRST_TIME/$DATETIME.txt"
fi

# -------------
# process file/dir
for i in $SOURCE_FILE_DIR
do
  if [ ! -d "$i" ] ;then
    echo "it's NOT dir [$i], ignore it..."
    continue
  fi

  echo "======================================================================"
  # echo PWD_TMP=`pwd`
  echo "processing -----[$i]-----"

  if [ "$FLAG_FIRST_TIME" == "" ]
  then
    # echo "NOT 1st time for $i"
    # copy, then remove duplicated
    runCmd cp -fr $i $BACKUP_DIR_THIS_TIME/

    removeDuplicated $BACKUP_DIR_FIRST_TIME  $BACKUP_DIR_THIS_TIME
  else
    # echo "1st time for $i"
    # copy directoy
    runCmd cp -fr $i $BACKUP_DIR_FIRST_TIME/
  fi

  echo

done

