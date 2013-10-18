#coding:utf8
'''
Created on 2012-2-22

@author: sean_lan
'''
from twisted.python import log

WEB_TAG = 88          #后台节点服务起始标示
CHAT_TAG = 100        #聊天节点服务起始标示
NET_TAG = 100000      #网络节点服务起始标识
SCENE_TAG = 200000    #场景节点服务起始标识
FAM_TAG = 300000      #副本节点服务起点标识
TEAM_TAG = 9999       #组队节点服务标识
CHAT_NAME = "chatserver"
NET_NAME = "netserver"
SCENE_NAME = "sceneserver"
FAM_NAME = "famserver"
WEB_NAME = "adminserver"
TEAM_NAME = "teamserver"

class DNSManager:
    '''域名解析管理器（管理分布节点）单例
    '''
    
    def __init__(self):
        '''初始化
        @param nodes: dict 所有的节点
        '''
        self._childs = {}
        
    def getChildById(self,childId):
        '''根据节点的id获取节点实例
        @param childId: int 子节点的id
        '''
        return self._childs.get(childId)
    
    def getChildByTag(self,tag):
        '''根据节点的id获取节点实例
        @param childId: int 子节点的id
        '''
        return self._childs.get(tag)
    
    def getChildByName(self,childname):
        '''根据节点的名称获取节点实例
        @param childname: str 节点的名称
        '''
        for key,child in self._childs.items():
            if child.getName() == childname:
                return self._childs[key]
        return None
    
    def addChild(self,child):
        '''添加一个child节点
        @param child: Child object
        '''
        name = child.getName()
        taglist = name.split('_')
        if taglist[0] == CHAT_NAME:
            tag = CHAT_TAG
        elif taglist[0] == NET_NAME:
            tag = NET_TAG
        elif taglist[0] == SCENE_NAME:
            tag = SCENE_TAG
            tag += int(taglist[1])
        elif taglist[0] == FAM_NAME:
            tag = FAM_TAG
            tag += int(taglist[1])
        elif taglist[0] == TEAM_NAME:
            tag = TEAM_TAG
        elif taglist[0] == WEB_NAME:
            tag = WEB_TAG
        else:
            raise Exception("child node %d exists"% tag)
            
        if self._childs.has_key(tag):
            raise Exception("child node %d exists"% tag)
        self._childs[tag] = child
    
    def dropChild(self,child):
        '''删除一个节点'''
        print child.getName(),'dropChild'
        key = child._id
        try:
            del self._childs[key]
        except Exception,e:
            log.msg(str(e))
            
    def callChild(self,key,*args,**kw):
        '''调用子节点的接口'''
        child = self._childs.get(key,None)
        if not child:
            log.err("child %d doesn't exists"%key)
            return
        return child.callbackChild(*args,**kw)
        
    def callChildByName(self,childname,*args,**kw):
        '''调用子节点的接口
        @param childname: str 子节点的名称
        '''
        child = self.getChildByName(childname)
        if not child:
            log.err("child %s doesn't exists"%childname)
            return
        return child.callbackChild(*args,**kw)
    
    def dropChildByID(self,childId):
        '''删除一个child 节点
        @param childId: int Child ID 
        '''
        for key,child in self._childs.items():
            if child._id == childId:
                del self._childs[key]
        return None
    
    
    