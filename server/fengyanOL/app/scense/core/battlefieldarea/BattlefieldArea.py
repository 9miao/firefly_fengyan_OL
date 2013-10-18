#coding:utf8
'''
Created on 2011-9-23

@author: lan
'''
from app.scense.core.battlefieldarea.guildBattleScene import GuildBattleScene

class BattlefieldArea(object):
    '''战斗区域（行会战副本）'''
    
    def __init__(self,id,attackCamp,defenseCamp,templateId = 0,entrance_1=0,entrance_2=0):
        '''初始化战斗区域
        @param id: int区域的动态id
        @param templateId: int 区域的模板id
        @param entrance_1: 区域入口地图1
        @param entrance_2: 区域入口地图2
        @param attackCamp: int 主动方国阵营id
        @param defenseCamp: int 被动方国阵营id
        @param attackIntegral: int 主动方的评分
        @param defenseCamp: int 被动方的评分
        @param scenes: int 区域的场景
        '''
        self.id = id
        self.name = u''
        self.templateId = templateId
        self.entrance_1 = entrance_1
        self.entrance_2 = entrance_2
        self.attackCamp = attackCamp
        self.defenseCamp = defenseCamp
        self.attackIntegral = 0
        self.attackIntegral = 0
        self.scenes = {}#所有的场景
        self.initData()
        
    def initData(self):
        '''初始化战场'''
        sceneIdList = [1001,1002,1003,1004,1005]#模拟数据
        entrance_1 = 1001
        entrance_2 = 1005
        self.setEntrance_1(entrance_1)
        self.setEntrance_2(entrance_2)
        for sceneId in sceneIdList:
            self.addScene(sceneId)
        
    def setTemplateId(self,templateId):
        '''设置模板id
        @param templateId: int 模板id
        '''
        self.templateId = templateId
        
    def setEntrance_1(self,entrance_1):
        '''设置入口1的场景id
        @param entrance_1: int 入口1的场景id
        '''
        self.entrance_1 = entrance_1
        
    def setEntrance_2(self,entrance_2):
        '''设置入口1的场景id
        @param entrance_2: int 入口2的场景id
        '''
        self.entrance_2 = entrance_2
        
    def addScene(self,sceneId):
        '''添加场景'''
        scene = GuildBattleScene(sceneId,self)
        if sceneId == self.entrance_1:
            scene.produceMonster(1,position=(300,400),camp = self.attackCamp)
        if sceneId == self.entrance_2:
            scene.produceMonster(1, position=(900,400),camp = self.defenseCamp)
        self.scenes[sceneId] = scene
            
    def pushAreaInfo(self):
        '''推送场景信息，遍历战斗区域中所有的场景，推送场景中的信息
        '''
        for scene in self.scenes.values():
            scene.pushSceneInfo()
            
    def pushBattleFieldInfo(self):
        '''推送行会战斗信息'''
        pass
        
    def getSceneById(self,sceneId):
        '''根据id获取场景实例
        '''
        return self.scenes.get(sceneId,None)
    
    def enterGuildBattleField(self,guildId,characterId):
        '''进入行会战副本中
        @param guildId: int 行会的id
        @param characterId: int 角色的id
        '''
        if guildId == self.attackCamp:
            scene = self.getSceneById(self.entrance_1)
            scene.addPlayer(characterId)
            return self.entrance_1
        if guildId == self.defenseCamp:
            scene = self.getSceneById(self.entrance_2)
            scene.addPlayer(characterId)
            return self.entrance_2
        return 0
    
    
    
    
    
    