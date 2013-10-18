#coding:utf8
'''
Created on 2012-8-9
多人副本操作
@author: jt
'''
from app.scense.utils.dbopera import dbTeamInstance
from twisted.python import log
from app.scense.core.character.Monster import Monster
from app.scense.core.fight import fight_new
from app.scense.utils import dbaccess
from app.scense.netInterface import pushObjectNetInterface
#from serverconfig.publicnode import publicnoderemote
from app.scense.applyInterface import configure
from app.scense.core.language.Language import Lg

 
def getInfo(typeid):
    '''根据多人副本类型id获取多人副本信息'''
    all=dbTeamInstance.teamInstanceAll #所有多人副本信息
    info=all.get(typeid)
    zy=info.get('resourceid')#资源id
    width=info.get('width')#场景宽度
    height=info.get('height')#场景高度
    mostersList=info.get('mosters')#[[怪物id,阵法位置(1-9)],[怪物id,阵法位置(1-9)]]
    MosterList=[]#怪物实例列表
    mosterwz={}#key:怪物动态di，value:怪物位置
    sa=0
    for mid in mostersList:
        sa+=1
        MosterList.append(Monster(id=sa,templateId=mid[0]))
        mosterwz[sa]=mid[1]
    rs={}
    rs['zy']=zy
    rs['width']=width
    rs['height']=height
    rs['MosterList']=MosterList
    rs['mosterwz']=mosterwz
    return rs
    
def TeamFighting(pid):
    '''开始多人副本战斗'''
    from app.scense.core.teamfight.TeamFight import TeamFight
    from app.scense.applyInterface import teamInstanceDrop
    
    if not configure.isteamInstanceTime(17):
        return
    teamid=TeamFight().getTeamidByPid(pid)
    if teamid==0:
        return{'result':False,'message':Lg().g(260)}
    teaminfo=TeamFight().getteaminfoByteamid(teamid)
    
    if not teaminfo.pid==pid:
        return{'result':False,'message':Lg().g(261)}
    if teaminfo.count<2:
        pushObjectNetInterface.pushOtherMessageByCharacterId(Lg().g(646), [pid])
        return{'result':False,'message':Lg().g(262)}
    PlayerList=teaminfo.players.values()#角色实例列表
    typeid=teaminfo.type
    msgs={}#记录角色获得物品
    playeritem={}#记录角色获得物品信息 key:角色id,value:[{'id':5201,'count':2}]物品列表[物品id和物品数量]
    
        
    playerzf=teaminfo.getZfInfo()#角色阵法位置
    rs=getInfo(typeid)
    MosterList=rs.get('MosterList')#怪物实例列表
    mosterwz=rs.get('mosterwz')#怪物阵法位置
    ItemList=rs.get('ItemList')#物品实例列表
    zy=rs.get('zy')#资源id
    fightinfo=fight_new.DoGroupFight(PlayerList, playerzf, MosterList, mosterwz)
    
    if fightinfo.battleResult==1:
        pklist=teaminfo.players.keys()
        for pk in pklist:
            msgs[pk]=u''
            ItemList=teamInstanceDrop.getTeamDropListItemidCountByTypeid(typeid) #[{'id':5201,'count':2}]
            playeritem[pk]=ItemList
            for item in ItemList:
                itemTemplateId=item.get('id')
                iname=dbaccess.all_ItemTemplate[itemTemplateId]['name']#物品名称
                msgs[pk]=msgs[pk]+u'%s * %s\n'%(iname,item.get('count'))
                gm="player.pack.putNewItemsInPackage(%s,%s)"%(itemTemplateId,item.get('count'))
#                publicnoderemote.callRemote("updateplayerInfo",pk,gm)
    else:#战斗失败
        for pk in teaminfo.players.keys():
            msgs[pk]=Lg().g(143)
    
    for pk in teaminfo.players.keys():
        msg=msgs.get(pk)
        TeamFight().addfightcount(pk, typeid)
        
        pushObjectNetInterface.getzudui_4308(fightinfo, [pk], msg,zy)
    TeamFight().dismissTeam(teamid)
