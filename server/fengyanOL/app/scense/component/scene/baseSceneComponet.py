#coding:utf8
'''
Created on 2011-9-24

@author: lan
'''
from app.scense.core.character.Monster import Monster
from app.scense.component.Component import Component

class BaseSceneComponent(Component):
    '''基础场景类'''
    
    def __init__(self,id,owner):
        '''初始化基础场景类
        @param id: int 场景的id
        __players 存放场景中所有的角色id集合
        __monsters 存放场景中所有的怪物id集合
        __npcs 存放场景中所有的npc id 集合
        __pkType 场景pk 类型 1和平 2杀怪 3队伍 &杀怪 4国&杀怪 5全体&杀怪 (2默认)
        __resource 场景的资源id
        __tag 场景动态标识（用来表示怪物的动态ID）
        '''
        Component.__init__(self, owner)
        self.__id = id
        self.__players = set()
        self.__monsters = {}
        self.__npcs = set()
        self.__pkType = 2
        self.__resource = 1000
        self.__tag = 1001
        self.initScene()
        
    def initScene(self):
        '''初始化战斗场景'''
        pass
        
    def getId(self):
        '''获取场景的id
        '''
        return self.__id
    
    def getPlayers(self):
        '''获取场景中所有的角色'''
        return list(self.__players)
    
    def addPlayer(self,playerId):
        '''添加角色
        @param playerId: int 角色的id
        '''
        if playerId not in self.__players:
            self.__players.add(playerId)
            
    def dropPlayer(self,playerId):
        '''删除场景中的玩家
        @param playerId: int 角色的id
        '''
        self.__players.remove(playerId)
    
    def getMonsters(self):
        '''获取场景中所有的怪物'''
        return self.__monsters
    
    def produceMonster(self,monsterId,position = (300,400),camp=0):
        '''产生一个怪物
        @param monsterId: int 怪物的模板id
        '''
        monster = Monster(templateId = monsterId,id = self.__tag)
        monster.baseInfo.setPosition(position)
        monster.setCamp(camp)
        self.addMonster(monster)
    
    def addMonster(self,monster):
        '''添加角色
        @param monsterId: int 怪物的id
        '''
        self.__monsters[monster.baseInfo.id] = monster
        self.__tag +=1
            
    def dropMonster(self,tagId):
        '''删除场景中的玩家
        @param monsterId: int 怪物的id
        '''
        try:
            del self.__monsters[tagId]
        except Exception:
            pass
    
    def getNpcs(self):
        '''获取场景中所有的npc'''
        return list(self.__npcs)
        
    def addNpc(self,npcId):
        '''添加NPC
        @param monsterId: int 怪物的id
        '''
        if npcId not in self.__npcs:
            self.__npcs.add(npcId)
            
    def dropNpc(self,npcId):
        '''删除场景中的NPC
        @param monsterId: int 怪物的id
        '''
        self.__npcs.remove(npcId)
        
    def setPkType(self,pkType):
        '''设置pk类型
        @param pkType: int 场景的pk类型
        '''
        self.__pkType = pkType
        
    def getPkType(self):
        '''获取pk类型
        '''
        return self.__pkType
    
    def getResource(self):
        '''放回场景的资源id'''
        return self.__resource
        
    def pushSceneInfo(self):
        '''推送场景信息'''
        pass
        
        
    