# coding=utf-8


# ————————————————
# 版权声明：本文为CSDN博主「qq_39427552」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
# 原文链接：https://blog.csdn.net/qq_39427552/article/details/98224762

import random
import time
import psutil  #构建数据
from influxdb import InfluxDBClient

client_all = InfluxDBClient("localhost", "8086", "Tom", "", "")
DataBasename = "Tom"

# delete a database(table) from the client we connected, if
#   the client(Clientname) has a database named (Databasename): 
def DeletefromDB(Clientname, Databasename):
  database = Clientname.get_list_database()  # actually there's no need to check if Cn in database
  for Cn in database:
    if Databasename in Cn.values():
      Clientname.drop_database(Databasename)
      break

# returns a struct that contains a data item. 
def gen_item():
  data_list = [
    {
      'measurement': DataBasename,
      'tags': {
        'cpu': 'i7-7700HQ'
        },
      'fields':{
        'randnum':random.randint(1,100),
        'cpu-usage/%':psutil.cpu_percent(None),
        'memory-usage/%':psutil.virtual_memory().percent
        }
    }
  ]
  return data_list

def main():
    # create a database table named DataBasename:
    client_all.create_database(DataBasename)

    # connect to client and use the database "DataBasename"
    client = InfluxDBClient("localhost", "8086", "Tom", "", DataBasename)

    # query. this returns the result of "show measurements"
    # the string in ( ) can be changed into any instructions. 
    result = client.query('show measurements')

    # directly print the data (in string format)
    print("{0}".format(result))

    # write data in database:
    cnt = 0
    while cnt<100000:
      client.write_points(gen_item())
      cnt = cnt+1
      time.sleep(0.1)

    # query data and get results.
    result = client.query("select * from "+DataBasename+" where \"cpu-usage/%\">3")
    items = list(result.get_points())  # from iterator to list

    # itgt is short for 'item to get type'
    itgt = items[0]
    print(type(itgt['time']), type(itgt[u'cpu']), type(itgt[u'randnum']), type(itgt[u'cpu-usage/%']), type(itgt[u'memory-usage/%']))

    # print the items in the format we need:
    for item in items:
      print(item['time'], item[u'cpu'], item[u'randnum'], item[u'cpu-usage/%'], item[u'memory-usage/%'])
    
    # delete table from client 'client_all'.
    # DeletefromDB(client_all, DataBasename)
    print(client_all.get_list_database())

if __name__ == '__main__':

  # print the table names
  list1 = client_all.get_list_database()
  for db1 in list1:
    print('db1=[{0}]'.format(db1))
    pass
  
  main()
