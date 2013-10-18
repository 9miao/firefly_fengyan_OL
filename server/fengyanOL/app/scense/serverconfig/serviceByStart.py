#coding:utf8
'''
Created on 2011-3-17

@author: sean_lan

服务启动时需要启动的服务
'''
from twisted.internet import reactor
from twisted.python import log
from app.scense.utils import dbaccess
from app.scense.core.instance.InstanceManager import InstanceManager
from app.scense.core.battlefieldarea.battleAreaManager import BattleAreaManager
from app.scense.core.campaign.FortressManager import FortressManager
from app.scense.core.zhanyi.zymanage import ZYManage
import datetime
from app.scense.utils.dbopera import dbDropOut,dbInstanceInfo, dbGuild, dbNobility,\
    dbPublicscene, dbTeamInstance, dbTeamInstanceDrop
from app.scense.utils.dbopera import dbInstance_d
from app.scense.utils.dbopera import dbSkill
from app.scense.utils.dbopera import dbBuff
from app.scense.utils.dbopera import dbDrinkery
from app.scense.utils.dbopera import dbChat
from app.scense.utils.dbopera import dbEffect
from app.scense.utils.dbopera import dbtask,dbMail
from app.scense.utils.dbopera import dbCharacterPet,dbMonster
from app.scense.utils.dbopera import dbInstanceColonizeChallenge
from app.scense.utils.dbopera import dbVIP,dbPetShopConfigure
from app.scense.utils.dbopera import dbfightfail,dbCharacterFate,dbtower,dbfigure
from app.scense.utils.dbopera import db_zhanyi
from app.scense.core.instance.InstanceGroupManage import InstanceGroupManage
from app.scense.applyInterface import dropout, guild, instance_app,instanceColonizeChallenge,\
    configure
from app.scense.serverconfig.node import noderemote
from app.scense.core.instance.ColonizeManage import ColonizeManage
from app.scense.core.teamfight.TeamFight import TeamFight
from app.scense.core.ConsMonitor import ConsMonitor



reactor = reactor

def initAlldata():
    '''初始化常用数据，从数据库读入到内存中
    '''
    dbaccess.All_ShieldWord = dbaccess.getAll_ShieldWord()
    dbaccess.tb_mallitem_Column_name=dbaccess.getTablecolumnName('tb_item_template')+['item_templateid','tag','promotion','gold','coupon','restrict','cheapstart','cheapend','discount','up','down','onoff']
    dbaccess.tb_mallitem_Column_name1=dbaccess.getTablecolumnName('tb_mall_item')
    dbaccess.tb_mall_restrict_Column_name=dbaccess.getTablecolumnName('tb_mall_restrict')
    dbaccess.tb_mall_log_Column_name=dbaccess.getTablecolumnName('tb_mall_log')
    dbaccess.tb_instanceinfo_Columen_name=dbaccess.getTablecolumnName('tb_instanceinfo')
    dbaccess.tb_instance_activation_Columen_name=dbaccess.getTablecolumnName('tb_instance_activation')
    dbaccess.tb_instance_close_Columen_name=dbaccess.getTablecolumnName('tb_instance_close')
    dbaccess.tb_instance_record_Columen_name=dbaccess.getTablecolumnName('tb_instance_record')
    dbaccess.tb_profession_Columen_name = dbaccess.getTablecolumnName("tb_profession")
    dbDropOut.tb_dropout_Column_name=dbaccess.getTablecolumnName('tb_dropout')
    dbaccess.tb_marix_Columen_name = dbaccess.getTablecolumnName("tb_matrix")#获取阵法表中所有的阵法数据
    dbDrinkery.tb_drinkery_Column_name=dbaccess.getTablecolumnName('tb_drinkery') #存储数据库中酒店表中的所有字段
    dbChat.tb_chat_astrict_name=dbaccess.getTablecolumnName('tb_chat_astrict')
    
    dbaccess.tb_Profession_Config = dbaccess.getProfession_Config()         #初始化职业成长配置表
    dbaccess.tb_Experience_config = dbaccess.getExperience_Config()        #初始化经验成长配置表
    dbaccess.all_ItemTemplate = dbaccess.getAll_ItemTemplate()              #获取所有的物品模板信息
    dbaccess.all_marix_info = dbaccess.getAllMarix_Info()                   #获取所有的阵法信息
    
    dbEffect.ALL_EFFECT_INFO = dbEffect.getAllEffectInfo()#获取所有的效果信息
    dbBuff.ALL_BUFF_INFO = dbBuff.getAllBuffInfo()#获取所有的buff信息
    instance_app.allInfo=dbInstanceInfo.getAllInfo() #获取所有副本信息
    guild.AllCharacterGuildInfo=dbGuild.getAllCharacterGuildInfo() #获取所有角色与行会对应关系
    dropout.alldrop=dbDropOut.getAll() #获取所有掉落信息
    instanceColonizeChallenge.allColonizeChallenge=dbInstanceColonizeChallenge.getAllColonizeChallenge()
    instanceColonizeChallenge.allMosterNameByinstance=dbInstanceColonizeChallenge.getAllMosterName()
    
    dbtask.ALL_MAIN_TASK = dbtask.getAllMainTask()
    dbtask.ALL_EXTEN_TASK = dbtask.getAllExtedTask()
    dbInstance_d.instance_dAll= dbInstance_d.getInstance_dAll()#副本掉落tip
    dbTeamInstance.getAll() #设置所有多人副本数据
    dbTeamInstanceDrop.getAll() #设置所有多人副本掉落数据
    dbNobility.getAll()#获取所有爵位信息
    dbPetShopConfigure.getAll()#获取所有宠物商店推荐宠物组合信息
    dbPublicscene.getAllInfo()
    dbSkill.getAllSkill()
    dbSkill.getBuffAddition()
    dbSkill.getBuffOffsetInfo()
    dbMonster.getAllMonsterInfo()
    dbCharacterPet.getPetTrainConfig()
    dbCharacterPet.getAllPetTemplate()
    dbCharacterPet.getPetExp()
    dbCharacterPet.getAllPetGrowthConfig()
    dbMail.getAllLevelMail()
    dbGuild.getAllTechnology()
    dbGuild.getTechnologyLimit()
    dbVIP.getAllVIPPer()
    dbVIP.getVIPExp()
    dbVIP.getAllLibao()
    dbfightfail.getAllFightFail()
    dbCharacterFate.getAllFateTemplate()
    dbtower.initAllTowerInfo()
    dbfigure.getAllFigureInfo()
    db_zhanyi.getAllZhanYiInfo()#获取所有的战役信息
    db_zhanyi.getAllZhangJieInfo()#获取所有的战役信息
    InstanceGroupManage()
#    ColonizeManage()
    FortressManager()
    ZYManage()
    configure.shuxingbianliang()

def addEnergyPerDay():
    '''每天8点加点90活力'''
    energy = 90
    try:
        dbaccess.updateAllPlayersEnergy(energy)
    except Exception:
        pass
    reactor.callLater(3600*24,addEnergyPerDay)
    
def pingMysql():
    ''''''
    dbaccess.pingMysql()
    reactor.callLater(3600*3,pingMysql)
    
def pushAllSceneInfo(delta):
    '''推送所有场景中的玩家位置'''
    try:
        InstanceManager().pushAllInstanceInfo(delta)
    except Exception,e:
        log.err(e)
    reactor.callLater(delta,pushAllSceneInfo,delta)
    
def prepareGuildBattle():
    '''每天晚上7点30安排行会战'''
    BattleAreaManager().prepareGuildBattle()
    #print u"行会战开始了"
    reactor.callLater(3600*24,pushAllSceneInfo)

#def delFriendRecord():
#    '''每天晚上24点将所有角色的祝福次数设置为0'''
#    dbFriendRecord.delRecordAll()
#    print u'所有角色祝福次数已经重置为0'
#    winning_app.set0()#清空副本输入信息
#    dbNobilityAstrict.clear()#每天晚上24点清除官爵领取兑换限制
#    TopList().updateAll()#每天24点更新排行榜
#    reactor.callLater(3600*24,delFriendRecord)
    
    
def updateDefence():
    '''每天早上6点更新防御奖励'''
    from app.scense.applyInterface import defencelog_app
    defencelog_app.updatets()
    log.msg(u"更新殖民奖励")
    reactor.callLater(3600*24,updateDefence)
    
def cleanTeamfight():
    '''每天晚上24点将所有角色的祝福次数设置为0'''
    TeamFight().ct={}#每天清0多人副本战斗次数限制
    reactor.callLater(3600*24,cleanTeamfight)
    
def GuildFightHandle(ldID):
    '''国战斗处理
    @param ldID:int 城镇要塞的ID
    '''
    fortress = FortressManager().getFortressById(ldID)
    fortress.doFight()
    reactor.callLater(3600*24,GuildFightHandle,ldID)
    
def ConsRecordWriter():
    '''消费记录定时写入
    '''
    ConsMonitor().insertConsRecord()
    reactor.callLater(600,ConsRecordWriter)
    
    
def doGuildFight():
    '''执行国战斗
    '''
    n="scense_1000"
    t=n.split('_')
    if t[0]=="scense_" and int(t[1])%100==0:
        sceneId = int(t[1])/100*100
        ldID =0
        for fortress in FortressManager().fortresss.values():
            if fortress.get('sceneId')==sceneId:
                ldID = fortress.id
                break
        #上半场
        reactor.callLater(differTime(19,10,0), GuildFightHandle,ldID)
        #下半场
        reactor.callLater(differTime(19,40,0), GuildFightHandle,ldID)
    

    
def doService():
    '''启动服务器时需要启动的服务：
    1.初始化常用数据
    2.每天8点加点90活力
    3.启动场景信息更新
    '''
    initAlldata()
    doGuildFight()#开启国战定时启动
    ConsRecordWriter()#消费记录的定时写入

#    n=noderemote.getName()
#    t=n.split('_')
#    if t[0]=="teamserver":
#        #(晚上12点不能写成00:00:00)
#        reactor.callLater(differTime(12,29,0), cleanTeamfight)
#        reactor.callLater(differTime(17,29,0), cleanTeamfight)


def differTime(h,m,s):
    '''到达预设时间执行函数  return与当前时间相差的秒数
    @param h,m,s: int 预设 时,分,秒 
    return int 秒数
    '''
    hour = datetime.datetime.now().hour
    minute = datetime.datetime.now().minute
    second = datetime.datetime.now().second
    old=h*3600+m*60+s #预设时间 据0点得秒数
    young=hour*3600+minute*60+second #当前时间据0点得秒数
    
    if old>=young:
        return old-young
    else:
        return 24*3600-(young-old)
    
    
