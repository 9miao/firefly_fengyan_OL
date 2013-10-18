#coding:utf8
'''
Created on 2011-2-14

@author: sean_lan
'''
from app.scense.core.singleton import Singleton

class ChaterManager:
    '''聊天成员单例管理
    @param _chaters: 所有的在线成员
    '''
    __metaclass__ = Singleton

    def __init__(self):
        self._chaters = {}
        
    def addChater(self, chater):
        '''添加一个成员到在线聊天成员列表中'''
        if self._chaters.has_key(chater.characterId):
            raise Exception("系统记录冲突")
        self._chaters[chater.characterId] = chater
    
    def getChaterByCharacterId(self ,characterId):
        '''根据角色的id得到聊天成员'''
        try:
            chater = self._chaters[characterId]
            return chater
        except:
            return None
        
    def getChaterDynamicId(self, id):
        '''得到聊天成员的动态Id'''
        try:
            chater = self._chaters[id]
            return chater.dynamicId
        except:
            return None
        
    def dropChater(self, chater):
        '''移除在线聊天成员'''
        key = None
        for k, v in self._chaters.items():
            if chater is v:
                key = k
        if key is not None:
            #print 'chatManager drop player '
            del self._chaters[key]
            
    def dropChaterById(self ,id):
        '''根据id移除在线聊天成员'''
        try:
            #print
            del self._chaters[id]
        except:
            pass
        
    def dropChaterByDynamicId(self ,dynamicId):
        '''根据动态id移除在线聊天成员'''
        key = None
        for k, v in self._chaters.items():
            if v.dynamicId == dynamicId:
                key = k
        if key is not None:
            del self._chaters[key]
            
            