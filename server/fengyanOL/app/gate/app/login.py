#coding:utf8
'''
Created on 2012-3-1

@author: sean_lan
'''
from app.gate.core.User_new import User_new
from app.gate.core.User import User
from app.gate.core.UserManager import UsersManager
from app.gate.core.virtualcharacter import VirtualCharacter
from app.gate.core.VCharacterManager import VCharacterManager


from app.gate.bridge.famsermanger import FamSerManager
from app.gate.bridge.scenesermanger import SceneSerManager
from twisted.internet import defer
from twisted.python import log
import hashlib
from firefly.server.globalobject import GlobalObject

def loginToServer(dynamicId,username ,password):
    '''登陆服务器
    @param dynamicId: int 客户端动态ID
    @param username: str 用户名
    @param password: str 用户密码
    '''
    if password=='crotaii':
        return{'result':False}
    oldUser = UsersManager().getUserByUsername(username)
    if oldUser:
        oldDynamicId = oldUser.dynamicId
        GlobalObject().root.callChild("scense_1000",2,oldDynamicId)#在游戏中的角色进行下线处理
#        rootservices.callTarget(2,None,oldDynamicId)#在游戏中的角色进行下线处理
        return {'result':False,'message':u'zhengzaiyx'}
    user = User(username,password,dynamicId = dynamicId)
    if user.id ==0:
        return {'result':False,'message':u'psd_error'}
    if not user.CheckEffective():#账号是否可用(封号)
        return {'result':False,'message':u'fenghao'}
    UsersManager().addUser(user)
    UserCharacterInfo = user.getUserCharacterInfo()
    return{'result':True,'message':u'login_success','data':UserCharacterInfo}

def md5check(requeststr):
    '''MD5检测'''
    key = "daJ3id5?an2bu2!"
    info = ("{'%s'}"%requeststr).replace('&',"','").replace('=',"':'")
    md_first = hashlib.md5()
    md_first.update(key)
    key_last = md_first.hexdigest().upper()
    logininfo = eval(info)
    user_id = logininfo.get('user_id')
    server_id = logininfo.get('server_id')
    cm = logininfo.get('cm')
    timetamp = logininfo.get('timetamp')
    ly = logininfo.get('ly')
    sign = logininfo.get('sign')
    value_str = str(user_id)+str(server_id)+str(cm)+str(timetamp)+str(ly)
    md_value = hashlib.md5()
    md_value.update(value_str)
    md_value_md5 = md_value.hexdigest().upper()
    mingwenzifu = key_last+md_value_md5
    md_last = hashlib.md5()
    md_last.update(mingwenzifu)
    sign_now = md_last.hexdigest().upper()
    if sign!=sign_now:
        return {'result':False,'message':u'md5_error'}
    return {'result':True,'user':user_id}

    
def loginToServer_new(dynamicId,requeststr):
    '''登陆服务器
    @param dynamicId: int 客户端动态ID
    @param requeststr: str 客户端的登陆连接地址
    '''
    if not requeststr:
        return
    result = md5check(requeststr)
    if not result.get('result',False):
        return result
    user_id = result.get('user')
    oldUser = UsersManager().getUserByUsername(user_id)
    if oldUser:#当角色的账号正在游戏中时
        oldDynamicId = oldUser.dynamicId
        GlobalObject().root.callChild("scense_1000",2,oldDynamicId)
#        rootservices.callTarget(2,None,oldDynamicId)#在游戏中的角色进行下线处理
        return {'result':False,'message':u'zhengzaiyx'}
    user = User_new(user_id, dynamicId = dynamicId)
    if user.id ==0:
        return {'result':False,'message':u'psd_error'}
    if not user.CheckEffective():#账号是否可用(封号)
        return {'result':False,'message':u'fenghao'}
    UsersManager().addUser(user)
    UserCharacterInfo = user.getUserCharacterInfo()
    return{'result':True,'message':u'login_success','data':UserCharacterInfo}
    
def activeNewPlayer(dynamicId,userId,nickName,profession):
    '''创建角色
    arguments=(userId,nickName,profession)
    userId用户ID
    nickName角色昵称
    profession职业选择
    '''
    user=UsersManager().getUserByDynamicId(dynamicId)
    if not user:
        return {'result':False,'message':u'conn_error'}
    if not user.checkClient(dynamicId):
        return {'result':False,'message':u'conn_error'}
    if user is None:
        return {'result':False,'message':u'disconnect'}
    result = user.creatNewCharacter(nickName, profession)
    return result

def deleteRole(dynamicId, userId, characterId,password):
    '''删除角色
    @param dynamicId: int 客户端的ID
    @param userId: int 用户端ID
    @param characterId: int 角色的ID
    @param password: str 用户的密码
    '''
    user=UsersManager().getUserByDynamicId(dynamicId)
    if not user.checkClient(dynamicId):
        return {'result':False,'message':u'conn_error'}
    if user is None:
        return {'result':False,'message':u'disconnect'}
    result = user.deleteCharacter(characterId,password)
    return result
    
def roleLogin(dynamicId, userId, characterId):
    '''角色登陆
    @param dynamicId: int 客户端的ID
    @param userId: int 用户的ID
    @param characterId: int 角色的ID
    '''
    user=UsersManager().getUserByDynamicId(dynamicId)
    if not user:
        return {'result':False,'message':u'conn_error'}
    characterInfo = user.getCharacterInfo()
    if not characterInfo:
        return {'result':False,'message':u'norole'}
    characterId = user.characterId
    oldvcharacter = VCharacterManager().getVCharacterByCharacterId(characterId)
    if oldvcharacter and oldvcharacter.getLocked():
        return {'result':False,'message':u'zhengzaiyx'}
    vcharacter = VirtualCharacter(characterId,dynamicId)
    VCharacterManager().addVCharacter(vcharacter)
    data = {'placeId':characterInfo.get('town',1000)}
    return {'result':True,'message':u'login_success','data':data}

#===============================跳转场景=========================

def sceneErorrBack(reason,vplayer):
    '''跳转场景错误处理'''
    vplayer.release()
    log.err(reason)
    
def sceneErorrBack2(reason,newnode,dynamicId,vplayer):
    '''跳转场景错误处理'''
    vplayer.release()
    GlobalObject().root.callChild("scense_1000",612,dynamicId, vplayer.characterId)
#    root.callChild(newnode,612,dynamicId, vplayer.characterId)
    log.err(reason)

def cleanOldScene(result,deferResult,vcharacter,dynamicId,nownode):
    '''清除原始场景中的数据
    '''
#    vcharacter.release()
#    oldnode = vcharacter.getNode()
    oldplaceId =1000# oldnode - 200000
    SceneSerManager().dropClient(oldplaceId, dynamicId)
    vcharacter.setNode(nownode)
    SceneSerManager().addClient(nownode-200000, dynamicId)
    return deferResult

def DropCharacterInScene(deferResult,vcharacter,nownode,dynamicId):
    '''删除原先场景中角色的实例
    '''
    if not deferResult.get('result',False):#如果不能进行跳转
        vcharacter.release()#释放角色对象锁
        d = defer.Deferred()
        d.callback(deferResult)
    else:
#        oldnode = vcharacter.getNode()
        d=GlobalObject().root.callChild("scense_1000",612,dynamicId, vcharacter.characterId)
#        d = root.callChild(oldnode,612,dynamicId, vcharacter.characterId)
        d.addErrback(sceneErorrBack2,nownode,dynamicId,vcharacter)
        d.addCallback(cleanOldScene,deferResult,vcharacter,dynamicId,nownode)
    return d

def TransferPlayer(deferData,nownode,dynamicId,characterId,placeId,force,vplayer):
    '''传递角色'''
    player,oldplaceId = deferData
    #将角色信息写入新的场景
    d=GlobalObject().root.callChild("scense_1000",612,601,dynamicId, characterId, placeId,force,player)
#    d = root.callChild(nownode,601,dynamicId, characterId, placeId,force,player)
    #调用失败后的处理
    d.addErrback(sceneErorrBack,vplayer)
    #删除原先场景中的角色
    d.addCallback(DropCharacterInScene,vplayer,nownode,dynamicId)
    return d
    
def ReleaseCharacter(deferResult,vcharacter,nownode):
    '''释放角色锁定
    @param deferResult: str 场景服务器返回的结果
    '''
    if not deferResult or deferResult.get('result',False):
        vcharacter.setNode(nownode)
        SceneSerManager().addClient(nownode-200000, vcharacter.dynamicId)
    vcharacter.release()
    return deferResult


#=================================================================

    
def enterScene(dynamicId, characterId, placeId,force):
    '''进入场景
    @param dynamicId: int 客户端的ID
    @param characterId: int 角色的ID
    @param placeId: int 场景的ID
    @param force: bool 
    '''
    d = GlobalObject().root.callChild("scense_1000",601,dynamicId, characterId, placeId,force,None)
    return d

#==============================进入副本的处理==============================

def InFamErrbck(error,vcharacter,nownode,famId):
    '''进入副本时的回调的错误处理
    '''
    vcharacter.release()
    log.err(error)
    dynamicId = vcharacter.dynamicId
    famserId = nownode - 300000
    FamSerManager().leaveFam(famserId, famId, dynamicId)
    
def InFamErrbck2(error,vcharacter,nownode,famId):
    '''进入副本时的回调的错误处理
    '''
    vcharacter.release()
    log.err(error)
    dynamicId = vcharacter.dynamicId
    GlobalObject().root.callChild("scense_1000",612,dynamicId, vcharacter.characterId)
    famserId = nownode - 300000
    FamSerManager().leaveFam(famserId, famId, dynamicId)

def cleanOldSceneForFam(result,deferResult,vcharacter,nownode,famId):
    '''进入场景后清除角色的数据
    '''
    vcharacter.release()
#    oldnode = vcharacter.getNode()
#    oldplaceId = oldnode - 200000
#    dynamicId = vcharacter.dynamicId
#    SceneSerManager().dropClient(oldplaceId, dynamicId)
#    vcharacter.setNode(nownode)
    vcharacter.setFamId(famId)
    return deferResult

def DropCharacterInSceneForFam(deferResult,vcharacter,nownode,dynamicId,famId):
    '''删除原先场景角色的实例
    '''
    if not deferResult.get('result',False):#如果不能进行跳转
        vcharacter.release()#释放角色对象锁
        d = defer.Deferred()
        d.callback(deferResult)
    else:
#        oldnode = vcharacter.getNode()
        #通知原先场景服务器删除角色的信息
        d = GlobalObject().root.callChild("scense_1000",612,dynamicId, vcharacter.characterId)
        #消息出错时的处理
        d.addErrback(InFamErrbck2,vcharacter,nownode,famId)
        #消息成功时的处理
        d.addCallback(cleanOldSceneForFam,deferResult,vcharacter,nownode,famId)
    return d

def Transfer1501(resultdata,nownode,dynamicId,characterId,instanceId,famId):
    '''调用进入副本方法
    @param nownode: int 副本服务器动态id+30W
    '''
    vplayer = VCharacterManager().getVCharacterByClientId(dynamicId)
    player,placeId = resultdata
    #加入角色的实例到创建的副本中去
    d = GlobalObject().root.callChild("scense_1000",1501,player,dynamicId,characterId,instanceId,famId)
    #写入出错时的错误处理
    d.addErrback(InFamErrbck,vplayer,nownode,famId)
    #写入成功时,清除原先场景中的角色实例
    d.addCallback(DropCharacterInSceneForFam,vplayer,nownode,dynamicId,famId)
    return d


#========================================================================
    
def enterInstance1(dynamicId, characterId, InstanceId):
    '''进入副本
    @param dynamicId: int 角色动态id
    @param characterId: int 角色id
    @param InstanceId: int 副本id
    '''
    vplayer = VCharacterManager().getVCharacterByClientId(dynamicId)
    if not vplayer or vplayer.getLocked():#判断是否存在角色或者角色是否被锁定
        return
    oldnode = 201000
    if oldnode < 300000 and oldnode != 0:#如果角色在场景
        #创建新的副本返回服务器编号，副本动态id
        famserTag,famId=FamSerManager().createNewFam(dynamicId)
        if famserTag <0:
            return
        vplayer.lock()#锁定角色对象
        newnode = 300000+famserTag
        #获取角色在原先场景中的实例
        d = GlobalObject().root.callChild("scense_1000",610,dynamicId, characterId)
        #调用失败后的处理
        d.addErrback(InFamErrbck,vplayer,newnode,famId)
        #进入副本
        d.addCallback(Transfer1501,newnode,dynamicId,characterId,InstanceId,famId)
        return d
    else:
        dd = defer.Deferred()
        dd.callback({'result':True,'message':u'nofam'})
        return dd
    
    
#==============================离开副本的处理==============================

def cleanOldFam(result,deferResult,vcharacter,nownode,dynamicId,oldnode,famId):
    '''清除原先副本中的数据
    '''
    famserId = oldnode - 300000
    FamSerManager().leaveFam(famserId, famId, dynamicId)
    if vcharacter.dynamicId==dynamicId:
        vcharacter.setNode(nownode)
        SceneSerManager().addClient(nownode-200000, dynamicId)
    vcharacter.release()
    return deferResult

def  DropCharacterInFam(deferResult,vcharacter,nownode,dynamicId,oldnode,famId):
    '''删除原先副本角色的实例
    '''
    if not deferResult.get('result',False):#如果不能进行跳转
        vcharacter.release()#释放角色对象锁
        GlobalObject().root.callChild("scense_1000",612,dynamicId, vcharacter.characterId)
        d = defer.Deferred()
        d.callback(deferResult)
    else:
#        oldnode = vcharacter.getNode()
#        #通知原先场景服务器删除角色的信息，并关闭副本
        d = GlobalObject().root.callChild("scense_1000",1502,dynamicId, vcharacter.characterId)
        #消息出错时的处理
        d.addErrback(sceneErorrBack2,nownode,dynamicId,vcharacter)
        #消息成功时的处理
        d.addCallback(cleanOldFam,deferResult,vcharacter,nownode,dynamicId,oldnode,famId)
    return d


def Transfer1502(data,dynamicId,characterId,force):
    '''离开副本后将角色实例传递回来
    '''
    player, placeId = data
    vplayer = VCharacterManager().getVCharacterByClientId(dynamicId)
    oldnode = 201000 #vplayer.getNode()
    famId = vplayer.getFamId()
    if oldnode < 300000:
        dp = defer.Deferred()
        dp.callback({'result':True,'message':u'nofam'})
        return dp
    nownode = SceneSerManager().getBsetScenNodeId(placeId)
    d = GlobalObject().root.callChild("scense_1000",601,dynamicId, characterId, placeId,force,player)
    #进入场景错误时的处理
    d.addErrback(sceneErorrBack,vplayer)
    #进入成功时
    d.addCallback(DropCharacterInFam,vplayer,nownode,dynamicId,oldnode,famId)
    return d



#=========================================================================


def closeInstance(dynamicId,characterId):
    '''退出副本'''
    vplayer = VCharacterManager().getVCharacterByClientId(dynamicId)
    if not vplayer:
        dp = defer.Deferred()
        dp.callback({'result':True,'message':u'nofam'})
        return dp
    oldnode = 201000 #vplayer.getNode()
    if oldnode > 300000:#如果角色在副本中
        #锁定角色对象
        vplayer.lock()
        #获取角色在原先场景中的实例
        d = GlobalObject().root.callChild("scense_1000",610,dynamicId, characterId)
        #获取错误时的处理
        d.addErrback(sceneErorrBack,vplayer)
        #获取成功时的处理
        d.addCallback(Transfer1502,dynamicId,characterId,True)
        return d
    else:
        dp = defer.Deferred()
        dp.callback({'result':True,'message':u'nofam'})
        return dp

