#coding:utf8
'''
Created on 2011-8-27
@author: SIOP_09
'''
from app.scense.utils.dbopera import dbInstance_d
from app.scense.core.Item import Item
from app.scense.core.character.Monster import Monster
from app.scense.core.language.Language import Lg

def getInstance_dByid(instanceid):
    '''根据副本id获取组队副本需要的信息
    @param id: int 副本id
    '''
    result=dbInstance_d.getInstance_dByid(instanceid)
    ditems=[] #存储掉落物品实例
    ms=[] #存储怪物实例
    if result:
        dropitems=result.get('dropitem',None)
        if dropitems:
            for itemid in dropitems:
                ditems.append(Item(itemid))
        monsters=result.get('moster',None)
        if monsters:
            for mosterid in monsters:
                ms.append( Monster(templateId=mosterid))
        result['dropitem']=ditems
        result['moster']=ms
        data={"result":True,"message":Lg().g(166),"data":result}
        return data
    return None

def getMonsterItemByid(instanceid):
    '''根据副本id获取组队副本需要的信息
    @param id: int 副本id
    '''
    result=dbInstance_d.getInstance_dByid(instanceid)
    ditems=[] #存储掉落物品实例
    ms=[] #存储怪物实例
    if result:
        dropitems=result.get('dropitem',None)
        if dropitems:
            for itemid in dropitems:
                itm=Item(itemid)
                val=[]
                val.append(itm.baseInfo.getBaseQuality()) #物品品质
                val.append(itm.baseInfo.getName()) #物品名称
                del itm
                ditems.append(val)
        monsters=result.get('moster',None)
        if monsters:
            for mosterid in monsters:
                ms.append( Monster(templateId=mosterid))
        result['dropitem']=ditems
        result['moster']=ms
        data={"result":True,"message":Lg().g(166),"data":result}
        return data
    return None
    