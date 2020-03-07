#!/home/tops/bin/python
# -*- coding: utf-8 -*-
# Create Time: 2020/3/7 10:59
# Author: Riners

import re
import csv
import sys
import subprocess
import requests
import argparse
import time

from socket import *
from decimal import Decimal, getcontext

Description = '''
Check Pangu And Disk Water
'''

VERSION = '1.0'
tianji_api = "http://127.0.0.1:7070/api/v3/column/m.*"
oss_ag = "http://localhost:7070/api/v3/column/m.ip?m.sr.id=oss-chiji.ChijiAgent%23"
ecs_ag = "http://localhost:7070/api/v3/column/m.ip?m.sr.id=ecs-init.EcsAg%23"
ots_ag = "http://localhost:7070/api/v3/column/m.ip?m.sr.id=TableStore.Tools%23"
blinks_ag = "http://localhost:7070/api/v3/column/m.ip?m.sr.id=blink-bayes.BayesAg%23"
odps_ag = "http://localhost:7070/api/v3/column/m.ip?m.sr.id=odps-service-console.AdminConsole%23"
ads_ag = "http://localhost:7070/api/v3/column/m.ip?m.sr.id=ads-service.AdminGateway%23"
pangu_api = "http://localhost:7070/api/v3/column/m.ip?m.sr.id=pangu.PanguTools%23"

product = ["ecs", "minirds", "rds", "vpc", "slb"]
warning_usage = 90
critical_usage = 95


CORLOR_BLACK    = "\033[0;30m"
COLOR_RED       =   "\033[0;31m"
COLOR_GREEN     =   "\033[0;32m"
COLOR_YELLOW    =   "\033[0;33m"
COLOR_BLUE      =   "\033[0;34m"
COLOR_PUPPLE    =   "\033[0;35m"
COLOR_CYAN      =   "\033[0;36m"
COLOR_WHITE     =   "\033[0;37m"
COLOR_RESTORE   =   "\033[0m"

def colorPrint(msg, color = None):
    msg = color + msg + COLOR_RESTORE
    print msg
    sys.stdout.flush()
    # return msg


'''颜色打印测试代码'''
# colorPrint('hello colorful world!', color = CORLOR_BLACK)
# colorPrint('hello colorful world!', color = COLOR_RED)
# colorPrint('hello colorful world!', color = COLOR_GREEN)
# colorPrint('hello colorful world!', color = COLOR_YELLOW)
# colorPrint('hello colorful world!', color = COLOR_BLUE)
# colorPrint('hello colorful world!', color = COLOR_PUPPLE)
# colorPrint('hello colorful world!', color = COLOR_CYAN)
# colorPrint('hello colorful world!', color = COLOR_WHITE)
# colorPrint('hello colorful world!', color = COLOR_RESTORE)

class CheckWater(object):
    def __init__(self):
        self.args = self.parse_args()

    def init_args(self):
        parser = argparse.ArgumentParser(description=Description)
        parser.add_argument("-V", action='version', version= VERSION)
        parser.add_argument("-V2", '-v2', action='store_true', dest = 'version2', default=False, help='check for v2')
        parser.add_argument("-V3", '-v3', action='store_true', dest = 'version3', default=False, help='check for v3')
        return parser


    def parse_args(self):
        args = self.init_args().parse_args()
        if args.version2 and args.version3:
            raise SystemExit("V2 and V3 cannot use together!")
        return args

    #
    # def get_v2_ag(self):
    #     ag_dict = {}
    #     pass



    def get_v3_ag(self):
        ag_dict ={}
        blikns, tianji = self.get_blink_pangu_ip()
        ecs = self.get_ip(ecs_ag)
        oss = self.get_ip(oss_ag)
        ots = self.get_ip(ots_ag)
        odps = self.get_ip(odps_ag)
        ads = self.get_ip(ads_ag)

        if ecs:
            ag_dict["ecs"] = ecs
        if oss:
            ag_dict["oss"] = oss
        if ots:
            ag_dict["ots"] = ots
        if odps:
            ag_dict["odps"] = odps
        if ads:
            ag_dict["ads"] = ads
        if blikns:
            ag_dict ["blins"] = blikns
        if tianji:
            ag_dict ["tianji"] = tianji

        return ag_dict

    def request_api(self):
        ret = requests.get(tianji_api)
        # print ret
        return ret.json()

    def get_v3_ips(self):
        ips = []
        result = self.request_api()
        for i in result:
            if i['m.project'] in product:
                ips.append((i['m.project'], i['m.ip']))
        return ips

    def get_cs_info(self, role):
        cmd = 'ssh %s -o ConnectTimeout=3 "/apsara/deploy/puadmin lscs"' % (role)


        try:
            cs_info = subprocess.check_output(cmd, shell=True).split('\n')
        except subprocess.CalledProcessError:
            return False
        return cs_info

    def get_ip(self, role):
        ret = requests.get(role).json()
        # print ret
        if ret:
            return ret[0]['m.ip']


    def get_blink_pangu_ip(self):
        blink_pangu_ip, tianji_pangu_ip= ('','')
        ret1 = requests.get(pangu_api)
        ret2 = requests.get(tianji_api)
        if ret1 and ret2:
            for x in ret1.json():
                for y in ret2.json():
                    if x['m.ip'] == y['m.ip']:
                        if ['m.project'] == 'blink':
                            blink_pangu_ip = y['m.ip']
                        if ['m.project'] == 'tianji':
                            tianji_pangu_ip = y['m.ip']
        return blink_pangu_ip, tianji_pangu_ip

    def usage(self, cs_info):
        getcontext().prec = 4
        total_disk_size = self.get_total_disk(cs_info)
        free_disk_size = self.get_free_disk(cs_info)
        used_disk_size = str(int(total_disk_size) - int(free_disk_size))
        result = Decimal(used_disk_size) / Decimal(total_disk_size) * Decimal(100)
        return result

    def get_total_disk(self, cs_info):
        total_disk_size = None
        for i in cs_info:
            if i.startswith("Total Disk Size"):
                total_disk_size = i.split(':')[-1].split()[0]
                break
        if not total_disk_size:
            raise SystemExit("Something error when get Total Disk Size!")
        return total_disk_size
    def get_free_disk(self, cs_info):
        free_disk_size = None
        for i in cs_info:
            if i.startswith("Total Free Disk Size"):
                free_disk_size = i.split(':')[-1].split()[0]
                break
        if not free_disk_size:
            raise SystemExit("something error when get Free Disk Size!")
        return free_disk_size

    def check_df(self, ips =[]):
        minirds_warning_result = []
        minirds_critical_result = []

        rds_warning_result = []
        rds_critical_result = []

        slb_warning_result = []
        slb_critical_result = []

        vpc_warning_result = []
        vpc_critical_result = []

        ecs_warning_result = []
        ecs_critical_result = []

        for role, ip in ips:
            cmd = 'ssh %s -o ConnectTimeout=3 "df -h" | grep -Eiv "success|Filesystem"' %(ip)
            try:
                ret = subprocess.check_output(cmd, shell=True).split('\n')
                for i in ret:
                    r = i.split()
                    if len(r) == 6 and r[4].endswith("%"):
                        if warning_usage <= int(r[4].strip('%')) < critical_usage:
                            if role == 'minirds':
                                minirds_warning_result.append({'ip': ip, 'mount_point': r[0], 'path': r[5], 'usage': r[4]})
                            elif role == 'rds':
                                rds_warning_result.append({'ip': ip, 'mount_point': r[0], 'path': r[5], 'usage': r[4]})
                            elif role == 'slb':
                                slb_warning_result.append({'ip': ip, 'mount_point': r[0], 'path': r[5], 'usage': r[4]})
                            elif role == 'vpc':
                                vpc_warning_result.append({'ip': ip, 'mount_point': r[0], 'path': r[5], 'usage': r[4]})
                            else:
                                ecs_warning_result.append({'ip': ip, 'mount_point': r[0], 'path': r[5], 'usage': r[4]})
                        if int(r[4].strip('%')) >= critical_usage:
                            if role == 'minirds':
                                minirds_critical_result.append({'ip': ip, 'mount_point': r[0], 'path': r[5], 'usage': r[4]})
                            elif role == 'rds':
                                rds_critical_result.append({'ip': ip, 'mount_point': r[0], 'path': r[5], 'usage': r[4]})
                            elif role == 'slb':
                                slb_critical_result.append({'ip': ip, 'mount_point': r[0], 'path': r[5], 'usage': r[4]})
                            elif role == 'vpc':
                                vpc_critical_result.append({'ip': ip, 'mount_point': r[0], 'path': r[5], 'usage': r[4]})
                            else:
                                if not "SSDCache" in r[5]:
                                    ecs_critical_result.append({'ip': ip, 'mount_point': r[0], 'path': r[5], 'usage': r[4]})
            except Exception as e:
                print e


        return minirds_warning_result, minirds_critical_result, rds_warning_result, rds_critical_result, slb_warning_result, slb_critical_result, vpc_warning_result, vpc_critical_result, ecs_warning_result, ecs_critical_result






    def main(self):
        ag_dict = {}
        ips = []
        if self.args.version2:
            # ag_dict = self.getcontext
            print COLOR_PUPPLE + 'Weclome to ckeck water for v2'
        elif self.args.version3:
            print COLOR_PUPPLE + 'Welcome to check Water for v3'
            ag_dict = self.get_v3_ag()
            ips = self.get_v3_ips()
            # print ag_dict
            # print ips
        else:
            raise SystemExit(COLOR_RED + "-V2 or -V3 must has one !")
        if not ag_dict:
            raise SystemExit(COLOR_RED + "Not found any ag address !")

        colorPrint('Checkpangu:', COLOR_BLUE)
        for k, v in ag_dict.items():
            cs_info = self.get_cs_info(v)
            colorPrint('\t%s' %(k) + ':' ,COLOR_BLUE)
            if cs_info:
                usage = self.usage(cs_info)
                if 75 <= usage < 85:
                    colorPrint("\t\tWarning: Thepangu usage percentage of %s is: %s" % (k, usage) + '%', COLOR_YELLOW)
                elif usage >= 85:
                    colorPrint("\t\tCritical: Thepangu usage percentage of %s is: %s" % (k, usage) + '%', COLOR_RED)
                else:
                    colorPrint("\t\tOK: The pangu usage percentage of %s is: %s" %(k,usage) + '%',COLOR_GREEN)
            else:
                colorPrint("\t\tGet Pangu CS Info Error!",COLOR_RED)
        if not  ips:
            raise SystemExit("Not Found Any IP Address!")


        minirds_warning_result,minirds_critical_result,rds_warning_result,rds_critical_result,slb_warning_result,slb_critical_result,vpc_warning_result,vpc_critical_result,ecs_warning_result,ecs_critical_result, = self.check_df(ips)
        colorPrint('CheckDisk:', COLOR_BLUE)
        colorPrint('\tMiniRDS:', COLOR_BLUE)
        if not warning_usage or minirds_critical_result:
            colorPrint("\t\tALL OK",COLOR_GREEN)
        for mw in minirds_warning_result:
            colorPrint("\t\tWarning: %s of %s has used %s" % (mw['path'], mw['ip'], mw['usage']), COLOR_YELLOW)
        for mc in minirds_critical_result:
            colorPrint("\t\tCritical: %s of %s has used %s" % (mc['path'], mc['ip'], mc['usage']), COLOR_RED)

        colorPrint('\tRDS:',COLOR_BLUE)
        if not (rds_warning_result or rds_critical_result):
            colorPrint("\t\tALL OK",COLOR_GREEN)
        for rw in rds_warning_result:
            colorPrint("\t\tWarning: %s of %s has used %s" %(rw['path'],rw['ip'],rw['usage']),COLOR_YELLOW)
        for rc in rds_critical_result:
            colorPrint("\t\tCritical: %s of %s has used %s" %(rc['path'],rc['ip'],rc['usage']),COLOR_RED)

        colorPrint('\tSLB:',COLOR_BLUE)
        if not (slb_warning_result or slb_critical_result):
            colorPrint("\t\tALL OK",COLOR_GREEN)
        for sw in slb_warning_result:
            colorPrint("\t\tWarning: %s of %s has used %s" %(sw['path'],sw['ip'],sw['usage']),COLOR_YELLOW)
        for sc in slb_critical_result:
            colorPrint("\t\tCritical: %s of %s has used %s" %(sc['path'],sc['ip'],sc['usage']),COLOR_RED)

        colorPrint('\tVPC:',COLOR_BLUE)
        if not (vpc_warning_result or vpc_critical_result):
            colorPrint("\t\tALL OK",COLOR_GREEN)
        for vw in vpc_warning_result:
            colorPrint("\t\tWarning: %s of %s has used %s" %(vw['path'],vw['ip'],vw['usage']),COLOR_YELLOW)
        for vc in vpc_critical_result:
            colorPrint("\t\tCritical: %s of %s has used %s" %(vc['path'],vc['ip'],vc['usage']),COLOR_RED)

        colorPrint('\tECS:',COLOR_BLUE)
        if not (ecs_warning_result or ecs_critical_result):
            colorPrint("\t\tALL OK",COLOR_GREEN)
        for ew in ecs_warning_result:
            colorPrint("\t\tWarning: %s of %s has used %s" %(ew['path'],ew['ip'],ew['usage']),COLOR_YELLOW)
        for ec in ecs_critical_result:
            colorPrint("\t\tCritical: %s of %s has used %s" %(ec['path'],ec['ip'],ec['usage']),COLOR_RED)





if __name__ == '__main__':
    check_water = CheckWater()
    check_water.main()