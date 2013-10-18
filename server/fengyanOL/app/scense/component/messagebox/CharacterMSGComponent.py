#coding:utf8
'''
Created on 2012-3-13
角色消息盒子组件
@author: lan
'''
from app.scense.component.Component import Component
from app.scense.netInterface.pushPrompted import pushPromptedMessageByCharacter
from app.scense.netInterface.pushObjectNetInterface import pushOtherMessageByCharacterId,pushCorpsApplication

LEVELUPMESSAGE = 1#升级的消息
TASKFILISHED = 2#任务完成

class CharacterMSGComponent(Component):
    '''角色消息盒子组件'''
    
    def __init__(self,owner):
        '''
        @param fightmsg: str list 角色战斗消息盒子,里面的消息只对自身发送
        @param fightTmsg: str lit 角色战斗3秒提示消息盒子
        @param publicmsg: str list 角色产生的公共消息
        @param pecifiedmsg: str list 角色产生的指定范围玩家的消息
        @param specialmsg: int set() 特殊消息 升级 完成任务
        @param systemToInfo: str list 系统公告（跑马灯）
        @param chatzh: str list 聊天框综合频道发送消息
        @param fightfailmsg: list 战后失败消息
        '''
        Component.__init__(self, owner)
        self.fightmsg = []
        self.systemToInfo=[]
        self.fightTmsg = []
        self.chatzh=[]
        self.publicmsg = []
        self.pecifiedmsg = []
        self.specialmsg = set()
        self.fightfailmsg = []
        
    def putFightfailmsg(self,args):
        '''推送战后失败提示框'''
        self.fightfailmsg.append(args)
        
    def putFightMsg(self,msg):
        '''加入战斗消息
        @param msg: str 消息内容
        '''
        msg += '\n'
        self.fightmsg.append(msg)
        
    def popFightMsg(self):
        '''取出所有的战斗消息,并清空'''
        msg = ''
        msg = msg.join(self.fightmsg)
        self.fightmsg = []
        return msg
    
    def putFightTMsg(self,msg):
        '''加入战斗3秒消息
        @param msg: str 消息内容
        '''
        self.fightTmsg.append(msg)
        
    def popFightTMsg(self):
        '''取出所有的战斗3秒消息,并清空'''
        msg = self.fightTmsg
        self.fightTmsg = []
        return msg
    
    def putPublicMsg(self,msg):
        '''加入战斗消息
        @param msg: str 消息内容
        '''
        msg += "\n"
        self.publicmsg.append(msg)
        
    def popPublicMsg(self):
        '''取出所有的战斗消息,并清空'''
        msg = ''
        msg = msg.join([ms.join('\n') for ms in self.publicmsg])
        self.publicmsg = []
        return msg
        
    def putPecifiedMsg(self,msg):
        '''加入战斗消息
        @param msg: str 消息内容
        '''
        self.pecifiedmsg.append(msg)
        
    def popPecifiedMsg(self):
        '''取出所有的战斗消息,并清空'''
        msg = ''
        msg = msg.join([ms.join('\n') for ms in self.pecifiedmsg])
        self.pecifiedmsg = []
        return msg
    
    def putSpecialMsg(self,msgtype):
        '''添加特殊消息处理'''
        self.specialmsg.add(msgtype)
        
    def popSpecialMsg(self):
        '''取出所有的特殊消息'''
        msglist = list(self.specialmsg)
        self.specialmsg.clear()
        return msglist
        
    def pushSpecialMsg(self):
        '''推送特殊消息'''
        msglist = self.popSpecialMsg()
        for m in msglist:
            if m == LEVELUPMESSAGE:
                self._owner.level.pushLevelUpMessage()
            elif m == TASKFILISHED:
                self._owner.quest.pushTaskCanFinished()
    
    def pushFightFailMsg(self):
        '''推送战后失败消息'''
        msglist = self.fightfailmsg
        try:
            for msg in msglist:
                if len(msg)==5:
                    recCharacterId,sysOpeType,tishiStr,contentStr,caozuoStr = msg
                    pushCorpsApplication(recCharacterId,sysOpeType,tishiStr,contentStr,caozuoStr)
                else:
                    recCharacterId,sysOpeType,tishiStr,contentStr,caozuoStr,kw = msg
                    pushCorpsApplication(recCharacterId,sysOpeType,tishiStr,contentStr,caozuoStr,
                                         roleId = kw.get('roleId',0),roleName = kw.get('roleName',u''),
                                         icon = kw.get('icon',0,),type = kw.get('type',0),
                                         pos = kw.get('pos',0),curPage = kw.get('curPage',0),
                                         toposition = kw.get('toposition',0))
        finally:
            self.fightfailmsg = []
    
    def pushFightMsg(self):
        '''推送战后信息'''
        msg = self.popFightMsg()
        pushPromptedMessageByCharacter(msg, [self._owner.baseInfo.id])
    
    def pushFightTMsg(self):
        '''推送战后3秒信息'''
        msglist = self.popFightTMsg()
        for msg in msglist:
            pushOtherMessageByCharacterId(msg, [self._owner.baseInfo.id])
    
    
    ###########################系统公告###########################################
    def putSystem(self,msg):
        '''添加系统公告信息'''
        self.systemToInfo.append(msg)
    
    def popsystemToInfo(self):
        '''取出所有系统公告信息，并清空'''
        msg=self.systemToInfo
        self.systemToInfo=[]
        return msg
    
    def pushSystem(self):
        '''推送系统公告'''
        from app.scense.serverconfig.chatnode import chatnoderemote
        msg=self.popsystemToInfo()
        if len(msg)>0:
            for item in msg:
#                chat.pushSystemToInfo(item)
                chatnoderemote.callRemote('pushSystemToInfo',item)

    ############################聊天框综合通告############################################
    def putchatzh(self,msg):
        '''添加聊天框综合信息'''
        self.chatzh.append(msg)
    
    def popchatzh(self):
        '''取出所有聊天框综合信息，并清空'''
        msg=self.chatzh
        self.chatzh=[]
        return msg
    
#    def pushchatzh(self):
#        '''推送聊天框综合信息'''
#        from applyInterface import chat
#        msg=self.popchatzh()
#        if len(msg)>0:
#            for item in msg:
#                chat.aaa(item)

    
    
    
    def AfterFightMsgHandle(self):
        '''战后消息处理'''
        self.pushFightMsg()
        self.pushFightTMsg()
        self.pushSpecialMsg()
        self.pushFightFailMsg()
        self.pushSystem()
#        self.pushchatzh()
        
        
        
        
    
        