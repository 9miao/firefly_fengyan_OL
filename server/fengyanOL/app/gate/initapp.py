#coding:utf8
'''
Created on 2013-9-2

@author: jt
'''
#from app.gate.bridge.otherservermanager import OtherSerManager
from firefly.dbentrust.dbpool import dbpool
from firefly.dbentrust.memclient import mclient
from utils import dbaccess

dbconfig = dbpool.config
dbconfig['maxWait']=5
dbaccess.dbpool.initPool(**dbconfig)
dbaccess.memclient = mclient
dbaccess.memdb = mclient.connection
    
from bridge.netservermanager import NetSerManager
from bridge.scenesermanger import SceneSerManager
from bridge.famsermanger import FamSerManager
from serverconfig import serviceBystart

def loadModule():
    from netapp import *
    from services.rootsupport import *
    
    FamSerManager()
    SceneSerManager()
    NetSerManager()
    serviceBystart.doService()
