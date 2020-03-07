#!/home/tops/bin/python
# -*- coding: utf-8 -*-
# Create Time: 2020/3/7 20:26
# Author: Riners
import json

import requests

tianji_service_result_api = 'http://localhost:7070/api/v3/column/service.res.result'
ret = requests.get(tianji_service_result_api).json()


class QueryInfo(object):
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

    def query_db_login_info(self, dbname):
        db_json = self.get_db_info(dbname)
        db_host = db_json.get("db_host")
        db_name = db_json.get("dbName")
        db_user = db_json.get("db_user")
        db_password = db_json.get("db_password")
        db_port = db_json.get("db_port")
        login_info = 'mysql -h%s -u%s -p%s -P%s -D%s' % (db_host, db_user, db_password, db_port, db_name)
        print login_info
        return login_info

    def get_dns_info(self, app_name):
        ret = requests.get(tianji_service_result_api).json()
        dns_list = []
        for i in ret:
            ret1 = i.get("service.res.result")
            if 'dns' in ret1:
                ret2 = json.loads(str(ret1))
                dns_list.append(ret2['domain'])
        for i in dns_list:
            if app_name in i:
                print i

    def main(self):
        # while True:
        choice = int(raw_input("Please select resource type: \ntype 1 for dns, type 2 for db: \t"))
        if choice == 1:
            app_name = raw_input("Enter app name:\t")
            self.get_dns_info(app_name)
        elif choice == 2:
            db_name = raw_input("Enter db name:\t")
            db_login_info = self.query_db_login_info(db_name)
        else:
            raise SystemExit("something error, exiting.....")


if __name__ == '__main__':
    query_info = QueryInfo()
    query_info.main()
