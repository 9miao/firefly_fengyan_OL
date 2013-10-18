#coding:utf8
'''
Created on 2012-2-17

@author: lan
'''
from app.scense.core.PlayersManager import PlayersManager
from app.scense.core.guild.GuildManager import GuildManager
from app.scense.core.instance.ColonizeManage import ColonizeManage
from app.scense.core.campaign.FortressManager import FortressManager
import random
from app.scense.core.language.Language import Lg

DEFAULTCOLOR = "0xCCCC99"

def randomcorlor():
    return random.randint(0,int('0xFFFFFF',16))

SceneMaptestdata = [
            {'id':1000,'color':randomcorlor(),'tax':10,'income':100,'scene_name':u'克洛村','union_name':'CCC'},
            {'id':1100,'color':randomcorlor(),'tax':10,'income':100,'scene_name':u'雷格镇','union_name':'smsmsmsmsm'},
            {'id':1200,'color':randomcorlor(),'tax':10,'income':100,'scene_name':u'王城塞拉恩特','union_name':'CCTV'},
            {'id':1300,'color':randomcorlor(),'tax':10,'income':100,'scene_name':u'皇宫','union_name':'asdf'},
            {'id':1400,'color':randomcorlor(),'tax':10,'income':100,'scene_name':u'精灵之城','union_name':'ddd'},
            {'id':1500,'color':randomcorlor(),'tax':10,'income':100,'scene_name':u'雪风部落','union_name':'3sdfe'}
            ]

InstanceInfostestdata = [
            {'id':5001,'color':randomcorlor(),'once':100,'income':1000,'instance_name':u'平原入口','union_name':'CCTV'},
            {'id':5002,'color':randomcorlor(),'once':100,'income':1000,'instance_name':u'平原小径','union_name':'CCTV'},
            {'id':5003,'color':randomcorlor(),'once':100,'income':1000,'instance_name':u'落叶平原','union_name':'CCTV'},
            {'id':5004,'color':randomcorlor(),'once':100,'income':1000,'instance_name':u'平原深处','union_name':'CCTV'},
            {'id':5005,'color':randomcorlor(),'once':100,'income':1000,'instance_name':u'森林入口','union_name':'CCTV'},
            {'id':5006,'color':randomcorlor(),'once':100,'income':1000,'instance_name':u'森林小径','union_name':'CCTV'},
                         ]

def SceneMapInfos(dynamicId,characterId):
    '''获取大地图信息
    @param dynamicId: int 客户端的id
    @param characterId: int 角色的id
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    guildId = player.guild.getID()
    if not guildId:
        self_color = int(DEFAULTCOLOR,16)
    else:
        guild = GuildManager().getGuildById(guildId)
        self_color = guild.guildinfo.get('color',int(DEFAULTCOLOR,16))
    infos = FortressManager().getBigMapInfo()#ColonizeManage().getCityList()
    return {'result':True,'self_color':self_color,'infos':infos}

def InstanceMapInfos(dynamicId,characterId):
    '''获取副本组信息
    @param dynamicId: int 客户端的id
    @param characterId: int 角色的id
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    guildId = player.guild.getID()
    if not guildId:
        self_color = int(DEFAULTCOLOR,16)
    else:
        guild = GuildManager().getGuildById(guildId)
        self_color = guild.guildinfo.get('color',int(DEFAULTCOLOR,16))
    cityid = player.baseInfo.getTown()
    infos = ColonizeManage().getInstanceListByCityid(cityid)
    return {'result':True,'self_color':self_color,'infos':infos}
    


