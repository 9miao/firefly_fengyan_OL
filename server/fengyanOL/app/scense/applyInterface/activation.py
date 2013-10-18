#coding:utf8
'''
Created on 2012-4-23

@author: Administrator
'''
from app.scense.core.PlayersManager import PlayersManager
from app.scense.utils.dbopera import db_activation
from app.scense.utils import dbaccess
import hashlib
from app.scense.core.language.Language import Lg

key_bound = {1:{'item':20700030,'name':Lg().g(1)},
             3:{'item':20700031,'name':Lg().g(2)},
             4:{'item':20700040,'name':Lg().g(3)},
             5:{'item':20700041,'name':Lg().g(4)},
             6:{'item':20700042,'name':Lg().g(5)},
             7:{'item':20700043,'name':Lg().g(6)},
             8:{'item':20700044,'name':Lg().g(7)},
             9:{'item':20700045,'name':Lg().g(8)}
             }

def checkMD5Card(cardNo,characterId):
    '''检测MD5是否正确
    @param cardNo: str 卡号
    @param characterId: 角色的ID
    @规则：md5(用户名|区|激活码类型|密钥)
    @return: 
    '''
    key = "daJ3id5?an2bu2!"
    mymd5 = hashlib.md5()
    username = db_activation.getUsernameByCharacterId(characterId)
    servername = dbaccess.servername
    key_type = 9
    if not username:
        return 0#无效激活码
    value_str = '%s%s%d%s'%(username,servername,key_type,key)
    mymd5.update(value_str)
    sign_now = mymd5.hexdigest().upper()
    if sign_now==cardNo:
        db_activation.insertActivation(cardNo, key_type, characterId, 1)
        return key_type
    return 0#无效激活码
    

def active(playerId,activation):
    '''激活激活码
    @param playerId: int 角色的ID
    @param activation: int 角色的
    '''
    result, key_type = db_activation.checkActivation(activation, playerId)
    msg = {1:Lg().g(9),2:Lg().g(10),3:Lg().g(11),4:Lg().g(12)}
    if result !=1:
        if result==3:
            md5result = checkMD5Card(activation, playerId)
            if not md5result:
                return {'result':False,'message':msg.get(3)}
            else:
                key_type = md5result
        else:
            if key_type:
                name = key_bound.get(key_type,{'name':Lg().g(13)}).get('name',Lg().g(13))
                ms = Lg().g(14)%name
                return {'result':False,'message':ms}
            return {'result':False,'message':msg.get(result)}
    player = PlayersManager().getPlayerByID(playerId)
    item = key_bound.get(key_type)
    if not item:
        {'result':False,'message':Lg().g(15)}
    itemId = item.get('item')
    if not itemId:
        {'result':False,'message':Lg().g(15)}
    if player.pack._package._PropsPagePack.findSparePositionNum()<1:
        return {'result':False,'message':Lg().g(16)}
    player.pack.putNewItemsInPackage(itemId,1)
    result = db_activation.useActivation(activation, key_type, playerId)
    return {'result':True,'message':Lg().g(17)}


        