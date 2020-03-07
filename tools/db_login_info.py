#!/home/tops/bin/python
# -*- coding: utf-8 -*-
# Create Time: 2020/3/7 20:04
# Author: Riners

#!/home/tops/bin/python
# -*- coding: utf-8 -*-
# Create Time: 2020/3/7 17:00
# Author: Riners
import requests
import time
import commands
import json
tianji_service_result_api = 'http://localhost:7070/api/v3/column/service.res.result'
ret = requests.get(tianji_service_result_api).json()
class DbConnect(object):
    '''get db info'''
    def get_db_info(self, db_name):
        ret = requests.get(tianji_service_result_api).json()
        db_list = []
        for i in ret:
            ret1 = i.get("service.res.result")
            if 'db_password' in ret1:
                ret2 = json.loads(str(ret1))
                db_list.append(ret2)
        for i in db_list:
           if i['db_name'] == db_name:
                return i
    def query_login_info(self,dbname):
        db_json = self.get_db_info(dbname)
        db_host = db_json.get("db_host")
        db_name = db_json.get("dbName")
        db_user = db_json.get("db_user")
        db_password = db_json.get("db_password")
        db_port = db_json.get("db_port")
        login_info = 'mysql -h%s -u%s -p%s -P%s ' % (db_host, db_user, db_password, db_port )
        print login_info
        return login_info
    def main(self):
        # while True:
        db_name = raw_input("Enter db_name: ")
        db_login_info = self.query_login_info(db_name)
if __name__ == '__main__':
    db_connect = DbConnect()
    db_connect.main()