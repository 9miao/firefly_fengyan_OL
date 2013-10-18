#coding:utf8
'''
Created on 2012-8-7
团队战斗战力管理类
@author: jt
'''

from twisted.python import log
from app.gate.utils import dbaccess




def ishaveTeamFight(pid):
    mc=dbaccess.memclient
    ncxx=mc.get("TeamInstanceFight#pi")
    CXpi=list(ncxx) #set([])或None
    if not CXpi:
        return False
    if CXpi.count(pid)>0:
        return True
    return False

