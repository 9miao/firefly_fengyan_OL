#coding:utf8
'''
Created on 2013-9-2

@author: jt
'''
from utils.dbopera import dbItems
from utils import dbaccess
from firefly.dbentrust.dbpool import dbpool
from firefly.dbentrust.memclient import mclient
from firefly.server.globalobject import GlobalObject
from firefly.netconnect.datapack import DataPackProtoc

dbconfig = dbpool.config
dbaccess.dbpool.initPool(**dbconfig)

dataprotocl = DataPackProtoc(78,37,38,48,9,0) #协议头
GlobalObject().netfactory.setDataProtocl(dataprotocl)

def loadModule():
    from utils.dbopera import dbshieldword
    from net import *
    from rootnode import *
    from app import chat
    
    dbshieldword.getAll_ShieldWord()
    dbaccess.all_ItemTemplate = dbaccess.getAll_ItemTemplate()              #获取所有的物品模板信息
    dbItems.getAllsetInfo()

    
