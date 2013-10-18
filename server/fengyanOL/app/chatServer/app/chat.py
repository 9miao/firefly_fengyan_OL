#coding:utf8
'''
Created on 2011-4-14

@author: sean_lan
'''
from app.chatServer.net.pushObjectNetInterface import pushChatMessage
from app.chatServer.core.ChaterManager import ChaterManager
from app.chatServer.core.ChatRoomManager import ChatRoomManager

from app.chatServer.utils.dbopera import dbshieldword
from app.chatServer.app.gmhandle import doGmCommand
from app.chatServer.core.GuildManager import GuildManager
from app.chatServer.core.language.Language import Lg
#from core.scene.SceneManager import SceneManager_new
#from netInterface import pushObjectNetInterface
    
def loginToChatServer(dynamicId,characterId,roomId):
    '''登陆聊天服务器
    @param dynamicId: int 客户端的id
    @param characterId: int角色的id
    '''
    chater = ChaterManager().addChaterByid(characterId)
    if chater:
        ChaterManager().updateOnland(characterId,dynamicId)
        chater.setRoomId(roomId)
        ChatRoomManager().joinRoom( dynamicId, roomId)
    gid=chater.guildid#行会id 没有行会默认0
    dtid=chater.dynamicId
    GuildManager().add(dtid, gid)
    targetList = []
    targetList.append(dynamicId)
    content = Lg().g(638)
    pushChatMessage(5, -1, Lg().g(128), 0, content,[], targetList)
    return {'result':True,'message':Lg().g(25)}

    

def sendMessage(dynamicId,characterId,topic,content,linkData,tonickname=None):
    '''发送聊天信息
    @param dynamicId: int 客户端的id
    @param characterId: int 角色的id
    @param topic: int 频道的编号    
    @param content: string 发送的消息内容
    @param linkData: dict list 连接信息内容
    '''

    chater = ChaterManager().getChaterByCharacterId(characterId)
    if not chater:
        return {'result':False,'message':Lg().g(639)}
    if topic==7:
        toplayer=ChaterManager().getChaterByCharacterId(characterId)
        if not toplayer:
            return {'result':False,"message":Lg().g(640)}
        else:
            topic=toplayer.baseInfo.id
        
    targetList = []
    chaterName = chater.getCharacterName()
    profession = chater.getProfession()
    
    if topic==1: #世界频道聊天
        idlist = ChaterManager().getAlldynamicId()
        targetList=idlist
    elif topic==2:#当前 相当于同场景
        roomId = chater.getRoomId()
        targetList = ChatRoomManager().getRoomMember(roomId)

    elif topic==3:#国
        gid=chater.guildid
        if gid<1:
            return {'result':False,"message":Lg().g(641)}
        else:
#            return {'result':False,"message":u"国聊天功能暂未开放，敬请期待"}
#            idlist = ChaterManager().getAlldynamicId()
#            targetList=idlist
#            content=u"国聊天暂未开放"
            plist=GuildManager().getdtidListBygid(gid)
            if plist:
                targetList=list(plist)
                
#        gid=player.guild.getID()#返回行会id
#        resut=setGuildPlayerDynamicId(gid,targetList) #设置添加targetList，国聊天角色动态id列表,返回是否成功
#        if not resut:
#            return {'result':False,"message":Lg().g(641)}
    result = doGmCommand(characterId,content)
#    if not result:
    pushChatMessage(topic,characterId, chaterName, profession,
                     dbshieldword.replaceIllegalChar(content),linkData, targetList)
    return {'result':True}

def sendAnnouncement(msg):
    '''发送系统通告'''
    targetList = []
    for k in ChaterManager()._chaters:              
        targetId = ChaterManager()._chaters[k].dynamicId
        targetList.append(targetId)
    pushChatMessage(5, -1, Lg().g(128), 0, msg,[], targetList)
    
    
def sendGuildcement(msg,targetList = []):
    '''发送错误提示
    '''
    
    for k in ChaterManager()._chaters:              
        targetId = ChaterManager()._chaters[k].dynamicId
        targetList.append(targetId)
    pushChatMessage(7, -1, Lg().g(128), 0, msg,[], targetList)
    
def sendSysInfomation(msg,dynamicId,linkData=[]):
    """发送系统提示消息
    @param mag: 发送的聊天信息
    @param linkData: 物品提示信息
    @param dynamicId: 角色动态id
    """
    targetList = []
    dynamicId = ChaterManager().getChaterDynamicId
    if dynamicId:
        targetList.append(dynamicId)
    pushChatMessage(5, -1, Lg().g(128), -1, msg,linkData,targetList)

    
def sendSysInfomations_Item(msg,dynamicId,itemlist):
    """(根据物品实例列表)发送系统提示消息
    @param mag: 发送的聊天信息
    @param itemlist: 物品实例列表
    @param dynamicId: 角色动态id
    """
    targetList = []
    dynamicId = ChaterManager().getChaterDynamicId
    if dynamicId:
        targetList.append(dynamicId)
    if not itemlist:
        return
    linkData=[]
    for item in itemlist:
        it={}
        it['id']=item.baseInfo.id
        it['name']=item.baseInfo.getItemTemplateInfo().get('name','')
        it['chatEquipType']=0
        it['itemInfo']=item
        msg+=u"[%"+it['name']+u"%]  "
        linkData.append(it)
    pushChatMessage(5, -1, Lg().g(128),-1,Lg().g(642)+msg, linkData,targetList)
        



#def sss(dynamicId,msg=u""):
#    '''推送物品信息'''
#    
#    targetList = []
#    
#    setAllChatPlayerDynamicId(targetList)#设置targetList为所有在线聊天角色的动态id
#    
#    list=[]
#    list.append(Item(id=553))
#    list.append(Item(id=604))
#    list.append(Item(id=605))
#    linkData=[]
#    setlinkData(linkData)
#    for item in list:
#        it={}
#        it['id']=item.baseInfo.id
#        it['name']=item.baseInfo.getItemTemplateInfo().get('name','')
#        it['chatEquipType']=0
#        it['itemInfo']=item
#        msg+=u" 装备[%"+it['name']+"%]"
#        linkData.append(it)
#    #print msg+"sss()"
#    pushChatMessage(5, -1, Lg().g(128),-1,msg, linkData,targetList)

def aaa(msg=u""):
    '''推送世界消息'''
#    list=[]
#    list.append(PlayerCharacter(1000050))
    linkData=[]
    setlinkData(linkData)
#    for item in list:
#        it={}
#        it['id']=item.baseInfo.id
#        it['name']=item.baseInfo.getName()
#        it['chatEquipType']=1 #0代表物品  1代表角色
#        msg+=u"[%"+it['name']+"%]"
#        linkData.append(it)
        
    targetList = []
    setAllChatPlayerDynamicId(targetList)#设置targetList为所有在线聊天角色的动态id
    #print msg+"aaa()"
#    pushChatMessage(1, -1, Lg().g(128), -1, msg,[], targetList)
    pushChatMessage(5, -1, Lg().g(128),-1,msg, [],targetList)

#def fff(msg=u"",playerList=[],mag=u"",itemList=[]):
#    from core.character.PlayerCharacter import PlayerCharacter
#    linkData=[]
#    setlinkData(linkData)
#    itemList.append(Item(id=553))
#    itemList.append(Item(id=604))
#    itemList.append(Item(id=605))
#    
#    py1=PlayerCharacter(1000050)
#    playerList.append(py1)
#    
#    for item in playerList:
#        it={}
#        it['id']=item.baseInfo.id
#        it['name']=item.baseInfo.getName()
#        it['chatEquipType']=1 #0代表物品  1代表角色
#        msg+=u"[%"+it['name']+"%]"
#        linkData.append(it)
#    playerList.remove(py1)
#    msg+=mag
#    for item in itemList:
#        it={}
#        it['id']=item.baseInfo.id
#        it['name']=item.baseInfo.getItemTemplateInfo().get('name','')
#        it['chatEquipType']=0
#        it['itemInfo']=item
#        msg+=u" 装备 [%"+it['name']+"%]"
#        linkData.append(it)
#    targetList = []
#    setAllChatPlayerDynamicId(targetList)#设置targetList为所有在线聊天角色的动态id
#    #print msg +"fff()"
#    pushChatMessage(5, -1, Lg().g(128),-1,msg, linkData,targetList)
    
def setlinkData(linkData=[]):
    '''设置一个空的角色链接数据
    @param linkData: [] 连接数据  默认值为[]
    '''
    it={}
    it['id']=0
    it['name']=Lg().g(128)
    it['chatEquipType']=1 #0代表物品  1代表角色
    it['itemQuality']=0
    linkData.append(it)
    
def setAllChatPlayerDynamicId(targetList):
    '''设置所有在线聊天成员的动态id列表'''
    for k in ChaterManager()._chaters:              
        targetId = ChaterManager()._chaters[k].dynamicId
        targetList.append(targetId)
        
def setGuildPlayerDynamicId(gid,targetList):
    '''设置所在国中在线聊天成员的动态id列表-根据国id 有返回值（True or False）
    @param gid: int 国id
    @param targetList: [] 存储角色动态id
    '''
    rgetList1=''#dbGuild.getGuildMemberIdList(gid)#返回角色Id列表
    if len(rgetList1)>=1:
        for l in rgetList1:
            icno= ChaterManager().getChaterByCharacterId(l)
            if icno:
                targetList.append(icno.dynamicId)
    else:
        return False
    return True

#def setScenePlayerDynamicId(player,targetList):
#    '''设置所在场景中在线聊天成员的动态id-根据当前角色实例
#    @param player: object 角色实例
#    @param targetList: [] 角色动态id集合 
#    '''
#    
#    scene=None #场景实例
#    if player.baseInfo.getState()==0: #0表示玩家在普通场景       1表示玩家在副本    2行会战副本
#        sceneid=player.baseInfo.getTown() #场景id
#        scene= SceneManager_new().getSceneById(sceneid) #获取角色当前场景
#    elif player.baseInfo.getState()==1:
#        Instance=InstanceManager().getInstanceByIdTag(player.baseInfo.getInstancetag()) #获取角色当前副本
#        sceneid=player.baseInfo.getLocation() #场景id
#        scene=Instance.getScene(sceneid) #在副本中根据场景id 获取场景实例
#    dlist=scene._playerlist #字典类型
#    for itid in dlist:
#        targetList.append(ChaterManager().getChaterDynamicId(itid))
        
def setToPlayerDynamicId(characterid,targetList):
    '''设置私聊成员的动态id-根据接收方角色id 有返回值（True or False）
    @param characterid: int 接收方角色id
    '''
    inco=ChaterManager().getChaterByCharacterId(characterid)
    if inco:
        targetList.append(inco.dynamicId)
        return True
    else:
        return False   #{'result':False,"message":Lg().g(640)}
    
#def pushSystemToInfo(str):
#    '''推送系统公告信息（屏幕中央跑马灯）'''
#    sendList=[]
#    for player in PlayersManager()._players.values():
#        sendList.append(player.getDynamicId())
#    pushObjectNetInterface.pushSystemToInfo2700(str,sendList)
    
    