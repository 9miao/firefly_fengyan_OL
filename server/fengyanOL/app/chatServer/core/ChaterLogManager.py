#coding:utf8
'''
Created on 2011-11-16

@author: SIOP_09
'''
from app.chatServer.core.chat.ChatLog import ChatLog
from firefly.utils.singleton import Singleton
from app.chatServer.net import pushObjectNetInterface
from app.chatServer.core.language.Language import Lg

class ChaterLogManager:
    '''聊天整合管理类'''

    __metaclass__ = Singleton
    
    def __init__(self):
        
        self.list={} #聊天记录

    def addChatLog(self,id):
        '''获取(添加)聊天类,返回聊天类实例
        @param id: int 聊天角色id
        '''
        if not self.list.has_key(str(id)):
            self.list[str(id)]=ChatLog(id)
        return self.list[str(id)]
    
    def delChatLog(self,id):
        '''删除聊天类
        @param id: int 当前下线角色id
        '''
        if not self.list.has_key(str(id)):
            #print "此角色私聊已经删除,或者此角色而没有私聊过"
            return
        clog=self.addChatLog(id) #当前聊天实例
        
#        dbFriendTop.updateFriendTop(id, clog.getFriends(), clog.getReaderList()) #更新随进联系人列表、未读信息到数据库中
        #删除数据库中角色所有发送聊天信息
        #聊天内容加入数据库中
        del self.list[str(id)]

    def getFriendReaderState(self,id,tid):
        '''查询聊天信息是否已读取
        @param id: int 当前角色id
        @param tid: int 私聊对象id
        '''
        
        clog=self.addChatLog(id) #获取或添加私聊类
        list=clog.getReaderList() #获取微动信息角色列表
        if len(list)>0:
            if tid in list:
                return False
        return True
            
#--------------------------------------------------------------------------------------
    def addLog(self,id,tid,context,time):
        '''添加聊天记录
        @param id: int  当前角色id
        @param tid: int 接受聊天信息对象id
        @param contxt: int 聊天内容
        '''
        from app.chatServer.core.ChaterManager import ChaterManager
        chater=ChaterManager().getChaterByCharacterId(tid) #聊天接收者
        dyid=ChaterManager().getChaterByCharacterId(id).dynamicId

        ftypeid=chater.isf(id)#1好友  2黑名单  0没有关系
        if ftypeid==2:
            pushObjectNetInterface.pushOtherMessage(905, Lg().g(643), [dyid])
            return
        
        clog=self.addChatLog(id) #获取或添加私聊类
        clog.addFriends(tid) #当前角色添加私聊好友
        clog.addChat(tid,context,time) #添加聊天记录
        
        clog1=self.addChatLog(tid) #获取或添加私聊类(聊天接受者聊天类)
        clog1.addReaderList(id) #设置聊天接受者有未读信息
        clog1.addFriends(id) #聊天接受者角色添加私聊好友
        cter=ChaterManager().getChaterByCharacterId(tid) #聊天接收者
        
        sid=clog.getReading()#获取正在聊天角色id
        if sid==tid : #当前角色正在跟聊天接受者私聊中（并且私聊面板开启中）
            ct=self.getLogonly(id, tid)
            pushObjectNetInterface.pushChatToObjectList(id, tid) #推送给聊天发送者，聊天成员列表
            if cter.island:#如果聊天接收者在线
                pushObjectNetInterface.pushChatToObjectList(tid, id) #推送给聊天发接收者，聊天成员列表
            pushObjectNetInterface.pushServerSendChatInfo(id, ct,tid) #推送聊天信息
            if clog1.getReading()==id: #如果对方也正在跟我聊天
                pushObjectNetInterface.pushServerSendChatInfo(tid, ct,id) #推送聊天信息
                clog1.delReaderList(id)
#            else:
#                pushObjectNetInterface.pushChatToObjectList(tid, id) #推送给聊天接受者，聊天成员列表
        else: # 当前角色正在跟其他角色饲料中(或者私聊面板关闭)
            pushObjectNetInterface.pushChatToObjectList(id, tid) #推送给聊天发送者，聊天成员列表
            if not cter.island: #如果对方已经下线
                return
            pushObjectNetInterface.pushChatToObjectList(tid, id) #推送给聊天接受者，聊天成员列表
#            pushObjectNetInterface.pushServerSendChatInfo(id, context)
            
        clog.setReading(tid) #设置当前角色正在和tid聊天
        
        
            
    def getLog(self,id,tid):
        '''获取聊天记录
        @param id: int 当前角色id
        @param tid: int 私聊对象id
        '''
        from app.chatServer.core.ChaterManager import ChaterManager
        clog=self.addChatLog(id) #获取或添加私聊类
        result=clog.getChat(tid) #获取私聊信息
        clog.delReaderList(tid)#在未读信息列表中删除此角色id相应数据
        clog.addFriends(tid) #添加私聊最近联系人
        clog.setReading(tid) #设置当前跟谁聊天
        
        
        data={}
        players=ChaterManager().getChaterByCharacterId(tid)
        data['name']=players.charactername
        data['level']=str(players.level)
        data['perfession']=players.getProfessionName()
            
        if not players.island:#如果角色不在线
            data['chatObjectPos']=Lg().g(106)
        else:
            data['chatObjectPos']=players.scenename
        data['result']=result
        return data
    
    def getLogonly(self,id,tid):
        '''仅单纯获取聊天数据，没有逻辑处理
        @param id: int 当前角色id
        @param tid: int 私聊对象id'''
        clog=self.addChatLog(id) #获取或添加私聊类
        result=clog.getChat(tid) #获取私聊信息
        if not result:
            return ""
        return result
        
    
    def closeChat(self,id):
        '''关闭私聊窗口
        @param id: int 当前角色id
        '''
        clog=self.addChatLog(id) #获取私聊类
        clog.setReading(0) #设置当前角色没有跟任何人在聊天 (关闭私聊窗口))