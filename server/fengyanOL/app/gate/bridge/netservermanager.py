#coding:utf8
'''
Created on 2012-3-22
netserver Manager
@author: Administrator
'''

from twisted.internet import reactor
from firefly.utils.singleton import Singleton
import subprocess
from firefly.server.globalobject import GlobalObject

reactor = reactor

class NetSerManager:
    
    __metaclass__ = Singleton
    
    def __init__(self):
        pass
#        reactor.callLater(1,self.startNetServer)
    
    def startNetServer(self):
        '''start Net Server'''
        from app.gate.utils import dbaccess
        servername = dbaccess.servername
        subprocess.Popen('python ./servers/NetServer/src/startNetServer.pyc -servername %s'%servername
                         ,shell=True) 
        
    def doWhenStop(self):
        '''when netserver stoped'''
#        from bridge.famsermanger import FamSerManager
#        from bridge.scenesermanger import SceneSerManager
#        from core.UserManager import UsersManager
        from app.gate.core.VCharacterManager import VCharacterManager
#        from app.gate.serverconfig.root import root
#        childs = root._childsmanager._childs.keys()
#        for node in childs:
#            if 200000<node<300000:
#                root.callChild(node,50)
        for vcharacter in VCharacterManager().character_client.values():
            dynamicId = vcharacter.dynamicId
            node = vcharacter.getNode()
            if node:
#                root.callChild(node,2,dynamicId)
                GlobalObject().root.callChild("scense_1000",2,dynamicId)
        
        