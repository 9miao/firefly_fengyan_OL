#coding:utf8
'''
Created on 2011-12-20
副本殖民操作
@author: SIOP_09
'''
from app.scense.utils.dbopera import dbInstanceColonize,\
    InstanceColonizeGuerdon
from app.scense.core.character.Monster import Monster
from app.scense.core.character.PlayerCharacter import PlayerCharacter
from app.scense.core.PlayersManager import PlayersManager

from twisted.python import log
from app.scense.core.instance.InstanceGroupManage import InstanceGroupManage
from app.scense.core.instance.ColonizeManage import ColonizeManage
from app.scense.core.map.MapManager import MapManager

import random
from app.scense.applyInterface import instance_app, icon_app, configure,instanceColonizeChallenge
from twisted.internet import reactor

#from serverconfig.publicnode import publicnoderemote
from app.scense.world.scene import Scene
from app.scense.core.instance.WinManager import WinManager
from app.scense.netInterface import pushObjectNetInterface
import math
from app.scense.core.language.Language import Lg
reactor = reactor


def getWinningCount(pid):
    data=WinManager().getcount(pid)
    return data
    

def goClonizeGue(cid):
    flg=True
    player=PlayersManager().getPlayerByID(cid) #获取角色实例
    if player.pack._package._PropsPagePack.countItemTemplateId(20030072)==0:#背包中没有此物品
#        pushObjectNetInterface.pushOtherMessage(905, u'背包内缺少战书，无法进入殖民', [player.getDynamicId()])
        flg=False
    else:
        player.pack.delItemByTemplateId(20030072,1)
    return flg

def getBattlePlayer(instanceid,cid):
    '''副本殖民战斗,返回对手实例'''
    from app.scense.core.instance.Instance import Instance
    from app.scense.core.map.MapManager import MapManager
    player=PlayersManager().getPlayerByID(cid) #获取角色实例
    if player.baseInfo._state!=0:#如果在普通场景
        return False,Lg().g(144),False
    
#    cityid=InstanceGroupManage().getcityidBygroupid(instanceid)
#    if player.baseInfo._town!=cityid:
#        pushObjectNetInterface.pushOtherMessage(905, u'只能殖民本场景的副本', [player.getDynamicId()])
#        return False,u'只能殖民本场景的副本',False
    
    if player.level._level<=12:
        return False,Lg().g(145),False
    
    guildLevel= player.guild.getGuildLevel()#当前角色行会等级
    if guildLevel<1:#没有国
        return False,Lg().g(146),False
    
    zmcount=int(math.ceil((guildLevel/5.0)))#可殖民副本数量
    yydata=0#该角色已殖民数量
    for info in ColonizeManage().getI().values():
        if info['pid']==cid:
            yydata+=1
    if zmcount<=yydata:
        pushObjectNetInterface.pushOtherMessage(905, Lg().g(147), [player.getDynamicId()])
        return False,Lg().g(147),False
    
    player.schedule.noticeSchedule(17,goal = 1)
    tlist=[]
    sceneId = player.baseInfo.getTown()
    scene = MapManager().getMapId(sceneId)
    scene.dropPlayer(cid)
    allInfo=instance_app.allInfo
    info=allInfo.get(instanceid)
    downlevel=info.get('downlevle',0)#殖民等级
    if downlevel>player.level.getLevel():#如果角色等级<副本等级要求
        return False,Lg().g(148),False

    instancegroupid=InstanceGroupManage().getFristInstanceBy(instanceid)#根据副本id获取副本组id
    pid=ColonizeManage().getpidByinstanceid(instancegroupid) #通过副本组id获得副本殖民者id
    mosterid=15001
    if pid<1:#如果此副本没有被殖民
        try:
            mosterid=instanceColonizeChallenge.getColonizeChallengeByMosterid(instancegroupid) #获取怪物id
            if mosterid<0:
                log.err(u'殖民战斗当中副本组中没有配置对应的殖民挑战怪物，殖民副本组id为%d'%instancegroupid)
        except Exception as e:
            log.err(u'殖民战斗当中副本组中没有配置对应的殖民挑战怪物，殖民副本组id为%d'%instancegroupid)
            log.err(e.message)
        
        tlist.append(Monster(templateId=mosterid))
    else: #如果此副本被殖民了
        py=PlayersManager().getPlayerByID(pid)
        if not py:
            py=PlayerCharacter(pid)
        tlist.append(py)
    instance= Instance(instanceid) #副本
    scene=instance.getScene(instance._inSceneid) #第一个场景实例
    del instance
    zon=random.randint(500,scene._width-500)
    return tlist,zon,scene.formatSceneInfo() #场景资源id
    
    

def newBattleAward(player):
    '''根据角色实例获得副本殖民挑战boss成功之后的奖励游戏币
    @param player: obj 角色实例
    '''
    level=player.level.getLevel()
    return level*1000
    
def oldBattleAward(player,days,battlecount):
    '''根据角色id和殖民天数(及卫冕成功数量)获得卫冕奖励游戏币---每天24点统计奖励，第二天6点发放奖励
    @param player: obj 角色实例
    @param days: int 卫冕天数
    @param battlecount: int 卫冕成功数量
    '''
    again=1 #奖励倍数
    if battlecount>=20:
        again=1.2
    level=player.level.getLevel()
    return level*1000*days*again
    
    

def updateColonizeGuerdon(player,instance,days,battlecount,typeid):
    '''更新副本殖民奖励(其他角色通过副本奖励)
    @param cid: int 角色id
    @param typeid: int 类型 1卫冕奖励  2其他角色通关奖励
    @param coin: int 奖励玩家的游戏币数量
    '''
    level=player.level.getLevel()#角色等级
    cid=player.baseInfo.getId() #角色id
    hard=instance._hard #副本难度
    now=level*10*hard #应获得的奖励
    max_t=oldBattleAward(player,days+1,battlecount) #最大奖励数量
    GuerdonInfo=InstanceColonizeGuerdon.getInstanceColonizeGuerdon(cid, typeid) #获得奖励信息
    if not GuerdonInfo: #如果没有奖励记录
        if not InstanceColonizeGuerdon.addInstanceColonizeGuerdon(cid, now,typeid):
            log.err(u'添加殖民殖民副本奖励失败')
    else: #如果有奖励
        oldcoin=GuerdonInfo.get("coin") #已经有多少奖励
        if oldcoin==max_t:
            return
        if (oldcoin+now)>max_t: #如果获得奖励大于卫冕奖励
            InstanceColonizeGuerdon.updateInstanceColonizeGuerdon(cid, typeid, max_t) #修改奖励值为最大值
        else: #如果奖励达不到最大奖励
            InstanceColonizeGuerdon.updateInstanceColonizeGuerdon(cid, typeid, oldcoin+now)



def addInstanceColonizelog(cid,instanceid,iname):
    '''添加副本殖民成功记录'''
    player=PlayersManager().getPlayerByID(cid) #获得当前角色
    gid=0
    gname=Lg().g(143)
    if not player:
        log.err(Lg().g(106))
    if player.guild.getID()>0:
        gid=player.guild.getID()
        gname=player.guild.getGuildName()
    ColonizeManage().updateInstancePid(instanceid, cid, player.baseInfo.getName(), gid, gname, iname)
    return True

def getPidByinstanceid(instanceid):
    '''根据副本id获取领主id'''
    instancegroupid=InstanceGroupManage().getFristInstanceBy(instanceid) #根据副本id获取副本组id
    return ColonizeManage().getpidByinstanceid(instancegroupid) #领主id
    
def getInstancenameByinstanceid(instanceid):
    '''根据副本id获取副本名称'''
    info=instance_app.allInfo.get(instanceid)
    return info['name']

def getFightData(cid,list1,zon,instanceid):
    '''获取殖民战斗数据'''
    from app.scense.core.fight import fight_new
#    info=ColonizeManage().getInstanceInfoByinstanceid(instanceid)#城镇副本殖民信息
    val={'extVitper':0,'extStrper':0,'extDexper':0,'extWisper':0,'extSpiper':0,'preVitper':1,'preStrper':1,'preDexper':1,'preWisper':1,'preSpiper':1}
#    if info['property'][1][0]:#如果力量开启
#        val['extVitper']=20
#    if info['property'][2][0]:#如果敏捷开启
#        val['extDexper']=20
#    if info['property'][3][0]:#如果智力开启
#        val['extWisper']=20
#    if info['property'][4][0]:#如果精神开启
#        val['extSpiper']=20
#    if info['property'][5][0]:#如果耐力开启
#        val['extStrper']=20
    player=PlayersManager().getPlayerByID(cid)
##    player=PlayerCharacter(cid)
#    zid= player.profession.getProfession()
#    if zid==1:#战士
#        val['preStrper']=0.6
#        val['preVitper']=1.4
#    elif zid==2:#法师
#        val['preWisper']=1.1
#        val['preSpiper']=1.4
#    elif zid==3:#游侠
#        val['preDexper']=1.2
#        val['preVitper']=1.2
    return fight_new.DoFight([player], list1, zon,val)

def backScnee(pid,instanceid,boo):
    '''角色退出殖民战斗，返回城镇场景
    @param pid: int 角色id
    @param instanceid: int 副本id
    @param boo: bool 战斗结果
    '''
    player=PlayersManager().getPlayerByID(pid)
    player.msgbox.AfterFightMsgHandle()
    sceneId = player.baseInfo.getTown()
    scene = MapManager().getMapId(sceneId)
    scene.addPlayer(pid)
    scene.pushEnterPlace([player.getDynamicId()])
#    sceneId=player.baseInfo.getTown() #获取角色所在的公共场景id
#    scene=SceneManager_new().getSceneById(sceneId) #获取角色所在公共场景实例
#    scene.addPlayer(pid)
    
def getInstanceinfoBypid(pid,page,counts=6):
    '''根据角色id获取殖民副本列表'''
    tlist=[]
#    player=PlayersManager().getPlayerByID(pid)
#    ab=player.attribute
    data,zong=dbInstanceColonize.getInstanceInfoListBypid(pid,page, counts)
    if zong>0:
        for item in data:
            val={}
            val['id']=item['instanceid']
            val['name']=item['instancename']
            val['state']=getypjc(item['instanceid'])#存储状态开启及其剩余时间
            val['liliang']=10#int(ab.getLevelStr())
            val['minjie']=10#int(ab.getLevelDex())
            val['zhili']=10#int(ab.getLevelWis())
            val['naili']=10#int(ab.getLevelVit())
            val['jingshen']=120#int(ab.getLevelSpi())
            val['jialiliang']=0
            val['jiaminjie']=0
            val['jiazhili']=0
            val['jianaili']=0
            val['jiajingshen']=0
            w={'extVitper':0,'extStrper':0,'extDexper':0,'extWisper':0,'extSpiper':0}
            if val['state'][1]['status']:
                val['jialiliang']=20
                w['extVitper']=20
            if val['state'][2]['status']:
                val['jiaminjie']=20
                w['extDexper']=20
            if val['state'][3]['status']:
                val['jiazhili']=20
                w['extWisper']=20
            if val['state'][4]['status']:
                val['jianaili']=20
                w['extVitper']=20
            if val['state'][5]['status']:
                val['jiajingshen']=20
                w['extSpiper']=20
            val['wugong']=10#int(ab.getCurrPhyAtt(w))
            val['wufang']=10#int(ab.getCurrPhyDef(w))
            val['mogong']=10#int(ab.getCurrMigAtt(w))
            val['mofang']=10#int(ab.getCurrMigDef(w))
            val['gongsu']=10#int(ab.getCurrSpeed(w))
            val['mingzhong']=10#int(ab.getCurrHitRate(w))
            val['baoji']=10#int(ab.getCurrCriRate(w))
            val['shanbi']=10#int(ab.getCurrDodge(w))
            tlist.append(val)
    return tlist,zong
        
def gettime():
    '''获取当前时间 datetime'''
    import datetime,time
    return datetime.datetime.fromtimestamp(time.time())


def addAllProperty(groupid,itemid,tagid,pid):
    '''添加所有属性加成'''
    for i in [1,2,3,4,5]:
            Preperty(groupid, i, tagid, pid)
    player=PlayersManager().getPlayerByID(pid)#角色实例
    count=player.finance.getGold()#角色拥有的钻
    if count>=500:
        player.finance.updateGold(count-500)
            
def addProperty(groupid,itemid,tagid,pid):
    '''给副本组添加属性加成
    @param groupid: int 副本组id
    @param itemid: int 加成物品（1力量、2敏捷 、3智力、4精神、5耐力）
    @param tagid: int 角色动态id
    '''
    Preperty(groupid, itemid, tagid, pid)
    player=PlayersManager().getPlayerByID(pid)#角色实例
    count=player.finance.getGold()#角色拥有的钻
    if count>=100:
        player.finance.updateGold(count-100)

def Preperty(groupid,itemid,tagid,pid):
    instanceinfo= ColonizeManage().getInstanceInfoByid(groupid)
    if instanceinfo['property'][itemid][0]:#如果时间还有没到
        instanceinfo['property'][itemid][1]=gettime()
        instanceinfo['property'][itemid][2].cancel()#取消定时器
        instanceinfo['property'][itemid][3]=False#设置状态>30分钟
        dsq=reactor.callLater(configure.instanceStatus-configure.instanceStatusPrompt,changeimg,tagid,groupid,itemid,pid)#开始一个新的定时器
        instanceinfo['property'][itemid][2]=dsq
    else:#如果时间到了
        instanceinfo['property'][itemid]=[True,gettime(),None,False]
        dsq=reactor.callLater(configure.instanceStatus-configure.instanceStatusPrompt,changeimg,tagid,groupid,itemid,pid) #30分钟的时候推送流光溢彩
        instanceinfo['property'][itemid][2]=dsq
#    publicnoderemote.callRemote('updateColonizeManage',ColonizeManage().citys,ColonizeManage().instancetocity,ColonizeManage().Portals,ColonizeManage().instancetoprotal)
    istruelgyc(pid, tagid)
def getypjc(groupid):
    '''根据副本组id获取状态信息 1力量、2敏捷 、3智力、4精神、5耐力、6所有'''
    instanceinfo= ColonizeManage().getInstanceInfoByid(groupid)
    val={}
    for k in instanceinfo['property'].keys():
        val[k]={}
        if instanceinfo['property'][k][0]:#如果状态开启
            val[k]['status']=1 #激活
            val[k]['remainTime']=outtime(instanceinfo['property'][k][1])
        else:
            val[k]['status']=0 #没激活
            val[k]['remainTime']=0
    return val

def changeimg(tagid,groupid,itemid,pid):
    '''状态还有30分钟的时候
    @param tagid: int 角色动态id
    '''
    instanceinfo= ColonizeManage().getInstanceInfoByid(groupid)
    info=instanceinfo['property'][itemid]
    info[3]=True #表示小于30分钟
    icon_app.add(pid, 3) #发送流光溢彩殖民管理图标
    reactor.callLater(configure.instanceStatusPrompt,startclose,groupid,itemid,pid,tagid)#半小时之后设置状态关闭
    
def startclose(groupid,itemid,pid,tagid):
    '''状态消失'''
    instanceinfo= ColonizeManage().getInstanceInfoByid(groupid)
    info=instanceinfo['property'][itemid]
    info[0]=False
    info[3]=False
    istruelgyc(pid,tagid)

def istruelgyc(pid,tagid):
    '''根据角色id,判断是否推送流光溢彩
    @param pid: int 角色动态id
    return 0:表示殖民管理没有流光溢彩 1表示有流光溢彩
    '''
    data=dbInstanceColonize.getAllinstanceListBypid(pid)
    flg=False
    for item in data:
        groupid=item['instanceid']
        instanceinfo= ColonizeManage().getInstanceInfoByid(groupid)
        for k in instanceinfo['property'].keys():
            if instanceinfo['property'][k][0]:#如果状态开启
                if instanceinfo['property'][k][3]:#如果剩余时间小于半小时
                    flg=True
    if flg:
        icon_app.add(pid, 3)
    else:
        icon_app.add(pid, 2)
    
def outtime(down):
    '''根据到期时间,返回剩余秒数'''
    import datetime,time
    nowtime=datetime.datetime.fromtimestamp(time.time()) #系统当前时间
    down+=datetime.timedelta(seconds=configure.instanceStatus)
    s2=(down-nowtime).seconds
    return s2

def iscoloBypid(pid):
    '''该角色是否有殖民地'''
    flg=ColonizeManage().ishavestrengthen(pid)
    return flg
    
