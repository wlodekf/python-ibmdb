# 
#  Licensed Materials - Property of IBM
#
#  (c) Copyright IBM Corp. 2007-2008
#

import unittest, sys
import ibm_db
import config
from testfunctions import IbmDbTestFunctions

class IbmDbTestCase(unittest.TestCase):

  def test_032_ResultIndexName(self):
    self.obj = IbmDbTestFunctions()
    self.obj.assert_expect(self.run_test_032)

  def run_test_032(self):
      conn = ibm_db.connect(config.database, config.user, config.password)
      server = ibm_db.server_info( conn )

      if conn:
        stmt = ibm_db.exec_immediate(conn, "SELECT id, breed, name, weight FROM animals WHERE id = 6")
        
        while (ibm_db.fetch_row(stmt)):
          if (self.obj.isServerInformix(server)):
            id = ibm_db.result(stmt, "id")
            breed = ibm_db.result(stmt, "breed")
            name = ibm_db.result(stmt, "name")
            weight = ibm_db.result(stmt, "weight")
          else:
            id = ibm_db.result(stmt, "ID")
            breed = ibm_db.result(stmt, "BREED")
            name = ibm_db.result(stmt, "NAME")
            weight = ibm_db.result(stmt, "WEIGHT")
          print("int(%d)" % id)
          print("string(%d) \"%s\"" % (len(breed), breed))
          print("string(%d) \"%s\"" % (len(name), name))
          print("string(%d) \"%s\"" % (len(str(weight)), weight))
        ibm_db.close(conn)
      else:
        print("Connection failed.")

#__END__
#__LUW_EXPECTED__
#int(6)
#string(5) "llama"
#string(16) "Sweater         "
#string(6) "150.00"
#__ZOS_EXPECTED__
#int(6)
#string(5) "llama"
#string(16) "Sweater         "
#string(6) "150.00"
#__SYSTEMI_EXPECTED__
#int(6)
#string(5) "llama"
#string(16) "Sweater         "
#string(6) "150.00"
#__IDS_EXPECTED__
#int(6)
#string(5) "llama"
#string(16) "Sweater         "
#string(6) "150.00"
