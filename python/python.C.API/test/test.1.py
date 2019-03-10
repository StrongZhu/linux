#!/usr/bin/env python

import sys
import os
import time
import threading

# ---------------------------------------------------------------------------------
SCRIPT_FULLPATH = __file__
SCRIPT_DIR      = os.path.dirname(__file__)
SCRIPT_FILENAME = os.path.basename(__file__)

output_mutex = threading.Lock()

if True:
#if False:
  print 'SCRIPT_FULLPATH  : {0}'.format(SCRIPT_FULLPATH)
  print 'SCRIPT_DIR       : {0}'.format(SCRIPT_DIR)
  print 'SCRIPT_FILENAME  : {0}'.format(SCRIPT_FILENAME)
  pass

sys.path.append(SCRIPT_DIR + '/../build/lib.linux-x86_64-2.7/')
import foo

# ---------------------------------------------------------------------------------
def session_status_CB(_status):
  pass

def subscribe_cb(_long1, _str1, _str2):
  output_mutex.acquire()
  print 'subscribe_cb : _long1=[{0:20}], _str1=[{1:10}], _str2=[{2}]'.format(_long1, _str1, _str2)
  output_mutex.release()
  pass

def func_cb3(_int1, _double2, _string3):
  pass

def func_cb4(_int1, _double2, _string3):
  pass

# ---------------------------------------------------------------------------------
foo.bar()

foo.bar3(1)
foo.bar3(1,d=2.0)
foo.bar3(i=1,d=2.0)


# ---------------------------------------------------------------------------------
# open
session_ptr = foo.open_session(1, 2.2, 'strnig3', session_status_CB)
print 'open_session : got session_ptr=[{0}]=[{0:08X}]'.format(session_ptr)

# ---------------------------------------------------------------------------------
# subscribe
sub_id_dict = {}
for i in range(1,10):
  topic = "topic_{0}".format(i)
  sub_id = foo.subscribe(session_ptr, topic, subscribe_cb)

  print 'subscribe : i=[{0}], topic=[{1}], sub_id=[{2}]'.format(i, topic, sub_id)

  # save to dict
  sub_id_dict[i] = sub_id

  pass

# ---------------------------------------------------------------------------------
# sleep
time.sleep(5)

# ---------------------------------------------------------------------------------
# un-subscribe some
for i in range(1,10, 2):
  print i
  result = foo.unsubscribe(session_ptr, sub_id_dict[i])
  sub_id_dict[i]
  print 'unsubscribe : i=[{0}], result=[{1}], sub_id=[{2}]'.format(i, result, sub_id_dict[i])
  del sub_id_dict[i]
  pass

# ---------------------------------------------------------------------------------
# sleep
time.sleep(5)

# ---------------------------------------------------------------------------------
# request
for req in [ 'request_1', 'request_2', ]:
  result = foo.request(session_ptr, req)
  print 'request : req=[{0}], result=[{1}]'.format(req, result)
  pass

# ---------------------------------------------------------------------------------
# close
session_ptr = foo.close_session(session_ptr)





# ---------------------------------------------------------------------------------
print 'DONE'

