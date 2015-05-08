# 
#  Licensed Materials - Property of IBM
#
#  (c) Copyright IBM Corp. 2007-2013
#

import unittest, sys, datetime
import ibm_db
import config
from testfunctions import IbmDbTestFunctions

class IbmDbTestCase(unittest.TestCase):

  def test_InsertRetrieveDateTimeTypeColumn(self):
    self.obj = IbmDbTestFunctions()
    self.obj.assert_expectf(self.run_test_InsertRetrieveDateTimeTypeColumn)

  def run_test_InsertRetrieveDateTimeTypeColumn(self):
    conn = ibm_db.connect(config.database, config.user, config.password)
    
    if conn:
      drop = 'DROP TABLE tab_datetime'
      result = ''
      try:
        result = ibm_db.exec_immediate(conn, drop)
      except:
        pass
      t_val = datetime.time(10, 42, 34)
      d_val = datetime.date(1981, 7, 8)
      #ts_val = datetime.datetime.today()
      ts_val = datetime.datetime(1981, 7, 8, 10, 42, 34, 10)
      server = ibm_db.server_info( conn )
      if (self.obj.isServerInformix(server)):
        statement = "CREATE TABLE tab_datetime (col1 DATETIME HOUR TO SECOND, col2 DATE, col3 DATETIME YEAR TO FRACTION(5))"
        result = ibm_db.exec_immediate(conn, statement)
        statement = "INSERT INTO tab_datetime (col1, col2, col3) values (?, ?, ?)"
        stmt = ibm_db.prepare(conn, statement)
        result = ibm_db.execute(stmt, (t_val, d_val, ts_val))
      else:
        statement = "CREATE TABLE tab_datetime (col1 TIME, col2 DATE, col3 TIMESTAMP)"
        result = ibm_db.exec_immediate(conn, statement)
        statement = "INSERT INTO tab_datetime (col1, col2, col3) values (?, ?, ?)"
        stmt = ibm_db.prepare(conn, statement)
        result = ibm_db.execute(stmt, (t_val, d_val, ts_val))

      statement = "SELECT * FROM tab_datetime"
      result = ibm_db.exec_immediate(conn, statement)
      
      for i in range(0, ibm_db.num_fields(result)):
        print(str(i) + ":" + ibm_db.field_type(result,i))

      statement = "SELECT * FROM tab_datetime"
      stmt = ibm_db.prepare(conn, statement)
      rc = ibm_db.execute(stmt)
      result = ibm_db.fetch_row(stmt)
      while ( result ):
        row0 = ibm_db.result(stmt, 0)
        row1 = ibm_db.result(stmt, 1)
        row2 = ibm_db.result(stmt, 2)
        print("%s %s" % (type(row0), row0))
        print("%s %s" % (type(row1), row1))
        print("%s %s" % (type(row2), row2))
        result = ibm_db.fetch_row(stmt)
      
      ibm_db.close(conn)
    else:
      print("Connection failed.")

#__END__
#__LUW_EXPECTED__
#0:time
#1:date
#2:timestamp
#<%s 'datetime.time'> 10:42:34
#<%s 'datetime.date'> 1981-07-08
#<%s 'datetime.datetime'> 1981-07-08 10:42:34.000010
#__ZOS_EXPECTED__
#0:time
#1:date
#2:timestamp
#<%s 'datetime.time'> 10:42:34
#<%s 'datetime.date'> 1981-07-08
#<%s 'datetime.datetime'> 1981-07-08 10:42:34.000010
#__SYSTEMI_EXPECTED__
#0:time
#1:date
#2:timestamp
#<%s 'datetime.time'> 10:42:34
#<%s 'datetime.date'> 1981-07-08
#<%s 'datetime.datetime'> 1981-07-08 10:42:34.000010
#__IDS_EXPECTED__
#0:time
#1:date
#2:timestamp
#<%s 'datetime.time'> 10:42:34
#<%s 'datetime.date'> 1981-07-08
#<%s 'datetime.datetime'> 1981-07-08 10:42:34.000010
