#!/home/tops/bin/python
# -*- coding: utf-8 -*-
# Create Time: 2020/3/7 10:47
# Author: Riners

import commands

tianji_api = "http://127.0.0.1:7070/api/v3/column/m.*"
oss_ag = "http://localhost:7070/api/v3/column/m.ip?m.sr.id=oss-chiji.ChijiAgent%23"
ecs_ag = "http://localhost:7070/api/v3/column/m.ip?m.sr.id=ecs-init.EcsAg%23"
ots_ag = "http://localhost:7070/api/v3/column/m.ip?m.sr.id=TableStore.Tools%23"
blinks_ag = "http://localhost:7070/api/v3/column/m.ip?m.sr.id=blink-bayes.BayesAg%23"
odps_ag = "http://localhost:7070/api/v3/column/m.ip?m.sr.id=odps-service-console.AdminConsole%23"
ads_ag = "http://localhost:7070/api/v3/column/m.ip?m.sr.id=ads-service.AdminGateway%23"
pangu_api = "http://localhost:7070/api/v3/column/m.ip?m.sr.id=pangu.PanguTools%23"


cmd = 'curl %s' % tianji_api
print commands.getoutput(cmd)
