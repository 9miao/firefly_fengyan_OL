#coding:utf8
'''
Created on 2011-9-17
物品操作
@author: SIOP_09
'''

from app.scense.core.PlayersManager import PlayersManager

import math
from app.scense.core.Item import Item

def renovateItem(characterid,itemid):
    '''修理装备
    @param itemid: int 装备id 0修理全部装备
    '''
    player=PlayersManager().getPlayerByID(characterid)    
    listd=player.pack.getPackCategory(1).items
    coinCount=0 #修理的总费用
    for it in listd:
        item=it.get('wholeItem').get('itemComponent') #物品实例
        dn=item.attribute.getDurability() #当前耐久度
        zn=item.baseInfo.getItemTemplateInfo().get('baseDurability') #最大耐久
        coin=item.baseInfo.getItemTemplateInfo().get('buyingRateCoin')#出售铜币价格
        if not dn==zn:#如果当前耐久度没有达到最大耐久度
            coinCount+=coin*.05            
            item.attribute.updateDurability(zn)#修理装备
    player.finance.updateCoin(player.finance.getCoin+int(math.ceil(coinCount)))#跟新游戏币
    
def getInfoByitemid(itemid):
    '''根据角色拥有的物品id获取物品信息
    @param itemid: int 物品id
    '''
    Item(id=itemid)