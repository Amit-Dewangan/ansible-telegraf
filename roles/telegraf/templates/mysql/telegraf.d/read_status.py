import pymysql
import socket

host_ip=socket.gethostbyname(socket.gethostname())
host_connection = pymysql.connect(
  host=host_ip,
  user="mysql_dd_monitor",
  passwd='Jnr$56dD',
  port=3306

)
dbhandler = host_connection.cursor()
SLAVE_STATUS_QUERY="show slave status"
dbhandler.execute(SLAVE_STATUS_QUERY)
SLAVE_STATUS = dbhandler.fetchone()
if SLAVE_STATUS is  None:
    query ="select IF(VARIABLE_VALUE='ON',1,0) as read_only  from performance_schema.global_variables where variable_name='read_only'"
    dbhandler.execute(query)
    READ_STATUS = dbhandler.fetchone()
    for RS in READ_STATUS:
      metric="mysql_custom_readonly_status,type=master read_only_flag={}".format(RS)
      print metric
else:
    query ="select IF(VARIABLE_VALUE='ON',1,0) as read_only  from performance_schema.global_variables where variable_name='read_only'"
    dbhandler.execute(query)
    READ_STATUS = dbhandler.fetchone()
    for RS in READ_STATUS:
      metric="mysql_custom_readonly_status,type=slave read_only_flag={}".format(RS)
      print metric
