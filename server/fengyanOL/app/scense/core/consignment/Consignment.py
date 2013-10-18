#coding:utf8
'''
Created on 2011-8-31

@author: SIOP_09
'''
from app.scense.utils.dbopera import dbconsignment
from app.scense.core.PlayersManager import PlayersManager
from app.scense.core.Item import Item
from app.scense.netInterface import pushObjectNetInterface
from app.scense.core.language.Language import Lg

class Consignment:
    def __init__(self):
        '''初始化'''
        self.item=[]#存放寄卖的物品
        self.gold=[]#存放及买的货币
        
    def getAllCoin(self,change,ziduan,guize,page,counts,characterid=0):
        '''获取所有货币寄卖信息
        @param change:int 1金币兑换钻   2钻兑换金币 
        @param ziduan: string  1按时间排序,2按购买价格排序，3按物品价格排序
        @param guize: int 排序规则 1正序   2倒序
        @param page: int 当前页数
        @param counts: int 每页多少条信息
        @param characterid: int 当前用户角色id
        '''
        flist,count=dbconsignment.getAllcoin(change, ziduan, guize, page, counts, characterid)
        if not flist:
            return {'data':None,'count':0}
        return {'data':flist,'count':count}
    
    def getItemByLikeName(self,itemname,up,down,quality,type,ziduan,guize,page,counts,characterid=0):
        '''搜索寄卖物品 (模糊查询)
        @param itemname: int 物品名称  模糊查询
        @param up: int 物品等级上限  最大90 最小1
        @param down: int 物品等级下限  最大90 最小1
        @param quality: int 物品品质 1灰 2白 3绿 4蓝 5紫 6橙 7红
        @param type: int 物品类型
        @param ziduan: string 排序字段   name,levelRequire,addtime,price
        @param guize: int 排序规则   1正序    2倒序
        @param page: int 当前页数
        @param counts: int 每页多少条信息
        @param characterid: int 当前用户角色id  如果characterid>0的话 ,说明查询的是自己的物品
        '''
        flist,count=dbconsignment.getItemByLikeItemName(itemname, up, down, quality, type, ziduan, guize, page, counts, characterid)
        if not flist:
            return {'data':None,'count':0}
        return {'data':flist,'count':count}
    def addItem(self,itemId,characterId,coinnum,cointype,addtime,stack):
        '''添加寄卖物品
        @param itemId: int 物品id (tb_item主键)
        @param characterId: int 寄卖人角色id
        @param coinnum: int 物品货币数量
        @param cointype: int 物品货币类型
        @param addtime: int 寄售多少小时
        @param stack: int 物品层叠数
        '''
        player=PlayersManager().getPlayerByID(characterId)
        if not player:
            return{'result':False,'message':Lg().g(199)}
        ks=stack*10 #寄卖物品应缴纳的手续费(金币)
        if player.finance.getCoin()<ks:
            return{'result':False,'message':Lg().g(512)}
        else:
            player.finance.updateCoin(player.finance.getCoin()-ks) #扣除寄卖人的手续费

        packone=player.pack._package.getWholePagePack() #获取角色的全部物品包裹
        position = packone.getPositionByItemId(itemId) #物品在包裹中的位置
        if position==-1:
            return {'result':False ,'message':Lg().g(513)}
        result1 = player.pack.dropItem(position,3,stack,tag = 0) #删除物品 
        if not result1.get('result',False):
            #print'添加寄卖物品时没有删除物品'
            return {'result':False ,'message':result1.get('message',False)}
        result=dbconsignment.addItem(itemId, characterId, coinnum, cointype, addtime, stack)
        if not result:
            return {'result':False ,'message':Lg().g(514)}
        pushObjectNetInterface.pushUpdatePlayerInfo(player.dynamicId)
        return {'result':True ,'message':u'寄卖成功'}
    
    def addGold(self,salemoney,saletype,buymoney,buytype,adtime,characterid):
        '''添加寄卖金币
        @param salemoney: int 寄卖者出售货币数量
        @param saletype: int 寄卖者出售货币类型 1钻 2金币
        @param buymoney: int 购买货币数量
        @param buytype: int 购买货币类型  1钻 2金币
        @param adtime: int 寄售的小时数
        @param characterid: int 寄卖者的id
        '''
        player=PlayersManager().getPlayerByID(characterid)
        if not player:
            return{'result':False,'message':Lg().g(199)}
        
        if saletype==1:
            if salemoney>player.finance.getGold():
                return{'result':False,'message':u'钻不足'}
            player.finance.updateGold(player.finance.getGold()-salemoney)
        if saletype==2:
            if salemoney>player.finance.getCoin():
                return{'result':False,'message':Lg().g(88)}
            player.finance.updateCoin(player.finance.getCoin()-salemoney)
        result=dbconsignment.addGold(salemoney, saletype, buymoney, buytype, adtime, characterid)
        if not result:
            return{'result':False,'message':u'添加寄卖表失败'}
        pushObjectNetInterface.pushUpdatePlayerInfo(player.dynamicId)
        return{'result':False,'message':u'添加寄卖成功'}
    def buyGold(self,characterid,id):
        '''购买寄卖货币
        @param characterid: 购买人id
        @param id: 货币寄卖表主键id
        '''
        item=dbconsignment.getOneGold(id)
        player=PlayersManager().getPlayerByID(characterid)
        if not player:
            return{'result':False,'message':Lg().g(199)}
        buymoney=item.get('buymoney',0)#换取的货币数量
        buytype=item.get('buytype',1)#换取的货币种类    1钻 2金币
        
        if buytype==1:
            if player.finance.getGold()<buymoney:
                return{'result':False,'message':u'您钻不足，无法购买。'}
        elif buytype==2:
            if player.finance.getCoin()<buymoney:
                return{'result':False,'message':u'您金币不足，无法购买。'}
                    
        result=dbconsignment.buyGold(characterid, id,item)
        if result:
            pushObjectNetInterface.pushUpdatePlayerInfo(player.dynamicId)
            return{'result':True,'message':Lg().g(193)}
        else:
            return{'result':False,'message':Lg().g(470)}
    def buyItem(self,characterid,id):
        '''购买寄卖物品
        @param characterid: int 购买者的角色id
        @param id: int 物品寄卖表的主键id
        '''
        item = dbconsignment.getItemByoneid(id) #获取寄卖物品信息
        if not item:
            return{'result':False,'message':u'该物品已下架','data':None}
        tocharacterid=item.get('characterid',0) #寄卖物品的角色id
        itemid=item.get('itemid',0) #tb_item中的主键id
        buymoney=item.get('coinnum',0) #购买物品需要的货币数量
        if buymoney==0:
            return{'result':False,'message':u'价格不能为0','data':None}
        buytype=item.get('cointype',0) #购买物品需要的货币类型  1钻 2金币
        if buytype==1:
            buytype==2
        elif buytype==2:
            buytype==1
        counts=item.get('count',0) #购买的数量
        player=PlayersManager().getPlayerByID(characterid)
        if not player:
            return{'result':False,'message':Lg().g(199)}
        if buytype==1:
            if player.finance.getGold()<buymoney:
                return{'result':False,'message':u'您钻不足，无法购买。'}
        elif buytype==2:
            if player.finance.getCoin()<buymoney:
                return{'result':False,'message':u'您金币不足，无法购买。'}
        
        result=player.shop.buyConsItem(tocharacterid,id,counts,itemid,buymoney,buytype)
        pushObjectNetInterface.pushUpdatePlayerInfo(player.dynamicId)
        return result
    