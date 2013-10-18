#coding:utf8
'''
Created on 2012-2-8

@author: sean_lan
'''
from firefly.server.globalobject import GlobalObject

#实例化一条服务对象

#famserver_1  sceneserver_1000
noderemote = GlobalObject().remote['gate']

def nodeHandle(target):
    '''服务处理，添加处理函数
    @param target: func Object
    '''
    GlobalObject().remote["gate"]._reference._service.mapTarget(target)
    
def getNodeId():
    '''获取服务的节点ID'''
#    nodename = noderemote.getName()
#    servername,nid = nodename.split('_')
#    if servername=='sceneserver':
#        nodeId = 200000 + int(nid)
#    else:
#        nodeId = 300000 + int(nid)
#    return nodeId
    return "scense_1000"
    
def pushObject(topicID,msg,sendList):
    '''根据客户端的的ID推送消息'''
    if not sendList:
        return
    noderemote.callRemote("pushObject",topicID,msg,sendList)
    
def pushObjectToAll(topicID,msg):
    '''根据客户端的的ID推送消息'''
    noderemote.callRemote("pushObjectToAll_11",topicID,msg)
    
def pushObjectByCharacterId(topicID,msg,sendList):
    '''根据角色的ID推送消息'''
    if not sendList:
        return
    noderemote.callRemote("pushObjectByCharacterId_10",topicID,msg,sendList)
    


