#coding:utf8
'''
Created on 2011-11-29
私聊类
@author: SIOP_09
'''
from app.scense.utils.dbopera import dbFriendTop 
from app.scense.core.chat.ChatContextManager import ChatContextManager
class ChatLog():

    def __init__(self,id):
        '''
        @param id: int 当前聊天角色id
        '''
        self.playercount=15 #私聊角色数量上限
        cf= dbFriendTop.getReader(id)
        self.id=id #当前角色id
        self.friendList=[]
        self.readerList=[]
        if cf:
            self.friendList=eval(cf['friendsid']) #好友角色id列表
            self.readerList=eval(cf['reader']) #未读信息所属角色id列表
        self.reading=0 #正在和哪个角色id聊天
        
    def addChat(self,tid,context,time):
        '''添加发送聊天记录
        @param tid: int 向这个角色id的人发送
        @param context: str 发送的信息
        @param time: str 发送的时间
        '''
        ChatContextManager().addContext(self.id, tid, context, time)
        
    def getChat(self,tid):
        '''获取聊天记录
        @param tid: int 私聊信息接收者id
        '''
        return ChatContextManager().getContext(self.id, tid)
    
    def addFriends(self,id):
        '''添加私聊最近联系人
        @param id: int 最近联系人id
        '''
        if not id in self.friendList:#此角色不在好友列表中
            self.friendList.append(id)
            if len(self.friendList)>self.playercount:#最近联系人数量大于联系人数量上限
                zxList,xxList=self.zxListxxList()
                if len(xxList)<1:#如果都在线的话
                    del self.friendList[0] #删除第一个在线角色
                else:
                    self.friendList.remove(xxList[0]) #删除不在线中的第一角色
                
    def getFriends(self):
        '''获取私聊最近联系人'''
        return self.friendList
        
    def zxListxxList(self):
        '''获取最近联系人中在线列表和不在线列表'''
        from app.scense.core.PlayersManager import PlayersManager
        zxList=[] #在线最近联系人列表
        xxList=[] #下线最近联系人列表
        for id in self.friendList:
            if PlayersManager().getPlayerByID(id):#如果在线
                zxList.append(id)
            else:
                xxList.append(id)
        self.friendList=zxList.extend(xxList)
        return zxList,xxList
        
    def setReading(self,id):
        '''设置正在跟谁聊天
        @param id: int 角色id
        '''
        self.reading=id
        
    def getReading(self):
        '''获取正在跟谁聊天'''
        return self.reading
    
    def getReaderList(self):
        '''获取未读信息角色id列表'''
        return self.readerList
    
    def addReaderList(self,id):
        '''设置未读信息
        @param id: int 未读信息de角色id
        '''
        from app.scense.netInterface import pushObjectNetInterface
        if not id in self.readerList:
            self.readerList.append(id)
            pushObjectNetInterface.pushChatToObjectList(self.id, id)
    def delReaderList(self,id):
        '''删除未读信息
        @param id: int 未读信息的角色id
        '''
        from app.scense.netInterface import pushObjectNetInterface
        if id in self.readerList: #如果未读信息中有此角色id
            self.readerList.remove(id)
            pushObjectNetInterface.pushChatToObjectList(self.id, id)