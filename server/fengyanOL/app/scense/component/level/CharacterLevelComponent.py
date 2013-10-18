#coding:utf8
'''
Created on 2011-3-31

@author: sean_lan
'''
from app.scense.component.Component import Component
from app.scense.netInterface.pushObjectNetInterface import pushCharacterLevelMessage
from app.scense.netInterface.pushPrompted import pushPromptedMessage,pushApplyMessage,pushPromptedMessageByCharacter
from app.scense.utils.dbopera import dbMail,dbVIP
from app.scense.utils import dbaccess
from app.scense.component.mail.Mail import sendMail

from app.scense.protoFile.vip import ChongzhiMessage_3801_pb2
from app.scense.core.language.Language import Lg


def LevelMailPrompt(level,receiverId):
    '''等级邮件提示
    '''
    if dbMail.LEVEL_MAIL.has_key(level):
        mailinfo = dbMail.LEVEL_MAIL.get(level)
        title = mailinfo.get('title')
        senderId = -1
        sender = Lg().g(128)
        content = mailinfo.get('content')
        mtype = 1
        sendMail(title,senderId,sender,receiverId,content,mtype)
        
def pushChongzhiMessage(sendlist):
    '''推送充值消息
    '''
    reponse = ChongzhiMessage_3801_pb2.ChongzhiMessage()
    msg = reponse.SerializeToString()
    pushApplyMessage(3801,msg,sendlist)
    

class CharacterLevelComponent(Component):
    '''玩家等级组件类
    '''
    MAXLEVEL = 100  #满级限制
    MAXVIP = 10  #最大VIP等级
    def __init__(self,owner,level = 1,exp = 0):
        '''
        @param owner:  Character Object 组件拥有者
        @param level: int 角色的等级
        @param exp:  int 角色的当前经验
        '''
        Component.__init__(self, owner)
        self._level = level
        self._exp = exp
        self._vipexp = 0
        
    def getVipMaxExp(self):
        '''获取当前vip升级所需的最大经验
        '''
        return dbVIP.VIPEXP.get(self._owner.baseInfo._viptype)
        
    def setVipExp(self,exp):
        '''初始化VIP经验
        '''
        self._vipexp = exp
        
    def getVipExp(self):
        '''获取VIP经验
        '''
        return self._vipexp
    
    def addVipExp(self,exp):
        '''加经验'''
        self.updateVIPExp(exp+self.getVipExp())
        pushChongzhiMessage([self._owner.dynamicId])
    
    def updateVIPExp(self,exp):
        '''添加VIP经验
        '''
        if exp ==self._vipexp:
            return
        status = 0
        if self._owner.baseInfo._viptype>=self.MAXVIP:#判断是否超过最大VIP等级
            return
        self._vipexp = exp
        while self._vipexp >= self.getVipMaxExp():
            self._vipexp -= self.getVipMaxExp()
            self._owner.baseInfo._viptype += 1
            status = 1
            if self._owner.baseInfo._viptype>=self.MAXVIP:
                break
        if status:
            self._owner.baseInfo.updateType(self._owner.baseInfo._viptype)
        self._owner.pushInfoChanged()
        dbaccess.updateCharacter(self._owner.baseInfo.id, 'vipexp', self._vipexp)
        
    def getMaxExp(self):
        '''计算当前级别的最大经验值'''
        expinfo = dbaccess.tb_Experience_config.get(self._level,{})
        maxExp = expinfo.get('ExpRequired',0)#400 + 60 * (self._level - 1) + 10 * self._level * (self._level + 1) * (self._level - 1)
        return maxExp
    
    def getExp(self):
        '''获取角色当前经验
        '''
        return self._exp
    
    def setExp(self,exp):
        '''设置角色当前经验值
        @param exp: int 经验值
        '''
        self._exp = exp
        
    def updateExp(self,exp,state=1,update = 1):
        '''更新角色经验值
        @param exp: int 经验值
        @param status: int 表示是否及时推送升级消息
        '''
        if exp ==self._exp:
            return
        status = 0
        if self._level>=self.MAXLEVEL:
            return
        msg = Lg().g(356)%(exp-self._exp)
        self._exp = exp
        while self._exp >= self.getMaxExp():
            self._exp -= self.getMaxExp()
            self._level += 1
            LevelMailPrompt(self._level,self._owner.baseInfo.getId())
            status = 1
        sendList = [self._owner.baseInfo.id]
        if state:
            pushPromptedMessageByCharacter(msg,sendList)
            if status:
                self.updateLevel(self._level)
                self._owner.attribute.updateHp(self._owner.attribute.getMaxHp())
                name = self._owner.baseInfo.getNickName()
                pushCharacterLevelMessage(sendList,name,self._level)
        else:
            self._owner.msgbox.putFightMsg(msg)
            if status:
                self.updateLevel(self._level)
                self._owner.attribute.updateHp(self._owner.attribute.getMaxHp())
                self._owner.msgbox.putPecifiedMsg(1)
        self._owner.pushInfoChanged(statu = update)
        
    def addExp(self,exp,state = 1,update = 1):
        '''加经验'''
        self.updateExp(exp+self.getExp(),state = state,update = update)
        
    def getLevel(self):
        '''获取角色当前等级
        '''
        return self._level
    
    def setLevel(self,level):
        '''设置角色当前等级
        @param level: int 等级
        '''
        self._level = level
        
    def updateLevel(self,level):
        '''更新角色当前等级
        @param level: int 等级
        '''
        from app.scense.serverconfig.chatnode import chatnoderemote
        self._level = level
        
        self._owner.quest.pushPlayerQuestProcessList()
        self._owner.daily.noticeDaily(1,0,level)#升级通知每日目标
        chatnoderemote.callRemote('updateCharteLevel',self._owner.baseInfo.id,level)#同步聊天角色中的等级
        dbaccess.updateCharacter(self._owner.baseInfo.id, 'level', level)
        
    def pushLevelUpMessage(self):
        '''推送角色升级消息'''
        sendList = [self._owner.baseInfo.id]
        name = self._owner.baseInfo.getNickName()
        level = self._level
        pushCharacterLevelMessage(sendList,name,level)
        
    def getVIPInfo(self):
        '''获取角色的VIP信息
        '''
        info = {}
        info['level'] = self._owner.baseInfo.getType()
        if info['level']<self.MAXVIP:
            info['exp'] = self.getVipExp()
            info['maxexp'] = self.getVipMaxExp()
            info['msg'] = Lg().g(357)%(info['maxexp']-info['exp'],
                                               info['level']+1)
        else:
            info['exp'] = 0
            info['maxexp'] = 0
            info['msg'] = Lg().g(358)
        info['vipinfo'] = dbVIP.VIPINFO
        return {'result':True,'data':info}
        
        
        