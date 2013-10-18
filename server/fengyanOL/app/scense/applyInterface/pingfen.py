#coding:utf8
'''
Created on 2011-9-21
评分
@author: SIOP_09
'''
from app.scense.core.PlayersManager import PlayersManager
from app.scense.utils.dbopera import dbTopitem
from app.scense.core.Item import Item
from app.scense.core.toplist.TopList import TopList
from app.scense.core.language.Language import Lg

def getPFenByCharacterId(characterid):
    '''给装备评分
    @param characterid: int 角色id
    '''
    player=PlayersManager().getPlayerByID(characterid)
    if not player:
        return{"result":False,'message':Lg().g(199),'data':None}
    dt=[]
    ndt=[]#排序好的列表
    data=player.pack.getEquipmentSlot().getItemList()

    for item in data:
        data={}
        tp=item.get('position') #装备人物的位置
        it=item.get('itemComponent') #物品对象
        ql=it.attribute.strengthen #强化等级
        pl=it.baseInfo.getItemTemplateInfo().get('baseQuality') #品质
        pf=(ql+pl)*10 #评分数
        itemid=it.baseInfo.id
        if tp==9 or tp==10:
            iam=TopList().iarm#武器排行列表
            __F(iam, itemid, pf, data, dt, 0,tp)
                    
        if tp>=1 and tp<=6:
            iar=TopList().iaccouter
            __F(iar, itemid, pf, data, dt, 1,tp)
        if tp==7 or tp==8:
            ian=TopList().iadorn
            __F(ian, itemid, pf, data, dt, 2,tp)
        
    if len(dt)<1:
        return False
    
    fl=[9,10,1,2,3,4,5,6,7,8] #主武器  副武器  头部 肩部 胸部 手部 腿部 脚部 项链 戒指    
    for i in fl:
        for item in dt:
            if item.get('tp')==i:
                ndt.append(item)    
    return ndt
                                
def __F(iam,itemid,pf,data,dt,typeid,tp):
    if len(iam)<100:
        dbTopitem.addTop(itemid, typeid, pf)
        data['item']=Item(id=itemid) #物品
        data['pf']=pf #评分
        data['tp']=tp #装备位置
        dt.append(data)
        TopList().updateiaitem(0)
        TopList().updateiaitem(1)
        TopList().updateiaitem(2)
    else:
        TopList().updateiaitem(0)
        TopList().updateiaitem(1)
        TopList().updateiaitem(2)
        dbTopitem.updateTop(iam[99].get('itemid'), itemid, pf)
        data['item']=Item(id=itemid) #物品
        data['pf']=pf
        data['tp']=tp #装备位置
        dt.append(data)
        
            