# -*- coding: utf-8 -*-
#!/usr/bin/python

# ============================================================
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(os.path.dirname(os.path.abspath(__file__)) + os.sep + '..' + os.sep + 'lib')

# ============================================================

import json
import time
import csv
import os

from flask import Flask
from flask import render_template
from flask import request

from flask_cors import CORS

import datetime
# import argparse
import subprocess
import re 
import pprint

# ============================================================
import util



# ============================================================
app = Flask(__name__)
CORS(app)

html_BR = '<BR>'


# ============================================================
def sep___________________________________000():
  pass

# ============================================================
def DUMP_request(request, dump_environ=False):
  # -----------------------------------------------------
  #
  # for 'POST' + 'NO serverSide'
  # all below dict are EMPTY, and there is no epoch at all
  r1 = request.args
  r2 = request.form
  r3 = request.files

  r4 = request.data
  r5 = request.get_json()

  if dump_environ:
    util.Log('========= request.environ ===================')
    for key in sorted(request.environ.keys()):
      # focus on some keys
      if key not in [
        'HTTP_HOST',
        'HTTP_REFERER',
        'PATH_INFO',
        'QUERY_STRING',
        'RAW_URI',
        'REMOTE_ADDR',
        'REMOTE_PORT',
        'REQUEST_METHOD',
        'REQUEST_URI',
        'SERVER_NAME',
        'SERVER_PORT',
      ]:
        continue
      util.Log('request.environ  : [{0:40}]=[{1:10}]'.format(key, request.environ[key]))
      pass
    pass

  if request.args: util.Log('========= request.args ===================')
  for key in sorted(request.args.keys()):
    util.Log('request.args  : [{0:40}]=[{1:10}]'.format(key, request.args[key]))
    pass

  if request.form: util.Log('========= request.form ===================')
  for key in sorted(request.form.keys()):
    # util.Log('request.form  : [{0:40}]=[{1:10}]'.format(key, request.form[key]))

    # show as json string
    util.Log('request.form  : [{0:40}]=[{1:10}]'.format(key, json.dumps(request.form[key])))
    pass

  if request.data: util.Log('========= request.data===================')
  util.Log('request.data  : [{}]'.format(request.data))

  if request.files: util.Log('========= request.files===================')
  for key in sorted(request.files.keys()):
    util.Log('request.files : [{0:40}]=[{1:10}]'.format(key, request.files[key]))
    pass

  request_dict = request.get_json()
  if request_dict:
    util.Log('========= request.get_json()===================')
    s2 = pprint.pformat(request_dict)
    util.Log(s2)

    # for key in sorted(request_dict.keys()):
    #   util.Log('request_dict : [{0:40}]=[{1:10}]'.format(key, request_dict[key]))
    #   pass
    # pass

  util.Log('==========================================')

  pass

# ============================================================
# run shell cmd, sync
# get stdout, stderr
def run_shell_cmd_sync(_cmd_and_param_list=[]):
  result_stdout_list1 = []
  result_stderr_list1 = []

  try:
    p = subprocess.Popen(_cmd_and_param_list, 
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE,
                            )
    out, err = p.communicate()

    # util.Log('out=[{}]'.format(out))
    # util.Log('err=[{}]'.format(err))

    result_stdout_list1 = re.split('\r|\n', out) 
    result_stderr_list1 = re.split('\r|\n', err) 

    pass
  except Exception as ex:
    util.Log(ex)
    pass

  return (result_stdout_list1, result_stderr_list1,)
  pass

# ============================================================
# convert out, err list to html
def out_err_2_html(_out_list=[], _err_list=[], _cmd_list=[], _obj1=None):

  # -------------------
  s1 = ''

  # -------------------
  if _cmd_list:
    s1 += '<HR>'
    s1 += '<H3>cmd list</H3>' + html_BR 
    s1 += '<PRE>'
    for s_tmp1 in _cmd_list:
      s1 += '{}'.format(s_tmp1 ) + html_BR
      pass
    s1 += '</PRE>'
    pass

  # -------------------
  if _obj1:
    try:
      s1 += '<HR>'
      s1 += '<H3>obj1</H3>' + html_BR 
      s1 += '<PRE>'
      s2 = pprint.pformat(_obj1)
      s1 += s2
      s1 += '</PRE>'
      pass
    except:
      pass

  # -------------------
  if _out_list:
    s1 += '<HR>'
    s1 += '<H3>stdout</H3>' + html_BR 
    s1 += '<PRE>'
    for s_tmp1 in _out_list:
      s1 += '{}'.format(s_tmp1 ) + html_BR
      pass
    s1 += '</PRE>'

  # -------------------
  if _err_list:
    s1 += '<HR>'
    s1 += '<H3>stderr</H3>' + html_BR 
    s1 += '<PRE>'
    for s_tmp1 in _err_list:
      s1 += '{}'.format(s_tmp1 ) + html_BR
      pass
    s1 += '</PRE>'



  # -------------------
  if s1:
    s1 += '<HR>'
    pass

  return s1


# ============================================================
def sep___________________________________100():
  pass

# ============================================================
@app.route('/')
def index():
  return ''

# ============================================================
def sep___________________________________200():
  pass

# ============================================================
@app.route('/search', methods=['GET', 'POST'])
def search():
  # DUMP_request(request)

  result_obj = [
    'systemctl_service',
    'metric_upper_50',
    'metric_upper_95',
  ]

  # !!! value will be in request of '/query'
  XXX___result_obj = [
    {
      'text': 'metric_upper_25',
      'value': 100,
    },
    {
      'text': 'metric_upper_75',
      'value': 200,
    },
    {
      'text': 'systemctl_service',
      'value': 1000,
    },
  ]

  # return json string
  result_dict_json_str = json.dumps(result_obj)
  return result_dict_json_str


# ============================================================
def sep___________________________________300():
  pass

# ============================================================
@app.route('/query', methods=['GET', 'POST'])
def query():
  try:
    # # ------------
    # DUMP_request(request)

    # ------------
    while True:
      # ------------
      request_dict1 = request.get_json()

      request_dict1.setdefault('targets', [])

      # ------------
      targets_list = request_dict1['targets']
      if False:
        util.Log('========= targets_list =============')
        s2 = pprint.pformat(targets_list)
        util.Log(s2)
        util.Log('====================================')
        pass

      if not targets_list:
        break

      # ------------
      # focus on the 1st list only
      target_dict1 = targets_list[0]
      if False:
        util.Log('target=[{}]'.format(target_dict1))
        pass
      # e.g.
      # target=[{'hide': False, 'type': 'table',      'data': None, 'target': 'systemctl_service', 'refId': 'A'}]
      # target=[{'hide': False, 'type': 'timeseries', 'data': None, 'target': 'systemctl_service', 'refId': 'A'}]

      # ------------
      target_dict1.setdefault('type', '')
      target_dict1.setdefault('target', '')

      type1 = target_dict1['type']
      target1 = target_dict1['target']
      # util.Log('target_dict1=[{}]'.format(pprint.pprint(target_dict1)))

      if not type1:
        break

      # ------------
      if type1 == 'timeseries':
        # ------------
        # for now, ignore all timeseries
        pass
      elif type1 == 'table':
        # ------------
        # it's table
        pass
      else:
        # ------------
        # invalid...
        util.Log('invalid type1=[{}]'.format(type1))
        pass

      # ------------
      if target1 == 'systemctl_service':
        # ------------
        return query_systemctl_service()
        pass
      else:
        # ------------
        pass

      pass

      # ------------
      # always break
      break
      pass

    pass
  except:
    pass

  # ------------
  # set to empty
  result_obj = []

  # return json string
  result_dict_json_str = json.dumps(result_obj)
  return result_dict_json_str


# ============================================================
def query___test1():

  result_obj = [
    {
      'columns': [
        { 'text': 'Time', 'type': 'time'},
        {'text': 'Country', 'type': 'string'},
        {'text': 'Number', 'type': 'number'},
        {'text': 'Start', 'type': 'number'},
        {'text': 'Stop', 'type': 'number'},
        {'text': 'Restart', 'type': 'number'},
        {'text': 'Status', 'type': 'number'},
      ],
      'rows': [
        [ 1234567, 'SE', 111, 'Start', 'Stop', 'Restart', 'Status'],
        [ 1234567, 'DE', 222, 'Start', 'Stop', 'Restart', 'Status'],
        [ 1234567, 'US', 333, 'Start', 'Stop', 'Restart', 'Status'],
      ],
      'type': 'table',
    },
  ]
  # return json string
  result_dict_json_str = json.dumps(result_obj)
  return result_dict_json_str

# ============================================================
def query_systemctl_service():

  result_obj = []

  columns_list = [
    {'text': 'svcName', 'type': 'string'},
    {'text': 'LOAD', 'type': 'string'},
    {'text': 'ACTIVE', 'type': 'string'},
    {'text': 'SUB', 'type': 'string'},
    {'text': 'DESCRIPTION', 'type': 'string'},

    {'text': 'Start', 'type': 'string'},
    {'text': 'Stop', 'type': 'string'},
    {'text': 'Restart', 'type': 'string'},
    {'text': 'Status', 'type': 'string'},
  ]

  # for testing
  if False:
    result_obj = [
      {
        'columns': [
          { 'text': 'Time', 'type': 'time'},
          {'text': 'Country', 'type': 'string'},
          {'text': 'Number', 'type': 'number'},
          {'text': 'Start', 'type': 'number'},
          {'text': 'Stop', 'type': 'number'},
          {'text': 'Restart', 'type': 'number'},
          {'text': 'Status', 'type': 'number'},
        ],
        'rows': [
          [ 1234567, 'SE', 123, 'Start', 'Stop', 'Restart', 'Status'],
          [ 1234567, 'DE', 231, 'Start', 'Stop', 'Restart', 'Status'],
          [ 1234567, 'US', 321, 'Start', 'Stop', 'Restart', 'Status'],
        ],
        'type': 'table',
      },
    ]
    # return json string
    result_dict_json_str = json.dumps(result_obj)
    return result_dict_json_str

  services_dict = {}

  if util.isLinux():
    services_dict = get_systemctl_service()
    pass

  # for testing
  if util.isWindows():
    services_dict = {
      'alsa-restore': {'ACTIVE': 'active',
                       'DESCRIPTION': 'Save/Restore Sound Card State',
                       'LOAD': 'loaded',
                       'SUB': 'running',
                       'SvcName': 'alsa-restore'},
      'alsa-state': {'ACTIVE': 'active',
                     'DESCRIPTION': 'Manage Sound Card State (restore and store)',
                     'LOAD': 'loaded',
                     'SUB': 'running',
                     'SvcName': 'alsa-state'},
      'apparmor': {'ACTIVE': 'inactive',
                   'DESCRIPTION': 'Load AppArmor profiles',
                   'LOAD': 'loaded',
                   'SUB': 'running',
                   'SvcName': 'apparmor'},

    }
    pass

  # util.Log('services=[{}]'.format(pprint.pprint(services_dict)))

  rows_list1 = []

  extra_list = [
    'Start',
    'Stop',
    'Restart',
    'Status',
  ]

  for svcName in sorted(services_dict.keys()):
    try:
      # UNIT = ''
      LOAD = ''
      ACTIVE = ''
      SUB = ''
      DESCRIPTION = ''
      try: LOAD = services_dict[svcName]['LOAD']
      except: pass
      try: ACTIVE = services_dict[svcName]['ACTIVE']
      except: pass
      try: SUB = services_dict[svcName]['SUB']
      except: pass
      try: DESCRIPTION = services_dict[svcName]['DESCRIPTION']
      except: pass

      if not svcName:
        continue

      list1 = [
        svcName,
        LOAD,
        ACTIVE,
        SUB,
        DESCRIPTION,
      ]

      rows_list1.append(list1 + extra_list)
      pass
    except:
      pass
    pass

  result_obj = [
    {
      'columns': columns_list,
      'rows': rows_list1,
      'type': 'table',
    }
  ]

  # return json string
  result_dict_json_str = json.dumps(result_obj)
  return result_dict_json_str


# ============================================================
def sep___________________________________350():
  pass



# ============================================================
@app.route('/tag-keys', methods=['GET', 'POST'])
def tag_keys():
  try:
    # ------------
    DUMP_request(request)

    # ------------
    pass
  except:
    pass

  # ------------
  result_obj = [
    {"type": "string", "text": "City"},
    {"type": "string", "text": "Country"}
  ]

  # return json string
  result_dict_json_str = json.dumps(result_obj)
  return result_dict_json_str


# ============================================================
@app.route('/tag-values', methods=['GET', 'POST'])
def tag_values():
  try:
    # ------------
    DUMP_request(request)

    # ------------
    pass
  except:
    pass

  # ------------
  result_obj = [
    {"text": "Eins!"},
    {"text": "Zwei"},
    {"text": "Drei!"}
  ]

  # return json string
  result_dict_json_str = json.dumps(result_obj)
  return result_dict_json_str




# ============================================================
def sep___________________________________400():
  pass


# ============================================================
# call cmd : systemctl --type=service --all --plain
# return dict
# e.g.
# {
#   'alsa-restore': {'ACTIVE': 'active',
#                   'DESCRIPTION': 'Save/Restore Sound Card State',
#                   'LOAD': 'loaded',
#                   'SUB': 'exited',
#                   'SvcName': 'alsa-restore'},
#  'alsa-state': {'ACTIVE': 'active',
#                 'DESCRIPTION': 'Manage Sound Card State (restore and store)',
#                 'LOAD': 'loaded',
#                 'SUB': 'running',
#                 'SvcName': 'alsa-state'},
#
def get_systemctl_service():

  result_obj = None

  cmd1 = 'systemctl --type=service --all --plain'
  cmd_list_1 = cmd1.split(' ')

  out, err = run_shell_cmd_sync(cmd_list_1 )

  # # for testing
  # out = out[:7]

  # e.g.
  # split !!! by length !!!
  '''
  UNIT                                                        LOAD      ACTIVE   SUB     DESCRIPTION
  alsa-restore.service                                        loaded    active   exited  Save/Restore Sound Card State
  alsa-state.service                                          loaded    active   running Manage Sound Card State (restore and store)
  '''

  svcName_2_info_dict___list = {}
  for row_s1 in out:
    try:
      service_name = ''
      dict_tmp1 = {}
      service_name = str(row_s1[:62]).strip(' \t')

      postfix_s1 = '.service'
      if not service_name.endswith(postfix_s1):
        # skip it
        continue
        pass
      # e.g. 'grafana-server.service'
      service_name = service_name[:-len(postfix_s1)]
      dict_tmp1['SvcName'] = service_name

      dict_tmp1['LOAD'] = ''
      dict_tmp1['ACTIVE'] = ''
      dict_tmp1['SUB'] = ''
      dict_tmp1['DESCRIPTION'] = ''

      try: dict_tmp1['LOAD'] = str(row_s1[62:72]).strip(' \t')
      except: pass
      try: dict_tmp1['ACTIVE'] = str(row_s1[72:81]).strip(' \t')
      except: pass
      try: dict_tmp1['SUB'] = str(row_s1[81:89]).strip(' \t')
      except: pass
      try: dict_tmp1['DESCRIPTION'] = str(row_s1[89:]).strip(' \t')
      except: pass

      # util.Log('dict_tmp1={0}'.format(dict_tmp1))

      if service_name:
        svcName_2_info_dict___list[service_name] = dict_tmp1
        pass
      pass
    except:
      pass
    pass

  return svcName_2_info_dict___list




# ============================================================
def sep___________________________________500():
  pass


# ============================================================
def sep___________________________________600():
  pass

# ============================================================
def api_test(request):

  return;

  # -----------------------------------------------------
  #
  # for 'POST' + 'NO serverSide'
  # all below dict are EMPTY, and there is no epoch at all
  r1 = request.args
  r2 = request.form
  r3 = request.files

  util.Log('========= request.args ===================')
  for key in sorted(request.args.keys()):
    util.Log('request.args  : [{0:40}]=[{1:10}]'.format(key, request.args[key]))
    pass
  util.Log('========= request.form ===================')

  for key in sorted(request.form.keys()):
    util.Log('request.form  : [{0:40}]=[{1:10}]'.format(key, request.form[key]))
    pass

  util.Log('========= request.files===================')
  for key in sorted(request.files.keys()):
    util.Log('request.files : [{0:40}]=[{1:10}]'.format(key, request.files[key]))
    pass
  util.Log('==========================================')
  pass

  # -----------------------------------------------------
  # -----------------------------------------------------
  # -----------------------------------------------------
  #
  # sample data for 'serverSide + POST'
  # reference : https://datatables.net/manual/server-side
  #
  # ==========================================
  # request.form  : [draw                                    ]=[5         ]   # Draw counter
  # request.form  : [start                                   ]=[0         ]   # Paging first record indicator.
  # request.form  : [length                                  ]=[10        ]   # Number of records that the table can display in the current draw.
  # request.form  : [search[regex]                           ]=[false     ]   # true if the global filter should be treated as a regular expression for advanced searching,
  # request.form  : [search[value]                           ]=[deb       ]   # Global search value. e.g. search for 'deb
  #
  # request.form  : [order[0][column]                        ]=[3         ]   # Column to which ordering should be applied.
  # request.form  : [order[0][dir]                           ]=[desc      ]
  #
  # request.form  : [columns[0][data]                        ]=[0         ]
  # request.form  : [columns[0][name]                        ]=[          ]
  # request.form  : [columns[0][orderable]                   ]=[true      ]
  # request.form  : [columns[0][search][regex]               ]=[false     ]
  # request.form  : [columns[0][search][value]               ]=[          ]
  # request.form  : [columns[0][searchable]                  ]=[true      ]

  # request.form  : [columns[1][data]                        ]=[1         ]
  # request.form  : [columns[1][name]                        ]=[          ]
  # request.form  : [columns[1][orderable]                   ]=[true      ]
  # request.form  : [columns[1][search][regex]               ]=[false     ]
  # request.form  : [columns[1][search][value]               ]=[          ]
  # request.form  : [columns[1][searchable]                  ]=[true      ]

  # request.form  : [columns[2][data]                        ]=[2         ]
  # request.form  : [columns[2][name]                        ]=[          ]
  # request.form  : [columns[2][orderable]                   ]=[true      ]
  # request.form  : [columns[2][search][regex]               ]=[false     ]
  # request.form  : [columns[2][search][value]               ]=[          ]
  # request.form  : [columns[2][searchable]                  ]=[true      ]

  # request.form  : [columns[3][data]                        ]=[3         ]
  # request.form  : [columns[3][name]                        ]=[          ]
  # request.form  : [columns[3][orderable]                   ]=[true      ]
  # request.form  : [columns[3][search][regex]               ]=[false     ]
  # request.form  : [columns[3][search][value]               ]=[          ]
  # request.form  : [columns[3][searchable]                  ]=[true      ]

  # ==========================================


  return 'api_test'
  pass


# ============================================================
def sep___________________________________700():
  pass

# ============================================================
def sep___________________________________800():
  pass

# ============================================================
def main():
  try:
    # # ------------------------------------
    # parseArg()

    # ------------------------------------
    # web_init()

    # ------------------------------------
    # get parameters
    host1 = '0.0.0.0'
    # port1 = 5000
    port1 = 3003
    debug1 = None
    debug1 = 1
    
    if debug1:
      app.config['TEMPLATES_AUTO_RELOAD'] = True
      pass

    # ------------------------------------
    app.run(host=host1, port=port1, debug=debug1, threaded=True)

    pass
  except Exception as ex:
    util.LogEx(ex)
    pass
  pass


  pass

# ============================================================
# start from here
if __name__ == '__main__':
  main()

  pass
