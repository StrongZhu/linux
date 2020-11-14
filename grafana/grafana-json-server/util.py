#!/usr/bin/python
# -*- coding:utf-8 -*-

# --------------------------------------------
# --------------------------------------------
# --------------------------------------------
import sys
import os
# __file__ is this 'util.py' file
STARTUP_SCRIPT_FULLPATH = sys.argv[0]
STARTUP_SCRIPT_DIR = os.path.dirname(STARTUP_SCRIPT_FULLPATH)
STARTUP_SCRIPT_BASENAME = os.path.basename(STARTUP_SCRIPT_FULLPATH)


# --------------------------------------------
import datetime
import threading
import platform




# --------------------------------------------
def LogEx(_ex):
  Log('{0}'.format(_ex))
  pass

# --------------------------------------------
def Log(_s, _logToFileOnly=False, call_by_Log=True):
  if not _s:
    return

  # -------------------
  s2 = ''

  # -------------------
  # add timestamp
  dt_now = datetime.datetime.now()
  dt_now_str = dt_now.strftime('%Y-%m-%d %H:%M:%S.%f')

  # s2 += '{0:23} : '.format(str(dt_now)[:-3])
  s2 += '{0:23} : '.format(dt_now_str[:-3])

  # -------------------
  # add current thread id
  s2 += '{0:05} : '.format(threading.currentThread().ident)

  # -------------------
  # add caller name
  bAddCaller = True
  try:
    if bAddCaller:
      frame = sys._getframe(2)

      if not call_by_Log:
        frame = sys._getframe(1)
        pass

      caller_function_name = frame.f_code.co_name
      caller_filename = frame.f_code.co_filename
      s2 += '{0} : '.format(caller_function_name)
  except Exception as ex:
    my_traceback(ex)
    pass

  s2 += '{0}'.format(_s)

  # -------------------
  # log to console
  if not _logToFileOnly:
    print(s2)
    pass
  pass


# =====================================================
# =====================================================
# Windows-7-6.1.7601-SP1
# 'Linux-4.19.97-v7l+-armv7l-with-debian-10.3'
def isWindows():
  return 'windows' in str(platform.platform()).lower()
def isLinux():
  return 'linux' in str(platform.platform()).lower()



# =====================================================
# =====================================================


# =====================================================
# =====================================================


# =====================================================
# =====================================================

