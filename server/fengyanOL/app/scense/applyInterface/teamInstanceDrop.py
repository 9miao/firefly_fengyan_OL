#coding:utf8
'''
Created on 2012-8-9
多人副本掉落
@author: jt
'''
from app.scense.utils.dbopera import dbTeamInstanceDrop, dbTeamInstance
import random
from twisted.python import log
from app.scense.core.Item import Item

def getTeamDropItem(dropid):
    '''获取多人副本掉落出的物品
    @param dropid: int 多人副本掉落id
    '''
    all=dbTeamInstanceDrop.teamInstanceDropAll#所有掉落信息
    # ditem [[物品id,物品数量,1,2],[物品id,物品数量,3,10]] 上限是100
    if not all.has_key(dropid):
        log.err(u"getTeamDropItem(%s) all=%s"%(dropid,all))
    ilist=all.get(dropid)['ditem']
    sj=random.randint(1,100)
    wpobj=None#物品实例
    for item in ilist:
        st=item[2]#较小的内定随机数
        en=item[3]#较大的内定随机数
        if st<=sj and en>=sj:
            wpobj=Item(item[0])
            wpobj.pack.setStack(item[1])
            return wpobj
    log.err(u"getTeamDropItem(%s) ilist=%s"%(dropid,ilist))
    return None

def getTeamDropItemidAndCounts(dropid):
    '''获取多人副本掉落出的物品id和数量
    @param dropid: int 多人副本掉落id
    '''
    all=dbTeamInstanceDrop.teamInstanceDropAll#所有掉落信息
    # ditem [[物品id,物品数量,1,2],[物品id,物品数量,3,10]] 上限是100
    if not all.has_key(dropid):
        log.err(u"getTeamDropItem(%s) all=%s"%(dropid,all))
    ilist=all.get(dropid)['ditem']
    sj=random.randint(1,100)
    wpobj={}#掉落物品物品id和数量
    for item in ilist:
        st=item[2]#较小的内定随机数
        en=item[3]#较大的内定随机数
        if st<=sj and en>=sj:
            wpobj['id']=item[0]
            wpobj['count']=item[1]
            return wpobj
    log.err(u"getTeamDropItem(%s) ilist=%s"%(dropid,ilist))
    return None

def getTeamDropListItem(dropidList):
    '''获取多人副本掉落出的物品
    @param dropid: [] [多人副本掉落id,多人副本掉落id]
    '''
    itemList=[]#物品列表
    for dropid in dropidList:
        itemList.append(getTeamDropItem(dropid))
    return itemList

def getTeamDropListItemidAndCounts(dropidList):
    '''获取多人副本掉落出的物品id和数量
    @param dropid: [] [多人副本掉落id,多人副本掉落id]
    '''
    itemList=[]#物品列表
    for dropid in dropidList:
        itemList.append(getTeamDropItemidAndCounts(dropid))
    return itemList


def getTeamDropListItemByTypeid(typeid):
    '''根据副本类型获取掉落物品'''
    from applyInterface import teamInstanceDrop
    all=dbTeamInstance.teamInstanceAll #所有多人副本信息
    info=all.get(typeid)
    dropidList=info.get('dropid') #[dropid,dripid]
    ItemList=teamInstanceDrop.getTeamDropListItem(dropidList)#掉落物品[物品实例,物品实例]
    return ItemList

def getTeamDropListItemidCountByTypeid(typeid):
    '''根据副本类型获取掉落物品id和数量'''
    from applyInterface import teamInstanceDrop
    all=dbTeamInstance.teamInstanceAll #所有多人副本信息
    info=all.get(typeid)
    dropidList=info.get('dropid') #[dropid,dripid]
    ItemList=teamInstanceDrop.getTeamDropListItemidAndCounts(dropidList)#掉落物品[物品实例,物品实例]
    return ItemList #[{'id':5201,'count':2}]