#coding:utf8
'''
Created on 2011-3-22

@author: sean_lan
'''
from app.scense.utils import dbaccess
from app.scense.component.baseInfo.BaseInfoComponent import BaseInfoComponent
from app.scense.core.language.Language import Lg

class CharacterBaseInfoComponent(BaseInfoComponent):
    '''玩家基础信息组件类'''
    def __init__(self, owner, cid, nickName=u"",viptype=1,portrait=u"",pronouncement=u"",status=1):
        '''
        Constructor
        '''
        BaseInfoComponent.__init__(self, owner, cid, nickName)
        self._viptype = viptype  #玩家类型 
        self._portrait = portrait  #人物头像
        self._pronouncement = pronouncement #个人宣言(描述)
        self._status = status #玩家当前状态 1正常状态 2排队大厅   3冥想状态 4战斗状态
        self._pkStatus = 1 #玩家的pk状态
        self._town = 1 #所属城镇
        self._location = 1 #所属位置 #副本场景Id
        self._baseName = nickName
        self._position =(300,400) #当前所属地点的x坐标
        self._lastposition = (300,400)#角色上一次的坐标位置
        self._destination = (0,0)
        self._instanceid = 0
        self._staticPosition = (300,400) #角色的静态地址，如果是怪物，那么怪物将在这个点附近自动移动
        self._queueRoom = 0 #角色在大厅中的房间号
        
        self._state=0 #0表示玩家在普通场景       1表示玩家在副本    2行会战副本
        self._instanceid=0 # 玩家所在副本模板Id
        self._instancetag=0 #玩家所在副本动态Id
        self._areaid=0 #玩家所在副本区域id
        
        
    #获取所在场景名称
    def getSceneName(self):
        '''获取角色当前场景名称 return str'''
        from app.scense.world.scene import Scene
        from app.scense.core.map.MapManager import MapManager
        if self._state<0:
            return Lg().g(272)
        sceneId = self._owner.baseInfo.getTown()
        scene = MapManager().getMapId(sceneId)
        return scene._name
        
        
    #----------------nickName----------- 
        
    def setnickName(self,nickName):#从数据库中读取后赋值
        self._baseName = nickName
        
    def getNickName(self):#获取内存中的值
        return self._baseName
    
    
    #---------------type----------------
    def setAreaid(self,cid):
        self._areaid=cid
        
    def getAreaid(self):
        return self._areaid
    
    def setInstancetag(self,cid):
        self._instancetag=cid
    def getInstancetag(self):
        return self._instancetag
    
    def setInstanceid(self,cid):
        self._instanceid=cid
    def getInstanceid(self):
        return self._instanceid
    
    def setState(self,state):
        self._state=state
        
    def getState(self):
        return self._state
    
    def setType(self ,viptype):#
        self._viptype = viptype
    
    def updateType(self ,viptype):#更新对应的值并修改数据库
        self._viptype = viptype
        dbaccess.updateCharacter(self.id,'viptype', viptype)
    
    def updateSpirit(self,spirit):
        '''修改角色心情
        @param spirit: string 角色心情
        '''
        return dbaccess.updateCharacterStr(self.id, 'spirit', spirit)
           
        
    
    def getType(self):
        return self._viptype
    
    #--------------portrait---------------
    
    def setPortrait(self, portrait):
        self._portrait = portrait
        
    def getPortrait(self):
        return self._portrait
    
    def updatePortrait(self ,portrait):
        self._portrait = portrait
    
    #-------------description--------------
    
    def setDescription(self, description):
        self._description = description
        
    def getDescription(self):
        return self._description
    
    def updateDescription(self ,pronouncement):
        self._pronouncement = pronouncement
        dbaccess.updateCharacter(self.id, 'pronouncement', pronouncement)
    
    #--------------status---------------
        
    def setStatus(self ,status):
        self._status = status
        
    def getStatus(self):
        return self._status
    
    def getStatusName(self):
        '''获取状态名称'''
        if self._status == 2:
            return Lg().g(273)
        elif self._status == 3:
            return Lg().g(274)
        elif self._status == 4:
            return Lg().g(275)
        elif self._status == 5:
            return Lg().g(276)
        elif self._status == 6:
            return Lg().g(277)
        else:
            return None
        
    def updateStatus(self ,status):
        self._status = status
        
    #-------------pkStatus-------------
    
    def setPkStatus(self , pkStatus):
        '''设置pk状态'''
        self._pkStatus = pkStatus
        
    def getPkStatus(self):
        '''获取pk状态'''
        return self._pkStatus    
    
    def updatePkStatus(self, pkStatus):
        self._pkStatus = pkStatus
    
    #-----------------town---------------
    
    def setTown(self, town):
        '''设置所在城镇'''
        self._town = town
        
    def getTown(self):
        '''获取所在城镇'''
        return self._town
    
    def updateTown(self ):
        '''更新所属城镇'''
        dbaccess.updateCharacter(self.id,'town',self._town)
        
    #------------------location----------
    
    def setLocation(self ,location):
        '''设置位置'''
        self._location = location
        
    def getLocation(self):
        '''获取位置'''
        return self._location
    
    def updateLocation(self):
        '''更新场景'''
        dbaccess.updateCharacter(self.id,'location', self._location)
    
    #------------------position------------#坐标相关
    def setPosition(self,position):
        '''设置坐标'''
        self._lastposition = self._position
        self._position = position
        
    def getPosition(self):
        '''获取坐标'''
        return self._position
    
    def getLastPosition(self):
        '''获取上一次的坐标
        '''
        return self._lastposition
    
    def initPosition(self,position):
        '''初始化坐标'''
        self._lastposition = position
        self._position = position
        self._destination = position
    
    def setStaticPosition(self,position):
        '''设置怪物的静态坐标'''
        self._staticPosition = position
        self._position = position
        
    def getStaticPosition(self):
        '''获取静态地址'''
        return self._staticPosition
    
    def updateDestination(self,position):
        '''更新目的地坐标'''
        self._destination = position
        
    def getDestination(self):
        '''获取目的地坐标'''
        return self._destination
    
    #------------------大厅房间信息---------
    def getQueueRoom(self):
        '''获取房间Id'''
        return self._queueRoom
    
    def setQueueRoom(self,queueRoom):
        '''设置房间Id'''
        self._queueRoom = queueRoom
    
    
