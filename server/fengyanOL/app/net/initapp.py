#coding:utf8
'''
Created on 2013-8-30

@author: jt
'''
from firefly.server.globalobject import GlobalObject
from firefly.netconnect.datapack import DataPackProtoc


def callWhenConnLost(conn):
    '''连接断开时的处理'''
    dynamicId = conn.transport.sessionno
    GlobalObject().remote['gate'].callRemote("NetConnLost_2",dynamicId)

def CreatVersionResult(netversion):
    from protoFile import getServerVersion_pb2
    response = getServerVersion_pb2.getVersionResponse()
    response.version = netversion
    msg = response.SerializeToString()
    return msg

def doConnectionMade(conn):
    '''当连接建立时调用的方法'''
    GlobalObject().netfactory.pushObject(10001, CreatVersionResult("Distributed Login Test"), [conn.transport.sessionno])
    
dataprotocl = DataPackProtoc(78,37,38,48,9,0) #协议头
GlobalObject().netfactory.setDataProtocl(dataprotocl)

GlobalObject().netfactory.doConnectionLost = callWhenConnLost
GlobalObject().netfactory.doConnectionMade = doConnectionMade
GlobalObject().remote['gate']._reference._service.unDisplay.add("pushData")
GlobalObject().remote['gate']._reference._service.unDisplay.add("pushObject")



def loadModule():
#    from firefly.dbentrust.dbpool import dbpool
#    from firefly.dbentrust.memclient import mclient
#    dbconfig = dbpool.config
#    dbaccess.dbpool.initPool(**dbconfig)
#    dbaccess.memclient = mclient
#    dbaccess.memdb = mclient.connection
    import netapp