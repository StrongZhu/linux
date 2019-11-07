#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------

import os
import sys

SCRIPT_NAME = __file__
SCRIPT_REAL_PATH = os.path.realpath(SCRIPT_NAME)
SCRIPT_DIR = os.path.dirname(SCRIPT_REAL_PATH)
# prgint SCRIPT_NAME
# print SCRIPT_REAL_PATH
# print SCRIPT_DIR

sys.path.append(SCRIPT_DIR + os.sep + 'lib')

# ------------------------------------
'''
cat xxx | fixcut -r tag1 tag2
'''
# ------------------------------------
import time
import datetime


import re



# ===================================

# tag -> re of tag
g_tag_dict = {}

TAG_PAIR_SEP = ';'
TAG_VAL_SEP = '='


def processOneLine(_line):
  global g_tag_dict

  try:
    _line = _line.strip()

    if not _line:
      return

    # print '=================== _line=[{0}]'.format(_line)

    s_out = ''


    tag_pair_list = _line.split(TAG_PAIR_SEP)

    b_is_the_1st_pair = True

    for tag_val in tag_pair_list:

      # TODO : refine the 1st tag-val pair later
      if b_is_the_1st_pair:
        s_out += '{0}{1}'.format(tag_val, TAG_PAIR_SEP)
        b_is_the_1st_pair = False
        continue

      arr1 = tag_val.split(TAG_VAL_SEP)
      if len(arr1) < 2 :
        continue

      tag = arr1[0].strip()
      val = arr1[1].strip()

      # # match tag by string
      # if tag in g_tag_dict:
      #   s_out += '{0}{1}{2}{3}'.format(tag, TAG_VAL_SEP, val, TAG_PAIR_SEP)
      #   pass
      #
      # match tag with RE
      for tag_tmp in g_tag_dict.keys():
        try:
          pattern_tmp = g_tag_dict[tag_tmp]
          result = re.match(pattern_tmp, tag)
          if result:
            # found it
            s_out += '{0}{1}{2}{3}'.format(tag, TAG_VAL_SEP, val, TAG_PAIR_SEP)
            break
          pass
        except:
          pass


      pass

    if s_out:
      print(s_out)

    return


    match = g_pattern.match(_line)
    if not match:
      return

    pass
  except Exception as ex:
    print(ex)
    print('==== EXCEPTION : {0}'.format(_line))
  pass


import sys, getopt
# ===================================
def Usage():
  print '''
    {0}     -r tag1[,tag2,tag3 ...]    [-h]
      -r      : cut tag list      support regular expression

      -h      : help


    e.g.
    {0}   -r tag1
    {0}   -r tag1,tag2,tag3



  '''.format(sys.argv[0])
  sys.exit(2)
  pass

# ===================================
def getOpt():

  global g_tag_dict

  try:
    opts, args = getopt.getopt(sys.argv[1:], "hr:")
  except getopt.GetoptError:
    Usage()
    pass

  for opt, arg in opts:
    if opt == '-h':
      Usage()
      pass
    elif opt in ('-r', '-r'):
      tag_list = arg
      for tag in tag_list.split(','):
        tag2 = tag.strip()
        if not tag2:
          continue

        g_tag_dict[tag2] = re.compile(tag2, re.IGNORECASE)

        pass

    else:
      # ignore it
      pass
    pass

  # --------------------------
  # verify parameters
  if len(g_tag_dict) <= 0:
    print('ERROR : MUST provide tag')
    Usage()
    return

  # --------------------------
  # dump parameters
  s1 = ''
  for tag in sorted(g_tag_dict.keys()):
    s1 += '[{0}], '.format(tag)
    pass

  # print '''
  #
  # tag list :  {0}
  #
  # '''.format(s1)

  pass



# ===================================
def main():
  # ----------------------------
  getOpt()


  # # ----------------------------
  # # test
  # lines = '''
# 2018-04-27 04:54:38.789489 (TD=16) : RDMClientLib.Decoder::EndRespMsg : Sym=FGBLM8  , rcvTime=2018-04-27 04:54:38.789489, GMT=2018-04-27 08:54:38.789489, b_Skip_bad_price=N, trade : ;TRDPRC_1=158.69;TRDVOL_1=2;TRDTIM_1=08:54:00:000:000:000;NUM_MOVES=13448;SEQNUM=322772;TRADE_DATE=27 APR 2018;ACTIV_DATE=27 APR 2018;TRDTIM_MS=32065329;TRDTIM_MS2=08:54:25.329;prevValue : ;TRADE_DATE=27 APR 2018;ACTIV_DATE=27 APR 2018;
# 2018-04-27 04:54:39.134777 (TD=16) : RDMClientLib.Decoder::EndRespMsg : Sym=FGBLM8  , rcvTime=2018-04-27 04:54:39.134777, GMT=2018-04-27 08:54:39.134777, b_Skip_bad_price=N, trade : ;TRDPRC_1=158.68;TRDVOL_1=100;TRDTIM_1=08:54:00:000:000:000;NUM_MOVES=13449;SEQNUM=322779;TRADE_DATE=;ACTIV_DATE=;TRDTIM_MS=32079080;TRDTIM_MS2=08:54:39.080;prevValue : ;TRADE_DATE=27 APR 2018;ACTIV_DATE=27 APR 2018;
# 2018-04-27 04:54:39.135778 (TD=16) : RDMClientLib.Decoder::EndRespMsg : Sym=FGBLM8  , rcvTime=2018-04-27 04:54:39.135778, GMT=2018-04-27 08:54:39.135778, b_Skip_bad_price=N, trade : ;TRDPRC_1=158.68;TRDVOL_1=6;TRDTIM_1=08:54:00:000:000:000;NUM_MOVES=13450;SEQNUM=322780;TRADE_DATE=;ACTIV_DATE=;TRDTIM_MS=32079080;TRDTIM_MS2=08:54:39.080;prevValue : ;TRADE_DATE=27 APR 2018;ACTIV_DATE=27 APR 2018;
#   '''

#   for line in lines.split('\n'):
#     processOneLine(line)

#   return

  # ----------------------------
  # process stdin
  for line in sys.stdin:
    processOneLine(line)

  # ----------------------------

  pass

# ===================================
# start from here
main()
pass
