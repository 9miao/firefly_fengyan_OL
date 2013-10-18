#coding:utf8
'''
Created on 2011-6-14

@author: SIOP_09
'''

from app.scense.core.instance.InstanceManager import InstanceManager
from app.scense.core.map.MapManager import MapManager
from app.scense.core.PlayersManager import PlayersManager
from app.scense.core.instance.InstanceGroupManage import InstanceGroupManage

from app.scense.component.mail import Mail
from twisted.python import log

from app.scense.netInterface import pushObjectNetInterface
import time
from app.scense.utils import dbaccess
from twisted.internet import reactor

from app.scense.applyInterface import instance_d
from app.scense.core.guild.GuildManager import GuildManager
from app.scense.serverconfig.chatnode import chatnoderemote
import cPickle
import math
from app.scense.utils.dbopera import dbInstance_record_id
from app.scense.core.instance.RqManage import RqManage
from app.scense.core.language.Language import Lg


allInfo={} #所有副本信息
reactor = reactor



def enterplay(player,instanceId,Instan1):
    '''角色进入副本操作
    @param player: object 角色id
    @param instanceId: int 角色当前场景id（公共场景中的）
    @param Instan1: object 副本实例
    '''
    scene1= Instan1._Scenes[Instan1._inSceneid] #获取副本中的初始场景
    if not scene1:
        return {'result':False,'message':u'副本中不存在id为'+str(Instan1._inSceneid)+"的场景"}
    if player.attribute.getEnergy()<Instan1._energy:
        return {'result':False,'message':Lg().g(118)}

    scene1.addPlayer(player.baseInfo.id) #将角色添加到该场景中
    player.baseInfo.initPosition(scene1.getInitPosition())
    player.baseInfo.setLocation(scene1.getID()) #设置玩家所在副本的场景id
    player.baseInfo.setState(1) # 0表示玩家在普通场景       1表示玩家在副本    2行会战副本
    player.baseInfo.setInstanceid(Instan1.getId()) #副本id #用以寻找副本组id
    player.baseInfo.setInstancetag(Instan1.getTag())
    #扣掉活力值
    player.attribute.updateEnergy(player.attribute.getEnergy()-Instan1._energy)
   
def enterInstance1(player,dynamicId,characterId,instanceId,famId):
    '''进入副本 
    @param dynamicId: int  角色动态Id
    @param characterId: int 角色Id
    @param instanceId: int 副本Id
    '''

    player=PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    if player.baseInfo.getState==1: #角色在副本中
        return  {'result':False,'message':Lg().g(114)}
    player.startAllTimer()
    Instan1= InstanceManager().addInstance(instanceId,famId) #把副本添加到副本管理器中,返回副本管理器中的这个副本实例
    scenename = Instan1._name
    chatnoderemote.callRemote('JoinRoom',characterId,famId,scenename)
#    Instan1.setTag(famId)
    if not Instan1:
        return {'result':False,'message':u'没有id为%d的副本'%instanceId}
    activationInstance(Instan1, player) #激活副本
    enterplay(player,instanceId,Instan1) #角色进入副本操作
    data = {'placeId':Instan1.getSceneResourceidByid(Instan1._inSceneid)}
    player.baseInfo.setInstanceid(instanceId)
    return {'result':True,'message':u'进入副本成功','data':data} #返回副本初始Id


def messageClose(Instan1,player,count):
    '''提示关闭副本
    @Instan1 副本实例
    @player 角色id
    '''
    if not Instan1:
        return
    if count==0:
        return
    
    playersid=[] #副本内的对象id列表
    for item in Instan1._Scenes.values():
        for it in item._playerlist:
            playersid.append(it)
    if len(playersid)<1:
        return
    
    if count==4:
            reactor.callLater(300,messageClose,Instan1,player,3)
    if count==3:
        reactor.callLater(120,messageClose,Instan1,player,2)
    if count==2:
        reactor.callLater(120,messageClose,Instan1,player,1)
    if count==1:
        reactor.callLater(60,messageClose,Instan1,player,-1)
    if count==-1:
        pass


def iteranceInstance(characterId):
    '''重打副本'''
    player= PlayersManager().getPlayerByID(characterId) #获取角色
    if not player:
        return {'result':False,'message':Lg().g(18)}
    instanceId=player.baseInfo.getInstanceid() #获取角色所在副本Id
    
    tag=player.baseInfo.getInstancetag() #副本动态Id
    Instance=InstanceManager().getInstanceByIdTag(tag) #获取 副本
    if not Instance:
        log.err(u"不存在副本动态id %s"%tag)
    Instance.initInstance() #初始化副本
    #start角色有队伍境况下组队进入副本
    loaduser=[]#记录需要推送消息的角色对象
    if player.teamcom.amisteam(): #如果角色有队伍
        if player.teamcom.amITeamLeader(): #判断是否是队长
            sceneid=player.baseInfo.getLocation() #获取队长当前场景Id
            members=player.teamcom.getMyTeamMember() #获取队伍成员列表 
            if members:
                if len(members)>1:
                    for py1 in members: #遍历所有队员
                        if py1.baseInfo.getLocation()==sceneid:#判断当前角色是否和队长在同一个场景中
                            enterplay(py1,instanceId,Instance) #角色进入副本操作
                        else:#若该成员和队长不在同一场景,推送是否进入副本提示框消息
                            loaduser.append(py1.getDynamicId())
                    pushObjectNetInterface.pushLeaderInstance(loaduser,player.baseInfo.getId())
        else:#如果请求的人有队伍并且不是队长
            return {'result':False,'message':u'在队伍中的成员中只有队长才能开启副本'}
    #end  角色有队伍境况下组队进入副本 
    else:
        enterplay(player,instanceId,Instance) #角色进入副本操作
    data = {'placeId':Instance.getSceneResourceidByid(Instance._inSceneid)}
    return {'result':True,'message':u'进入副本','data':data}
    
def dropInstanceAllplayer(did,tag):
    '''如果副本内没有角色那么销毁该副本
    @param did: int 副本id
    @param tag: int 副本动态id
    '''
    Instan1=InstanceManager().getInstanceByIdTag(tag)#获取副本实例
    if not Instan1.ishavingplayer():#如果副本内没有角色的话
        InstanceManager().dropInstanceById(tag)
    
def closeInstance(dynamicId,characterId):
    '''关闭副本
    @param characterId: int  角色Id
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False}
    tag=player.baseInfo.getInstancetag() #副本动态Id
    if not tag:
        return {'result':False}
    InstanceManager().dropInstanceById(tag)
    sceneId = player.baseInfo.getTown()
    scene = MapManager().getMapId(sceneId)
    scene.addPlayer(characterId)
    player.quest.setNpcList(scene._npclist)
    player.baseInfo.setInstancetag(0)
    player.baseInfo.setState(0)
    scene.pushEnterPlace([dynamicId])
#    player.updatePlayerDBInfo()#将角色信息写入数据库
#    player.stopAllTimer()#停止所有定时器
    return {'result':True}

#def getAllInstancesByAreaSceneid(id):
#    '''根据区域场景id获取副本列表
#    @param characterid：int 用户角色id
#    @param id: int 副本所在的区域的场景id
#    '''
#    from core.instance import Instance
##    player = PlayersManager().getPlayerByID(characterid)
##    if not player:
##        return {'result':False,'message':Lg().g(18)}
#    
#    data=[]
#    instances = dbaccess.getAllInstanceByAreaSceneid(id)
#    for id in instances:
#        list={}
#        info=Instance(id)#获取副本信息
#        list['name']=info._name
#        list['id']=info.getId()
#        list['numbers']=info._numbers#副本建议人数
#        list['score']=-1
#        list['state']=-1
##        if activationInstance(info, player):
##            list['state']=1  # -1没激活  1激活  2通关
##
##        result=dbaccess.getisInstanceRecord(characterid, id)
##        if result:#如果不为空
##            list['state']=2 # -1没激活  1激活  2通关
##            list['score']=result #添加评分属性
#
#        data.append(list)
#    return {'result':True,'message':u'获取当前场景中的所有副本信息成功','data':data}

def getAllInstances(characterid,csz):
    '''通过传送阵id获取所有副本信息
    @param characterid: int 角色id
    @param csz: int 传送阵id
    '''
    from app.scense.core.instance.ColonizeManage import ColonizeManage
    from app.scense.core.instance.Instance import Instance
    gid=2 #2表示角色没有国   3表示国等级1级   4表示国等级3级
    player = PlayersManager().getPlayerByID(characterid)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    
    if player.attribute.getEnergy()<5:
        pushObjectNetInterface.pushOtherMessage(905, Lg().g(117), [player.getDynamicId()])
        return{'result':False,'message':Lg().g(117)}

    guildLevel= player.guild.getGuildLevel()#行会等级
    if guildLevel>=1 and guildLevel<3:
        gid=3
    elif guildLevel>=3:
        gid=4
    
    
    data=[]
    cszGroupList=InstanceGroupManage().getInstanceGroupBycszid(csz) #获取副本组信息列表
    for itm in cszGroupList:
        tlist={}
        info=Instance(itm['levela'])#获取副本信息

        tlist['id']=itm['id']
        tlist['score']=-1
        tlist['instanceList']=[itm['levela'],itm['levelb'],itm['levelc']]
        tlist['drop']=[]
        tlist['stateList']=[]
        for inf in [itm['levela'],itm['levelb'],itm['levelc']]:
            dropinfo=instance_d.getMonsterItemByid(inf)
            va={}
            va['dropitem']=dropinfo.get('data')['dropitem']
            va['moster']=dropinfo.get('data')['moster']
            tlist['drop'].append(va)
            
#            rs22=dbInstance_record_id.getisInstanceRecord(characterid, inf)
            rs22=player.instance.isFamClean(inf)#副本是否通关
            if rs22:
                tlist['stateList'].append(1) #1通关
            else:
                tlist['stateList'].append(-1) #-1没通关
            
        tlist['state']=-1
        if activationInstance(info, player): 
            tlist['state']=1  # -1没激活  1激活  2通关
#        result=dbaccess.getisInstanceRecord(characterid, itm['id'])
        result=player.instance.isGroupClean(itm['id'])
        if result:#如果不为空
            tlist['state']=2 # -1没激活  1激活  2通关
            tlist['score']=-1 #添加评分属性
        colonize=ColonizeManage().getInstanceInfoByid(itm['id'])
        if colonize['pid']>0:
            tlist['leader_id']=colonize['pid'] #角色id
            tlist['leader_name']=colonize['pname'] #角色名称
            tlist['union_id']=colonize['gid'] #国id
            tlist['union_name']=colonize['gname'] #国名称
            if colonize['gid']>0:
                tlist['camp']=GuildManager().getGuildById(colonize['gid']).guildinfo['camp'] #0中立  1光明  2黑暗
            else:
                tlist['camp']=0
        else:
            tlist['union_id']=0 #国id
            tlist['leader_id']=0 #角色id
            tlist['union_name']=u"" #国名称
            tlist['leader_name']=u"" #角色名称
            tlist['camp']=0 #0中立  1光明  2黑暗
        data.append(tlist)
        del info
        
    return {'result':True,'message':u'获取所有副本信息','data':data,'guild':gid}


def getCsz(csz,pid):
    '''通过传送阵id获取所有副本信息
    @param csz: int 传送阵id
    @param pid: int 角色id
    '''
    from app.scense.core.instance.ColonizeManage import ColonizeManage
    data=[]
    cszGroupList=InstanceGroupManage().getInstanceGroupBycszid(csz) #获取副本组信息列表
    player=PlayersManager().getPlayerByID(pid)#角色
    gid=player.guild.getID()#角色的id
    for itm in cszGroupList:
        tlist={}
        info=allInfo.get(itm['levela'])
        tlist['name']=info['name']#副本名称
        tlist['id']=itm['levela']#副本组中第一个副本的id

        colonize=ColonizeManage().getInstanceInfoByid(itm['id'])
        if colonize['pid']>0:
            tlist['leader_id']=colonize['pid'] #角色id
            tlist['leader_name']=colonize['pname'] #角色名称
            tlist['union_id']=colonize['gid'] #国id
            tlist['union_name']=colonize['gname'] #国名称
            if colonize['gid']>0: #如果这个副本占领者有行会
                tlist['camp']=GuildManager().getGuildById(colonize['gid']).guildinfo['camp'] #0中立  1光明  2黑暗
                if gid>0:#如果当前角色有行会
                    if colonize['gid']==gid:
                        tlist['coloType']=1 #自己行会占领
                    else:
                        tlist['coloType']=2 #其他国占领
                else:#如果当前角色没有行会
                    tlist['coloType']=2 #自己行会占领
                    
            else:
                tlist['camp']=0
                tlist['coloType']=0 #没有被国占领
        else:
            tlist['union_id']=0 #国id
            tlist['leader_id']=0 #角色id
            tlist['union_name']=u"" #国名称
            tlist['leader_name']=u"" #角色名称
            tlist['camp']=0 #0中立  1光明  2黑暗
            tlist['coloType']=0 #没有被国占领
        data.append(tlist)
        del info
        
    return {'result':True,'message':u'获取所有副本信息','data':data}


def validateInstance(instance,player):
    '''玩家是否符进入副本限制
    @param instance: object 副本实例
    @param player: object 角色实例
    '''
    #------------------------------要分 1个人进入副本和组队团队进入副本的情况
    #副本开始/结束时间判断
    time_format = "%H:%M:%S"
    starttime=time.strptime(str(instance._starttime),time_format) #副本开启时间
    nowtime=time.strptime(time.strftime('%H:%M:%S'),time_format) #当前时间
    endtime=time.strptime(str(instance._endtime),time_format) #副本结束时间
    if str(instance._starttime)=='0:00:00' and str(instance._endtime)=='0:00:00':
        pass #说明没有限制
    else:
        if nowtime<starttime or nowtime>endtime:
            #print '此副本还未到开始时间'
            return {'result':False,'message':u'此副本还未到开始时间'} 
    
    #角色等级判断
    uplevle=instance._uplevle #副本等级上限 最大值
    downlevle=instance._downlevle#副本等级下限 最小值
    plevle=player.level.getLevel()#角色等级
    if (uplevle==-1 and downlevle)==-1 or uplevle==-1:
        pass #说明没有限制
    else:
        if plevle>uplevle or plevle<downlevle:
            #print'不满足副本等级限制'
            return {'result':False,'message':u'不满足副本等级限制需要'+str(uplevle)+' - '+ str(downlevle)} 

    #开启副本所需道具限制
#    props=instance._props #[]
    
    #行会要求
    astrictguild=instance._astrictguild #副本行会等级限制
    if astrictguild!=-1:
        info=player.guild.getGuildInfo()
        if(not info) or (not info.get('result',False)):
            #print "该角色没有加入行会"
            return {'result':False,'message':u'不满足副本行会等级限制'}
        else:
            levle=info['level'] #角色的行会等级
            if levle<astrictguild:
                #print'不满足副本行会等级限制'
                return {'result':False,'message':u'不满足副本行会等级限制'} 
    
    #组队进入限制
    teamState=instance._teamState #1=均可进入；2=组队方可进入 3=非组队状态方可进入
    if teamState==2:
        if not player.teamcom.amisteam():#如果角色没有队伍
            #print'角色没有队伍'
            return {'result':False,'message':u'角色没有队伍，不能进入副本'} 
    if teamState==3:
        if player.teamcom.amisteam():#如果角色有队伍
            #print'角色有队伍'
            return {'result':False,'message':u'角色当前有队伍，不能进入副本'}
        
    if player.teamcom.amisteam():#如果角色有队伍 
        #队伍人数要求
        teammax=instance._teammax #副本最大队伍人数
        teammin=instance._teammin#副本最小队伍人数
        teamnum=player.teamcom.getMyTeamNumb()#获取队伍人数
        if teammax==-1 and teammin==-1:
            pass
        else:
            if (teamnum>teammax and teammax!=-1) or (teamnum<teammin and teammin!=-1):
                #print'队伍人数不符合副本限制'
                return {'result':False,'message':u'队伍人数不符合副本限制，不能进入副本'} 
    
    #传送进入限制
#    carry=instance._carry
    
    #pk值是否符合要求
#    pknum=instance._pknum #副本所需要的pk值
    
    #活力值是否符合要求
    energy= player.attribute.getEnergy()#玩家的活力值
    instanceenergy=instance._energy #副本需要的活力值
    if instanceenergy>0:
        if energy>=instanceenergy:
            #数据库减去晚间活力值
            #角色管理器里面减去玩家活力值
            pass
        else:
            #print'玩家活力值不够'
            return {'result':False,'message':Lg().g(118)}
    

def activationInstance(instance,player):
    '''玩家是否可以激活该副本 (激活副本之后角色才能在地图中看到这个副本)
    @param instance: object 副本实例
    @param player: object 玩家信息
    '''
    #验证角色等级
    characterlevel=player.level.getLevel()#角色当前等级
    insplayerlevel=instance.activation.characterlevel #副本角色等级限制
    if insplayerlevel!=-1:
        if insplayerlevel>characterlevel:
            instance=None
            return False
            return {'result':False,'message':u'次副本要求角色等级为%d'%insplayerlevel} 
    #验证角色公会等级
    guildlevel=10 #角色的行会等级
    insguildlevel=instance.activation.guildlevel #副本行会等级限制
    if insguildlevel!=-1:
        if guildlevel<insguildlevel:
            instance=None
            return False
            return {'result':False,'message':u'次副本要求所在行会等级为%d'%insguildlevel} 
    
    #玩家获得的成就Id
    
    #已通过的副本Id
    instanceid=instance.activation.instanceid #已通关的副本id
    if instanceid!=-1:
        data=dbaccess.getInstanceRecordInfo(player.baseInfo.id, instanceid)
        if not data:
#            print"不满足副本激活条件,没有通过%d副本"%instanceid
            instance=None
            return False
            return {'result':False,'message':u'次副本要求所在行会等级为%d'%insguildlevel}
        #print "满足副本激活条件,通过%d副本"%instanceid
        
    #已接受的任务Id
    if instance.activation.accepttaskid>0:
        if not player.quest.IsTaskInAccept(instance.activation.accepttaskid):
#            print str(instance._name)+"副本 :   没有接受任务%d"%instance.activation.accepttaskid
            instance=None
            return False
        
        #已完成的任务Id
        if not player.quest.hasTaskCommited(instance.activation.finishtaskid):
#            print str(instance._name)+"副本 :   没有完成任务%d"%instance.activation.finishtaskid
            instance=None
            return False
    
    dts=validateInstance(instance, player)#验证是否满足副本需求
    if dts:
        if not dts.get('result',False):
            return False
    
    #已获得的物品Id
    instance=None
    return True

#def validateInstanceClose(instance,player):
#    '''验证是否满足副本关闭条件
#    @param instance: object 副本实例
#    @param player: object 角色实例
#    '''
#    flg=0
#    from utils.dbopera import dbtask
#    attackboss=instance.instanceClose.attackboss #打败的boss的id
#    taskid=instance.instanceClose.taskid #完成的任务id
#    if attackboss!=-1:
#        #此处验证是否打败那个boss
#        instance=None
#        pass
#    if taskid!=-1:
#        #此处验证是否完成过此任务
#        list=dbtask.getHasCommitQuestList(player.baseInfo.id)
#        instance=None
#        if list.count(taskid)>0:
#            return True
#        else:
#            return False

def addInstance_record(characterid,instanceid,score=-1):
    '''添加角色通关记录
    @param characterid:int 角色id
    @param instanceid: int 副本组id 
    '''
    player=PlayersManager().getPlayerByID(characterid) #当前角色实例
#    sid=dbaccess.getisInstanceRecord(characterid, instanceid)
    sid=player.instance.isGroupClean(instanceid)
    if not sid: #如果通关记录里面没有,加入通关副本
        if player.instance.addGroupClear(instanceid):#如果添加通关副本成功
#        if dbaccess.insertInstanceRecord(characterid, instanceid):#如果添加通关副本成功
            pushObjectNetInterface.pushOtherMessage(905, Lg().g(119), [player.getDynamicId()])
#            UnionTypeStr = player.guild.getUnionTypeStr()+Lg().g(129)
#            playername = player.baseInfo.getName()
#            instanceinfo = allInfo.get(instanceid)
#            hardinfo = {1:u'普通',2:Lg().g(282),3:Lg().g(283)}.get(instanceinfo.get('hard',0))
#            instansname = instanceinfo.get('name') +"-"+ hardinfo
#            sendstr = u"【%s】的强者【%s】通关了【%s】"%(UnionTypeStr,
#                                            playername,instansname)
#            chatnoderemote.callRemote('pushSystemToInfo',sendstr)
        else:
            pushObjectNetInterface.pushOtherMessage(905, u'通关副本添加失败', [player.getDynamicId()])
            
def addInstance_record_id(characterid,instanceid,score=-1):
    '''添加角色通关记录
    @param characterid:int 角色id
    @param instanceid: int 副本id 
    '''
    player=PlayersManager().getPlayerByID(characterid) #当前角色实例
    tag=player.baseInfo.getInstancetag()
    instance=InstanceManager().getInstanceByIdTag(tag)
    
    sid=dbInstance_record_id.getisInstanceRecord(characterid, instanceid)
    if not sid: #如果通关记录里面没有,加入通关副本
        if not player.instance.addClean(instanceid):#如果添加通关副本成功
#        if not dbInstance_record_id.insertInstanceRecord(characterid, instanceid):#如果添加通关副本成功
            log.err(u"instance_app/addInstance_record_id 添加通关记录失败")
        else:
            if instance.islq:
                player.finance.updateAddMorale(20,True)
                instance.islq=False
            player.schedule.noticeSchedule(19,goal = 1)
    else:
        if instance.islq:
            player.finance.updateAddMorale(2,True)
            instance.islq=False
    
    player.daily.noticeDaily(6,instanceid,1)
            

def objectVal(tid,iname,fid,flg,tname,fname):
    '''
    @param tid: int 挑战方id
    @param iname: int 副本id
    @param fid: int 元始领主id
    @param flg: int 殖民是否成功 True or False 
    return [item,item,...]
    '''
    from app.scense.core.character.PlayerCharacter import PlayerCharacter
    playert = PlayersManager().getPlayerByID(tid) #挑战方角色实例
    playerf = PlayersManager().getPlayerByID(fid)#元始领主角色实例
    content=u''
    if not playerf:
        playerf=PlayerCharacter(fid) #原始领主角色实例
    if flg:#如果挑战成功；挑战方取得胜利，元始领主掉落
        content=Lg().g(121)%(iname,tname)
        itemList=playerf.pack.LostItem()#返回防守方掉落结果   #return [item,...]
        if len(itemList)>0:
            content+=Lg().g(122)
        for item in itemList: #挑战成功获得物品列表
            rs= playert.instance.putNewItemInPackage(item)#如果背包满了
            if rs:
                content+=u'[%s+%s]'%(item.baseInfo.getName(),item.attribute.getStrengthen())
        instancecount=playert.instance.pack.findSparePositionNum()
        if instancecount<=3 and instancecount>0:
            playert.msgbox.putFightTMsg(Lg().g(123)%str(instancecount))
        if instancecount<=0:
            playert.msgbox.putFightTMsg(Lg().g(124))
    else:
        content=Lg().g(125)%iname
        itemList=playert.pack.LostItem()#返回挑战方掉落结果   #return [item,...]
        if len(itemList)>0:
            content+=Lg().g(126);
        for item in itemList: #挑战成功获得物品列表
            rs=playerf.instance.putNewItemInPackage(item)
            if rs:#如果添加物品成功
                content+=u'[%s+%s]'%(item.baseInfo.getName(),item.attribute.getStrengthen())
    Mail.sendMail(Lg().g(127), -1, Lg().g(128), fid, content, 1)
    return itemList

def dropItem(cid,instanceid,battle,iname): #进入殖民战瞬间所做的
    from app.scense.applyInterface import   defencelog_app,instanceColonizeChallenge
    from app.scense.applyInterface import  InstanceColonizeGuerdon
    from app.scense.core.instance.WinManager import WinManager
    from app.scense.applyInterface import winning_app
    from app.scense.core.instance.ColonizeManage import ColonizeManage
    from app.scense.core.character.PlayerCharacter import PlayerCharacter
    player=PlayersManager().getPlayerByID(cid) #挑战方角色
    zyname=player.guild.getUnionTypeStr()+Lg().g(129)#获取阵营名称
    pname=player.baseInfo.getName()
    instancegroupid=InstanceGroupManage().getFristInstanceBy(instanceid) #副本组id
    instanceinfo=ColonizeManage().getInstanceInfoByid(instancegroupid) #根据副本组id获取副本殖民信息
    pid=instanceinfo['pid']#元始领主的角色id#通过副本组id获取占领者id pid<0表示这个副本的领主是怪物
#    gid=0
#    gname=Lg().g(143)
#    if player.guild.getID()>0:
#        gid=player.guild.getID()
#        gname=player.guild.getGuildName()
    plv=player.level.getLevel()
    player2=None#原始领主实例
    p2name='' #元始领主角色名称
    datas=None #返回掉落信息
    if pid>0:#如果挑战者挑战其他角色
        p2name=instanceinfo['pname'] #元始领主角色名称
        datas=objectVal(cid, iname, pid, battle, pname, p2name)
        player2=PlayersManager().getPlayerByID(pid)#元始领主角色
        if not player2:
            player2=PlayerCharacter(pid)
#        winning_app.updateWinning(cid, battle)#设置连胜
    if battle: #殖民是否成功
        player.daily.noticeDaily(23,0,-1)
        if pid<1:#如果此副本没有被殖民，角色打得是怪物
            data = InstanceColonizeGuerdon.addInstanceColonizelog(cid, instancegroupid,iname)
            if data: #添加副本殖民成功
                coin=plv*1000
                player.finance.updateCoin(player.finance.getCoin()+coin,0)
                mname=instanceColonizeChallenge.getMosterNameByinstanceid(instancegroupid)
                mg=Lg().g(130)%(zyname,pname,mname,iname,str(coin));
                
                mmg=Lg().g(131)%(iname,mname,pname)
                ch=WinManager().getName(cid) #获得称号
                if ch:
                    mmg+=Lg().g(132)%ch
                winning_app.addmessage(mmg,type=1,id=instancegroupid)
                plist= ColonizeManage().getprotalBypid(cid)#获取主宰的传送门名称
                if plist and len(plist)>0:
                    for nme in plist:
                        sett=Lg().g(133)%(iname,mname,pname,nme)
                        winning_app.addmessage(sett)
                        player.msgbox.putSystem(sett)
                player.msgbox.putSystem(mg)

        else: #如果此副本被殖民了
#            lev=player2.level.getLevel()-player.level.getLevel()
#            if lev<0:
#                lev=0
#            ww= player.level.getLevel()*13+lev*10#殖民成功获得的威望
            ww= player.level.getLevel()*5#殖民成功获得的威望
            player.finance.updatePrestige(player.finance.getPrestige()+ww,0)
            
#            if player2:
#                defencelog_app.iscolonManage(player2.baseInfo.id, player.getDynamicId()) #刷新挑战者殖民管理图标
            defencelog_app.addDefeated_fail_logTrue(instancegroupid, cid, pname,pid,p2name,instanceinfo['name'])
            defencelog_app.updateColonize(instancegroupid,iname,cid, pid,pname) #更改殖民信息
            WinManager().add(cid)#添加连胜次数
            ColonizeManage().updateWm0(instancegroupid)
            mg=Lg().g(134)%(zyname,pname,p2name,iname)
            player.msgbox.putSystem(mg)
            
            mmg=Lg().g(135)%(iname,p2name,pname)
            ch=WinManager().getName(cid) #获得称号
            if ch:
                mmg+=Lg().g(136)%ch
            winning_app.addmessage(mmg,type=1,id=instancegroupid)
            player.msgbox.putSystem(mmg)
            plist= ColonizeManage().getprotalBypid(cid)#获取主宰的传送门名称

            if plist and len(plist)>0:
                for nme in plist:
                    sett=Lg().g(137)%(iname,p2name,pname,nme)
                    winning_app.addmessage(sett)
                    player.msgbox.putSystem(sett)
           
            
    else:#殖民失败
        if pid>0:##如果此副本被殖民了
#            ww= int(math.ceil((player.level.getLevel()*5.0)))#殖民成功获得的威望
            ww=player.level.getLevel()#殖民成功获得的威望
            player.finance.updatePrestige(player.finance.getPrestige()+ww,0)
            winning_app.updateWinning(pid, True)#增加元始领主连胜次数
#            dcount=winning_app.getWinning(pid)#获取连胜次数
            defencelog_app.addDefeated_fail_log(instancegroupid, cid, pname,pid,p2name,instanceinfo['name'])
            dcount=ColonizeManage().AddWm(instancegroupid)#增加卫冕次数
            RqManage().addSb(instancegroupid, iname, pid, p2name, cid, pname)#添加挑战失败记录
            mg=Lg().g(138)%(zyname,p2name,iname,pname,str(dcount))
            player.msgbox.putSystem(mg)
            ch=WinManager().getName(cid) #获得称号
            if not ch:
                ch=u""
            else:
                ch+=Lg().g(139)
            mmg=Lg().g(140)%(iname,p2name,ch,pname,dcount)
            winning_app.addmessage(mmg,type=1,id=instancegroupid)
            player.msgbox.putSystem(mmg)
            plist= ColonizeManage().getprotalBypid(cid)#获取主宰的传送门名称
            if plist and len(plist)>0:
                for nme in plist:
                    sett=Lg().g(141)%(iname,p2name,nme,pname,dcount)
                    winning_app.addmessage(sett)
                    player.msgbox.putSystem(sett)
            
#            if player2:
#                defencelog_app.iscolonManage(player2.baseInfo.id, player.getDynamicId()) #刷新挑战者殖民管理图标
        else:
            mname=instanceColonizeChallenge.getMosterNameByinstanceid(instancegroupid)
            mg=Lg().g(142)%(zyname,pname,iname,mname)
            player.msgbox.putSystem(mg)
#    defencelog_app.iscolonManage(cid, player.getDynamicId()) #刷新挑战者殖民管理图标
    return datas

def GetCopySceneInfo(pid):
    '''返回副本怪物数量，角色信息以及国信息'''
    from app.scense.core.instance.ColonizeManage import ColonizeManage
    player=PlayersManager().getPlayerByID(pid)
    if not player:
        log.err(u"角色不存在%s"%pid)
        return None
    if player.baseInfo.getState()==1: #如果角色在副本中
        tag=player.baseInfo.getInstancetag()#副本动态id
        sceneid=player.baseInfo.getLocation() #角色所在副本的场景id
        instanceinfo= InstanceManager().getInstanceByIdTag(tag)#副本实例
        sceneinfo=instanceinfo.getScene(sceneid)#副本场景实例
        count=len(sceneinfo._monsters)#怪物数量
        instanceid=instanceinfo.getId()#获取副本id
        data=ColonizeManage().getInstanceInfoByinstanceid(instanceid)
        if data['gid']==0:
            data['gname']=Lg().g(143)
        if data:
            return {'count':count,'pid':data['pid'],'pname':data['pname'],'gid':data['gid'],'gname':data['gname']}
        return None
    return None


def getItemsInFamPackage(dynamicId, characterId):
    '''获取殖民包裹的信息'''
    player=PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'messga':Lg().g(18)}
    packageItemInfo = player.instance.getFamItemInfo()
    return {'result':True,'data':packageItemInfo}

def getPortal(pid,page,count=10):
    '''获取传送门当前页数内容
    @param page: int 当前页数
    @param count: int 每页条数
    '''
    from app.scense.utils.dbopera import dbPortals
    player=PlayersManager().getPlayerByID(pid)
    if player:
        tlist=dbPortals.all#所有传送门信息 []
        zong=len(tlist)#总记录数
        gong=int(math.ceil(float(zong)/float(count))) #总页数
        alla=tlist[(page-1)*count:page*count] #当前页传送阵信息
        return [alla,gong]
    return [None,1]
    
    
    
    
    

