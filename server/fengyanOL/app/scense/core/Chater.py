#coding:utf8
'''
Created on 2011-2-14

@author: sean_lan
'''
class Chater:
    '''
    聊天成员类
    '''
    def __init__(self, characterId,dynamicId):
        self.characterId = characterId
        self.dynamicId = dynamicId
        
    def getDynamicId(self):
        return self.dynamicId
    
    def getCharacterId(self):
        return self.characterId
        