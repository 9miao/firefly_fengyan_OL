#coding:utf8
'''
Created on 2012-3-2

@author: sean_lan
'''
from app.gate.serverconfig.localservice import localservice
from app.gate.core.VCharacterManager import VCharacterManager
from app.gate.core.UserManager import UsersManager
from app.gate.bridge.famsermanger import FamSerManager
from app.gate.bridge.scenesermanger import SceneSerManager
from firefly.server.globalobject import GlobalObject,rootserviceHandle


@rootserviceHandle
def pushObject(topicID,msg,sendList):
    '''推送消息
    '''
    root=GlobalObject().root
    root.callChild('net',"pushData",topicID,msg,sendList)

@rootserviceHandle
def forwarding(key,dynamicId,data): #net传过来的信息
    '''分配处理netserver转发的请求
    @param key: int 请求的指令号
    @param conn: Conn Object Client到netserver的连接
    @param data: str Client 发送过来的数据
    '''
    if localservice._targets.has_key(key):
        return localservice.callTarget(key,dynamicId,data)
    else:
        from app.gate.basicapp.pushObject import pushOtherMessage
        from app.gate.utils.dbopera.db_language_login import getLanguageStr
        user = UsersManager().getUserByDynamicId(dynamicId)
        if not user:
            msg = getLanguageStr('conn_error')
            pushOtherMessage(msg,[dynamicId])
            return
        oldvcharacter = VCharacterManager().getVCharacterByClientId(dynamicId)
        if oldvcharacter.getLocked():#判断角色对象是否被锁定
            return
        node = VCharacterManager().getNodeByClientId(dynamicId)
        root=GlobalObject().root
        return root.callChild(node,key,dynamicId,data)
    
def SavePlayerInfoInDB(dynamicId):
    '''将玩家信息写入数据库'''
    vcharacter = VCharacterManager().getVCharacterByClientId(dynamicId)
#    node = vcharacter.getNode()
    root=GlobalObject().root
    d = root.callChild("scense_1000",2,dynamicId)
#    pid = vcharacter.getCharacterId()
#    if TeamFight.ishaveTeamFight(pid):
#        root.callChild(9999,4307,dynamicId,pid)
    return d

def SaveDBSuccedOrError(result,vcharacter):
    '''写入角色数据成功后的处理
    @param result: 写入后返回的结果
    @param vcharacter: 角色的实例
    '''
    vcharacter.release()#释放角色锁定
    return True

def dropClient(deferResult,dynamicId,vcharacter):
    '''清理客户端的记录
    @param result: 写入后返回的结果
    '''
    node =201000# vcharacter.getNode()
    if node<=0:
        return
    elif 200000<node<300000:#角色在场景中的处理
        SceneSerManager().dropClient(node, dynamicId)
    elif node>=300000:#角色在副本中的处理
        famserId = node - 300000
        famId = vcharacter.getFamId()
        FamSerManager().leaveFam(famserId, famId, dynamicId)
        
    VCharacterManager().dropVCharacterByClientId(dynamicId)
    UsersManager().dropUserByDynamicId(dynamicId)
    
@rootserviceHandle
def NetConnLost_2(dynamicId):
    '''客户端断开连接时的处理
    @param dynamicId: int 客户端的动态ID
    '''
    vcharacter = VCharacterManager().getVCharacterByClientId(dynamicId)
    if vcharacter and vcharacter.getNode():#判断是否已经登入角色
        vcharacter.lock()#锁定角色
        d = SavePlayerInfoInDB(dynamicId)#保存角色,写入角色数据
        d.addBoth(SaveDBSuccedOrError,vcharacter)#解锁角色
        d.addCallback(dropClient,dynamicId,vcharacter)#清理客户端的数据
    else:
        UsersManager().dropUserByDynamicId(dynamicId)
        
@rootserviceHandle
def ChatConnLost_3(broker,dynamicId):
    '''客户端断开连接时的处理
    @param dynamicId: int 客户端的动态ID
    '''
    pass

@rootserviceHandle
def ChatConnLost_4(dynamicId):
    '''客户端断开连接时的处理
    @param dynamicId: int 客户端的动态ID
    '''
    pass

    
@rootserviceHandle
def pushObjectByCharacterId_10(topicID,msg,sendList):
    '''根据角色的ID推送消息'''
    _sendList = [VCharacterManager().getClientIdByCharacterId(cid) for cid in sendList]
    root=GlobalObject().root
    root.callChild('net',"pushData",topicID,msg,_sendList)
    
@rootserviceHandle
def pushObjectToAll_11(topicID,msg):
    '''根据角色的ID推送消息'''
    _sendList = [cid for cid in VCharacterManager().client_character.keys()]
    root=GlobalObject().root
    root.callChild('net',"pushData",topicID,msg,_sendList)



