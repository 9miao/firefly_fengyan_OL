#coding:utf8
'''
Created on 2012-2-15
@author: jt
'''
from app.scense.utils.dbopera import dbInstanceColonize
from app.scense.utils.dbopera import dbDefeatedFailLog
from app.scense.core.instance.InstanceGroupManage import InstanceGroupManage
from app.scense.utils.dbopera import dbDefenceBonus
from app.scense.utils.dbopera import dbPublicscene

from app.scense.core.PlayersManager import PlayersManager
from twisted.python import log
from app.scense.core.instance.ColonizeManage import ColonizeManage
from app.scense.netInterface import pushObjectNetInterface

from app.scense.applyInterface import icon_app, InstanceColonizeGuerdon, instance_app
from app.scense.core.language.Language import Lg


def getBonusInfo(did):
    '''根据保卫奖励表主键id获取奖励信息'''
    data=dbDefenceBonus.getByid(did)
    if not data:
        return 0
    else:
        return data['reward']


def ObtainReward(pid,did):
    '''领取单个保卫奖励
    @param pid: int 角色id
    @param did: int 保卫奖励表主键id
    '''
    msg=u""
    flg=True
    player=PlayersManager().getPlayerByID(pid)#获得角色id
    info=dbDefenceBonus.getByid(did) #根据奖励主键id获得奖励信息
    if not info:
        pushObjectNetInterface.pushOtherMessage(905, Lg().g(61), [player.getDynamicId()])
        return False,Lg().g(61)
    reward=info['reward']
    player.finance.updatePrestige(player.finance.getPrestige()+reward)
    if not dbDefenceBonus.delByid(info['id']) : 
        msg+=Lg().g(62)
        flg=False

#    item=Item(itemTemplateId=20030061)
#    item.pack.setStack(info['reward']) #物品的数量
#    rs1=player.pack._package.canPutItem(item,info['reward']) #判断背包中是否可以放入这些数量的物品
#    if rs1: #如果可以放进去
#        player.pack.putNewItemsInPackage(20030061,info['reward'])
#        del item
#        if not dbDefenceBonus.delByid(info['id']) : 
#            msg+=Lg().g(62)
#            flg=False
#    else: #如果一个奖励所获得物品不能放入背包
#        del item
#        pushObjectNetInterface.pushOtherMessage(905, Lg().g(16), [player.getDynamicId()])
#        return False,Lg().g(16)
    return flg,msg

def ObtainAllReward(pid):
    '''获取所有保卫奖励(技能石奖励)'''
    msg=u"保卫奖励领取成功"
    flg=True
    Lists= dbDefenceBonus.getInfoByPid(pid) #获取该角色所有应得的奖励列表
    player=PlayersManager().getPlayerByID(pid) #获取该角色的内存中的实例
    if Lists and  len(Lists)>0:
        for info in Lists:
            reward=info['reward']
            player.finance.updatePrestige(player.finance.getPrestige()+reward)
            
            if not dbDefenceBonus.delByid(info['id']) : 
                msg+=Lg().g(62)
                flg=False
                return False,Lg().g(16)
#            item=Item(itemTemplateId=20030061)
#            item.pack.setStack(info['reward']) #物品的数量
#            rs1=player.pack._package.canPutItem(item,info['reward']) #判断背包中是否可以放入这些数量的物品
#            if rs1: #如果可以放进去
#                player.pack.putNewItemInPackage(item)
#                del item
#                if not dbDefenceBonus.delByid(info['id']) : 
#                    msg+=Lg().g(62)
#                    flg=False
#            else: #如果一个奖励所获得物品不能放入背包
#                del item
#                pushObjectNetInterface.pushOtherMessage(905, Lg().g(16), [player.getDynamicId()])
#                return False,Lg().g(16)
    return flg,msg
    

def getInvadeList(pid,page,counts):
    '''获取入侵列表
    @param pid: int 角色id
    @param page: int 当前页数
    @param counts: int 每页多少条信息
    '''
    invadeList=[]
    if page<1:
        page=1
    deflist,zong=dbDefeatedFailLog.getlogBydesc(pid, page, counts)#挑战列表
    if deflist:
        for item in deflist:
            if len(item['sb'])<=8:
                continue
            flg=True #True 表示保卫成功
            if item['cgid']>0:
                flg=False #False 表示保卫失败
            item['sb']= eval("{%s}"%item['sb'])
            item['battleResult']=flg
            invadeList.append(item)
    return invadeList,zong

def getRewardList(pid,page,counts):
    '''根据角色id获取保卫奖励列表'''
    '''获取入侵列表
    @param pid: int 角色id
    @param page: int 当前页数
    @param counts: int 每页多少条信息
    '''
    RewarList=[]
    rList,zong=dbDefenceBonus.getRewardList(pid, page, counts) #返回奖励列表、总页数
    if rList:
        for item in rList:
            flg=False #False 表示没有到达最大值
            if item['ismax']==1:
                flg=True
            val={'r_id':item['id'],'r_type':item['type'],'t_name':item['name'],'t_e1':item['clearancecount'],'t_e2':item['price'],'t_e3':item['reward'],'t_e4':flg}
            RewarList.append(val)
    return RewarList,zong

def isReward(pid,dynamicId):
    '''判断该角色是否有殖民奖励'''
    data=dbDefenceBonus.getCountBypid(pid)
    if data:#如果有奖励
        icon_app.add(pid, 1)
    else:
        icon_app.clear(pid, 1)
def iscolonManage(pid,dynamicId):
    data=InstanceColonizeGuerdon.iscoloBypid(pid)#角色是否有殖民地
    if data:#如果有殖民地
        icon_app.add(pid, 2)
    else:
        icon_app.clear(pid, 2)


def updatets():
    '''更新副本、城镇殖民奖励'''
    dbDefenceBonus.delAll()#删除殖民奖励列表所有数据
    
    dbDefeatedFailLog.copyto() #将数据复制到tb_defeated_fail_log1
    dbDefeatedFailLog.delAll() #删除入侵失败表所有数据
    
    updateBonus() #更新殖民副本奖励
#    dbInstanceColonize.copyto() #将数据复制到另一张表tb_instance_colonize1
#    dbInstanceColonize.setClearancecount(0) #设置保卫表所有数据的通关次数为0并设置所有记录成功占领者为 无
    
    updatecity() #更新城市奖励
#    ColonizeManage().setAllCount0() #内存中设置所有通关次数为0
    
    plist=dbDefenceBonus.getAllPid()#获取所有奖励角色id
    if plist and len(plist):
        for item in plist:
            icon_app.add(item,1)#推送殖民奖励
#    zlist=dbInstanceColonize.getAllUserid()#获取全部有殖民地的角色id
#    if zlist and len(zlist)>0:
#        for item in zlist:
#            iscolonManage(item[0],1)#刷新殖民管理图标
    
def updateColonize(instanceid,instancename,pid,cid,pname):
    '''更改副本保卫者
    @param instanceid: int 副本组id
    @param pid: int 挑战者id
    @param cid: int 领主id
    '''
    
    player=PlayersManager().getPlayerByID(pid) #获得挑战者角色
    gid=0
    gname=Lg().g(143)
    if not player:
        log.err(Lg().g(106))
    if player.guild.getID()>0:
        gid=player.guild.getID()
        gname=player.guild.getGuildName()
    ColonizeManage().updateInstancePid(instanceid, pid, player.baseInfo.getName(), gid, gname, instancename) #内存中更改信息 

def getInatanceColonizeInfo(instanceid,pid):
    '''获取殖民信息表主键id，通过副本组id和角色id'''
    data=dbInstanceColonize.getInfo(instanceid, pid)
    if data:
        if data['id']:
            return data['id']
        else:
            log.err(u"defencelog_app->def getInatanceColonizeInfo(instanceid=%s,pid=%s):,没有获取到数值"%(instanceid,pid)) 
    else:
        log.err(u"defencelog_app->def getInatanceColonizeInfo(instanceid=%s,pid=%s):,没有获取到数值"%(instanceid,pid))  
    return None

def updateBonus():
    '''更新殖民副本奖励'''
    for info in  ColonizeManage().getI().values():#info 殖民信息
        if info['pid']>0:
            count=0 #入侵次数
            reward=0#副本组中规定的这个副本单次通关奖励数量
            info['wm']=0
            instanceid=InstanceGroupManage().getInstanceidByGroupid(info['id'])#副本id
            instanceinfo=instance_app.allInfo.get(instanceid,0)
            dl=instanceinfo['downlevle']
            rewardAll=dl*20 #获得的威望值
            ismax=0 #0没有达到最高值  1达到最高值
            if rewardAll>0: #如果奖励的技能石>0 则添加奖励
                dbDefenceBonus.addLog(info['name'], 0, reward, count, 0, info['pid'],ismax,rewardAll,info['id'])
def updatecity():
    '''更新殖民城镇奖励'''
    citylist=dbPublicscene.Allinfo#获取所有城镇的信息
    for info in ColonizeManage().getC().values():#cityinfo #城市殖民信息
        if info['pid']>0:
            dl=citylist.get(info['cityid'],0)
            cityname=dl['name']
            reward=dl['levelRequired']*20
            dbDefenceBonus.addCityLog(cityname, 1,reward ,info['cityid'],1 )
                
def addDefeated_fail_log(groupid,sbid,sbname,pid,pname,name):
    '''根据保卫表主键id和挑战失败者角色id，查看失败列表是否有此记录
    @param groupid: int 殖民副本组id
    @param sbid: int 挑战失败者角色id
    @param pid: int 领主id
    '''
    result=dbDefeatedFailLog.ishave(groupid, pid) #是否存已经有此记录
    if not result:
        dbDefeatedFailLog.addLog(groupid, name, pid, pname,sbid,sbname)
    else:
        dbDefeatedFailLog.addSbLog(groupid, pid, sbid, sbname)
    
def addDefeated_fail_logTrue(groupid,cgid,cgname,pid,pname,name):
    '''添加挑战成功记录
    @param groupid: int 殖民副本组id
    @param sbid: int 挑战失败者角色id
    @param pid: int 领主id
    '''
    result=dbDefeatedFailLog.ishave(groupid, pid) #是否存已经有此记录
    if not result:
        dbDefeatedFailLog.addLogTrue(groupid, name, pid, pname, cgid, cgname)
    else:
        dbDefeatedFailLog.updateLogTrue(groupid, pid, cgid, cgname)
        
def ClearanceOperate(did,pid,flg):
    '''给殖民地领主添加其副本的通关次数
    @param did: int  副本id
    @param pid: int 当前角色id
    @param flg: bool 副本是否胜利(通关)
    '''
    if not flg:
        return
    instanceid=InstanceGroupManage().getFristInstanceBy(did) #副本组id
    if dbInstanceColonize.updateClearanceCount(instanceid): #在保卫表中增加通关次数
        ColonizeManage().defupdateInstanceClearancecount(instanceid)
    
