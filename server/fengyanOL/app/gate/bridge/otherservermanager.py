#coding:utf8
'''
Created on 2012-4-8

@author: Administrator
'''
from twisted.internet import reactor
import subprocess

reactor = reactor

class OtherSerManager:
    
    
    def __init__(self):
        pass
#        self.startOtherServer()
    
    def startOtherServer(self):
        '''start Net Server'''
        from app.gate.utils import dbaccess
        servername = dbaccess.servername
        subprocess.Popen('python ./servers/PublicServer/src/startPublicServer.pyc -servername %s'%servername
                         ,shell=True)
        subprocess.Popen('python ./servers/ChatServer/src/startChatServer.pyc -servername %s'%servername
                         ,shell=True)
        subprocess.Popen('python ./servers/SecurityServer/src/startSecserver.pyc -servername %s'%servername
                         ,shell=True)
        subprocess.Popen('python ./servers/AdminServer/src/startAdminServer.pyc -servername %s'%servername
                         ,shell=True)
        subprocess.Popen('python ./servers/SceneServer/src/startSceneServer.pyc \
        -named teamserver_9999 -servername %s'%(servername),shell=True) 
    