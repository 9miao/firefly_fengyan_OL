#coding:utf8
'''
Created on 2011-9-9
ApplyInterface 酒店
@author: SIOP_09
'''
from app.scense.utils.dbopera import dbDrinkery
from app.scense.core.PlayersManager import PlayersManager
from app.scense.netInterface import pushObjectNetInterface
from app.scense.core.language.Language import Lg

def add(characterid,typeid,count):
    '''添加酒店记录
    @param characterid: 角色id
    @param typeid: int 酒店物品类型
    @param count: int 使用数量
    '''
    result=dbDrinkery.add(characterid, typeid, count)
    if not result:
        return{'result':False,'message':u'添加酒店记录出错啦!'}
    return{'result':True,'message':u'添加酒店记录成功!'}
    
     

def getHotelinfo(characterid):
    '''根据角色id获取酒店商品使用信息
    @param characterid: int 角色id
    '''
    result=dbDrinkery.getHotelinfo(characterid)
    if not result:
        return{'result':False,'message':u'获取酒店信息出错啦!'}
    return {'result':True,'message':u'添加酒店记录出错啦!','data':result}

def HotelUseItem(characterid,typeid):
    '''使用酒店物品
    @param characterid: int 角色id
    @param typeid: int #0魔法泡沫酒 1普通果汁酒 2神奇果汁酒
    '''
    import math
    player=PlayersManager().getPlayerByID(characterid) #角色
    if typeid==0:
        Hp=player.attribute.getMaxHp()-player.attribute._hp #最大血量-当前血量
        Mp=player.attribute.getMaxMp()-player.attribute._mp #最大魔法-当前魔法
        coin=int(math.ceil((Hp+Mp)/5.0))
        if coin>player.finance.getCoin():
            return{'result':False,'message':u'金币不足,无法恢复'}
        if player.attribute.getMaxHp()==player.attribute._hp and player.attribute.getMaxMp()==player.attribute._mp:
            return {'result':False,'message':u'您很健康，不要来捣乱'}
        player.attribute.updateHp(player.attribute.getMaxHp()) #最大血量
        player.attribute.updateMp(player.attribute.getMaxMp()) #最大魔法
        if player.level.getLevel()>=15: #15级之前免费
            player.finance.updateCoin(player.finance.getCoin()-coin) #修改金币
    elif typeid==1:#1普通果汁酒
        if player.attribute.getEnergy()>=200:
            return {'result':False,'message':u'您的活力充足，不需要补充，我很忙的，不要来捣乱!'}
        if 10>player.finance.getGold():
            return{'result':False,'message':u'钻不足,无法恢复'}
        if player.attribute.getEnergy()<=200-8:
            player.attribute.updateEnergy(player.attribute.getEnergy()+8)
        else:
            player.attribute.updateEnergy(200)
        count=dbDrinkery.getByTypeAndCharacterid(characterid, typeid+1)
        if count>=3:
            return{'result':False,'message':u'普通果汁酒今天已经使用了 3次'}
        if count==0:
            add(characterid,2,1)
        elif count<3:
            dbDrinkery.updateByCharacteridAndtype(characterid, typeid+1, 1)        
        
        player.finance.updateGold(player.finance.getGold()-10)
    elif typeid==2:
        if player.attribute.getEnergy()>=200:
            return {'result':False,'message':u'您您的活力充足，不需要补充，我很忙的，不要来捣乱'}
        if 35>player.finance.getGold():
            return{'result':False,'message':u'钻不足,无法恢复'}
        if player.attribute.getEnergy()<=200-30:
            player.attribute.updateEnergy(player.attribute.getEnergy()+30)
        else:
            player.attribute.updateEnergy(200)
        
        player.finance.updateGold(player.finance.getGold()-35)
        
        
        count=dbDrinkery.getByTypeAndCharacterid(characterid, typeid+1)
        if count==1:
            return{'result':False,'message':u'普通果汁酒今天已经使用了 1次'}
        if count==0:
            add(characterid,3,1)
        
    pushObjectNetInterface.pushUpdatePlayerInfo(player.dynamicId)
    return{'result':True,'message':Lg().g(166)}
        
        
        
        