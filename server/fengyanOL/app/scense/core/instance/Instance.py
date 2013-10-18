#coding:utf8
'''
Created on 2011-6-14

@author: SIOP_09
'''
#from core.scene.Scene import Scene
from app.scense.core.scene.InstanceScene import InstanceScene
from app.scense.core.instance.InstanceActivation import InstanceActivation
from app.scense.core.instance.InstanceClose import InstanceClose
from app.scense.core.instance.InstanceColonize import InstanceColonize
from app.scense.core.PlayersManager import PlayersManager
from app.scense.netInterface import pushObjectNetInterface
from app.scense.component.card.SceneCardComponent import SceneCardComponent
#from netInterface.pushObjectNetInterface import pushTurnAllCardMessage,pushTurnOneCardMessage
from app.scense.utils.dbopera import dbScene
from app.scense.core.instance.InstanceGroupManage import InstanceGroupManage
from app.scense.core.language.Language import Lg

CARD_NUM = 5#默认为10张 

class Instance():
    '''
    副本类
    '''
    def __init__(self,id):
        self._tag=1001 #副本动态Id
        self._id=id    #副本Id
        self._name=""    #副本名称
        self._typeid=1   #副本类型
        self._hard=1   #副本难度  1普通 2精英  3英雄
        
        self._Scenes={}  #存储副本所有场景
        self._sceneid=[]   #场景Id
        
        self._starttime="0:00:00"  #副本开始时间
        self._endtime="0:00:00"    #副本结束时间
        self._uplevle=100    #角色等级上限
        self._downlevle=1   #角色等级下限
        self._props=[]      #开启副本所需要的道具Id
        self._astrictguild=-1 #此副本只允许该行会成员进入 1只允许同行会的在一个副本
        self._pknum=-1        #pk值限制 -1无限制
        self._energy=-1       #进入副本所需要的活力值
        self._teamState=-1    #组队限制 -1无限制   2组队才能进入  3非组队方可进入
        self._teammax=10      #组队最大人数限制
        self._teammin=1       #组队最小人数限制
        self._carry=0         #表示该副本允许玩家使用传送技能或道具进入 -1则不能        
        self._achieveprop=[]  #通过副本后获得的道具列表
        self._teamastrict=-1  #进入该副本后能否组队
        self._noprop=[]       #副本内禁用道具列表
        self._backCity=0      #表示可以使用道具技能回城 -1 表示不能使用道具技能回城
        self._annal=0         #表示可以使用路点记录道具记录副本和坐标  -1不能记录副本及其坐标
        self._bargain=0       #允许玩家在该副本进行交易  -1则不能
        self._duel=0          #允许角色之间进行战斗   -1则不允许
        self._autoWay=0       #该副本内允许自动寻路  -1不允许自动寻路
        self._inSceneid=2000     #角色进入副本后所在的场景id
        self._outSceneid=1001    #角色退出副本后所在的Id
        self._areasceneid=-1      #副本所在的区域场景id
        self._dropoutid=-1      #副本掉落表主键id
        self.instanceClose=None #触发副本关闭流程的条件
        self.activation=None #副本的激活条件实例 
        self.colonize=None #副本殖民
        self._numbers=1 #副本建议人数
        self.cards = None#SceneCardComponent(self)                   #卡片信息
        self.islq=True#是否可以领取奖励（斗气）
        self.initInstance()

             
    @property
    def templateInfo(self):
        from app.scense.applyInterface import instance_app
        return instance_app.allInfo.get(self._id)
    
    def initInstance(self):
        '''初始化副本
        @param id: int 副本Id
        '''
        info=self.templateInfo
        if not info:
            pass
        self.islq=True
        self._name=info['name']
        self._typeid=info['typeid']   #副本类型
        self._hard=info['hard']   #副本难度  1普通 2精英  3英雄
        self._sceneid=eval("["+info['sceneid']+"]") #副本你所有场景Id
        self._starttime=info['startime']  #副本开始时间
        self._endtime=info['endtime']    #副本结束时间
        self._uplevle=info['uplevle']    #角色等级上限
        self._downlevle=info['downlevle']   #角色等级下限
        self._props=eval("["+info['props']+"]")      #开启副本所需要的道具Id列表
        self._astrictguild=info['astrictguild'] #此副本只允许该行会成员进入  1只允许同行会的在一个副本
        self._pknum=info['pknum']        #pk值限制 -1无限制
        self._energy=info['energy']       #进入副本所需要的活力值
        self._teamState=info['teamState']    #组队限制 -1无限制   2组队才能进入  3非组队方可进入
        self._teammax=info['teammax']      #组队最大人数限制
        self._teammin=info['teammin']       #组队最小人数限制
        self._carry=info['carry']         #表示该副本允许玩家使用传送技能或道具进入 -1则不能
        
        self._achieveprop=eval("["+info['achieveprop']+"]")  #通过副本后获得的道具列表
        self._teamastrict=info['teamastrict']  #进入该副本后能否组队
        self._noprop=eval("["+info['noprop']+"]")       #副本内禁用道具列表
        self._backCity=info['backCity']      #表示可以使用道具技能回城 -1 表示不能使用道具技能回城
        self._annal=info['annal']        #表示可以使用路点记录道具记录副本和坐标  -1不能记录副本及其坐标
        self._bargain=info['bargain']       #允许玩家在该副本进行交易  -1则不能
        self._duel=info['duel']         #允许角色之间进行战斗   -1则不允许
        self._autoWay=info['autoway']       #该副本内允许自动寻路  -1不允许自动寻路
        self._inSceneid=info['insceneid']    #角色进入副本后所在的场景id
        self._inSoruceid=self.getSceneSourceid(self._inSceneid) #角色进入副本后所在的场景资源id
        self._outSceneid=info['outsceneid']    #角色退出副本后所在的Id
#        self._outSourceid=self.getSceneSourceid(self._outSceneid) #角色退出副本后所在的场景资源id
        self._numbers = info['numbers'] #副本建议人数
        self._dropoutid=info['dropoutid'] #副本掉落表主键id
        self.activation=InstanceActivation(info['activateid']) #激活副本的条件
        self.colonize=InstanceColonize(self._id) #副本殖民
        self.instanceClose=InstanceClose(info['closeid']) #触发副本关闭流程的条件
        self._lastSceneid=0 #副本中最后一个场景的id
        self.cards = SceneCardComponent(self)
        self.cards.initCards(self._id, self._dropoutid, CARD_NUM)
        self.initScene() #初始化副本内所有场景
        
        #print "初始化副"+self._name+"本完成"
        
    def initScene(self):
        '''初始化场景'''
        self._lastSceneid=self._sceneid[len(self._sceneid)-1]#最后一个场景的id
        groupid=InstanceGroupManage().getFristInstanceBy(self._id)
#        #print str(self._name)+"副本最后一个场景id: "+str(endid)
        for l in self._sceneid:
            ss=InstanceScene(l,group=groupid)
            if l==self._lastSceneid:
                self._Scenes[ss._id]=ss #场景 self._Scenes[场景id]=场景实例
                self._Scenes[ss._id]._isend=True #是否是副本中的最后一个场景
            else:
                self._Scenes[ss._id]=ss
#        print ""

    def getOutSceneid(self):
        return self._outSceneid
    
    def getSceneSourceid(self,id):
        '''根据场景id获取场景资源id'''
        resourceid=dbScene.getStringInSceneByFilename("id", id, "resourceid")["resourceid"]
        return resourceid
    
    def setOutSceneid(self,id):
        self._outSceneid=id
    
    def getId(self):
        return self._id
    def setId(self,id):
        self._id=id
    
    def getTag(self):
        return self._tag
    def setTag(self,id):
        self._tag=id
    
    def getScene(self,id):
        '''根据场景Id获取场景实例'''
        if self._Scenes[id]:
            return self._Scenes[id]
        return None
        
    def getSceneResourceidByid(self,id):
        '''根据场景id获取场景资源id(只适用于副本中的场景实例)'''
        if self._Scenes[id]:
            return self._Scenes[id]._resourceid
        return -1
        
        
        
    def Instanceenterplay(self,player,sceneid):
        '''
        @param player: object 角色对象
        @param sceneid: int 目标场景Id
        '''
        target= self._Scenes[sceneid] #目标场景
        oldsceneid= player.baseInfo.getTown() #获取角色的场景
        old= self._Scenes[oldsceneid] #当前场景实例
        old.dropPlayer(player.baseInfo.id) #在当前场景中移除角色
        target.addPlayer(player) #在目标场景中加入角色
        player.baseInfo.setLocation(sceneid) #设置角色当前场景
        player.quest.setNpcList(target._npcids)
        player.baseInfo.setPosition(target.baseInfo.getInitiaPosition()) #设置角色在场景中的初始化位置
        pushObjectNetInterface.pushEnterPlace(target.baseInfo.id,player.getDynamicId()) #推送副本消息
        
    def skipScene(self,characterid,sceneid):            
        '''副本内跳转场景
        @param characterid: int 角色Id
        @param sceneid: int 场景Id
        '''
        player= PlayersManager().getPlayerByID(characterid)#获取角色
        if not player:
            return {'result':False,'message':Lg().g(199)}
        scene1=self._Scenes.get(player.baseInfo.getLocation())#获取角色当前所在场景实例
        data=None
        if len(scene1._monsters)>0: #如果副本中的怪物没有清空
            if self._Scenes[sceneid]._bossInSceneId!=-1:
                data={'placeId':self._Scenes[sceneid]._resourceid,'isboos':True,'copySceneId':self._id,'sceneType':2}
            else:
                data = {'placeId':self._Scenes[sceneid]._resourceid,'isboos':False,'copySceneId':self._id,'sceneType':2}
            return {'result':False,'message':Lg().g(559),'data':data}
            
        #start角色有队伍境况下组队进入副本
        if player.teamcom.amisteam(): #如果角色有队伍
            members=player.teamcom.getMyTeamMember() #获取队伍成员列表 
            if members:
                if len(members)>1:
                    for py1 in members: #遍历所有队员
                            self.Instanceenterplay(py1,sceneid) #角色进入副本操作
        #end  角色有队伍境况下组队进入副本 
        else:#如果角色没有队伍
            self.Instanceenterplay(player,sceneid) #角色进入副本操作
        if self._Scenes[sceneid]._bossInSceneId!=-1:
            data={'placeId':self._Scenes[sceneid]._resourceid,'isboos':True,'copySceneId':self._id,'sceneType':2}
        else:
            data = {'placeId':self._Scenes[sceneid]._resourceid,'isboos':False,'copySceneId':self._id,'sceneType':2}
        
        return {'result':True,'message':u'副本内跳转场景','data':data}
            
    def pushInstanceInfo(self):
        '''推送场景里面的所有场景'''
        
        for item in self._Scenes.values():
            item.pushSceneInfo()
            
    def ishavingplayer(self):
        '''判断该副本内是否还有角色'''
        playernum=0
        for item in self._Scenes.values():
            for it in item._players.values():
                if it:
                    playernum+=1
        if playernum>0:
            return True
        return False
    