import pymysql
import socket
import sys

slave_ip=socket.gethostbyname(socket.gethostname())
slave_connection = pymysql.connect(
  host=slave_ip,
  user="mysql_dd_monitor",
  passwd='Jnr$56dD',
  port=3306

)

dbhandler = slave_connection.cursor()
SLAVE_STATUS_QUERY="show slave status"
dbhandler.execute(SLAVE_STATUS_QUERY)
SLAVE_STATUS = dbhandler.fetchone()
if SLAVE_STATUS is None:
    sys.exit(0)

slave_executed_gtid ="SHOW GLOBAL VARIABLES LIKE 'gtid_executed'"
dbhandler.execute(slave_executed_gtid)
SLAVE_GTID = dbhandler.fetchone()

for sgtid in SLAVE_GTID :
        x = sgtid.split('gtid_executed')
        SGTID = x[0]

MASTER_FIND_QUERY="select host from  mysql.slave_master_info"
dbhandler.execute(MASTER_FIND_QUERY)
MASTER = dbhandler.fetchone()
for master in MASTER :
        y=str(master)


config = {
    'user': 'mysql_dd_monitor',
    'password': 'Jnr$56dD',
    'host':y
}


cnx = pymysql.connect(**config)


mdbhandler = cnx.cursor()
master_executed_gtid="SHOW GLOBAL VARIABLES LIKE 'gtid_executed'"
mdbhandler.execute(master_executed_gtid)
MASTER_GTID = mdbhandler.fetchone()

for mgtid in MASTER_GTID :
        z = mgtid.split('gtid_executed')
        MGTID =z[0]

query = "select gtid_subset('" + SGTID + "','" + MGTID + "')"
dbhandler.execute(query)
ERRANT_FLAG = dbhandler.fetchone()
for EF in ERRANT_FLAG:
       metric="mysql_custom_errant_gtid_status,type=slave errant_gtid_flag={}".format(EF)
       print metric
