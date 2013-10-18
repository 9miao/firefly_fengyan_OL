#coding:utf8
'''
Created on 2011-8-19
@author: SIOP_09
'''

from app.scense.utils.dbopera import dbMonster
from app.scense.core.Item import Item
from twisted.python import log
import random

alldrop={}
base=1000000 #几率的基数
fbitemcount=27 #副本翻牌子得牌子数量

def jc():
    for key in alldrop.keys():
        if key==4001:
            pass
#            a=""
#            b=a
        try:
            for i in alldrop[key].get('itemid'):
                del i
                pass
                #sf=i[2]
        except:
            print key

def getByDropOutByid(did):
    '''根据掉落did获取掉落信息 (适用于副本,返回一个字典,分三个部分,1 items存储掉落物品实例  2 coupon存储绑定钻  3 gold存储游戏币)
    @param id: int 掉落id
    '''
    tlist=[] #存储副本掉落
    
    
    
    
    try:
        data=alldrop.get(did,None)
        for item in data.get('itemid'):
            dt={"item":None,"coin":0,"coupon":0}
            abss=random.randint(1,base)
            if abss>=1 and abss<=item[2]:#如果随机出来此物品
                abss=random.randint(1,item[1]) #物品数量
                item1=Item(item[0])
                item1.pack.setStack(abss)
                dt['item']=item1
                tlist.append(dt)
                
        coupon=data.get('coupon')
        if len(coupon)>2:
            dt={"item":None,"coin":0,"coupon":0}
            cp=eval("["+coupon+"]")
            abss=random.randint(1,base)
            if abss>=1 and abss<=cp[1]:
                dt["coupon"]=cp[0]
                tlist.append(dt)
        
        if len(tlist)<fbitemcount:
            lower=data.get('lower',-1)
            upper=data.get('upper',-1)
            if lower>0 and upper>0 and upper>=lower:
                for i in range(fbitemcount-len(tlist)):
                    dt={"item":None,"coin":0,"coupon":0}
                    dt['coin']=random.randint(lower,upper)
                    tlist.append(dt)
                    del i
            else: 
                for i in range(fbitemcount-len(tlist)):
                    dt={"item":None,"coin":0,"coupon":0}
                    dt['coin']=1
                    tlist.append(dt)
    except:
        for it in range(fbitemcount):
            dt={"item":None,"coin":0,"coupon":0}
            dt['coin']=random.randint(1,1000)
            tlist.append(dt)
            del it
    if len(tlist)>0:
        return random.sample(tlist,fbitemcount)
        
    return None

def getDropByid(did):
    '''根据怪物id获取掉落物品信息 (适用于 怪物掉落 返回一个掉落物品)
    @param did: int 怪物掉落表主键id
    '''
    data=alldrop.get(did,None)
    if not data:
        log.err(u'掉落表填写错误不存在掉落信息-掉落主键:%d'%did)
        return None
    for item in data.get('itemid'):
        abss=random.randint(1,base)
        if abss>=1 and abss<=item[2]:#如果随机出来此物品
            abss=random.randint(1,item[1]) #物品数量
            item1=Item(item[0])
            item1.pack.setStack(abss)
            return item1
    return None

def getDropByMosterid(mosterid):
    '''根据怪物id获取掉落物品信息
    @param mosterid: int 怪物id
    '''
    data=dbMonster.All_MonsterInfo.get(mosterid)
    if not data:
        return None
    dropid=data['dropoutid']#掉落表主键id
    data=getDropByid(dropid)
    return data

    
        
