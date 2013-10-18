#coding:utf8
'''
Created on 2011-3-23

@author: sean_lan
'''
from app.scense.utils import dbaccess
from app.scense.utils.dbopera import dbCharacter,dbUser
from app.scense.core.PlayersManager import PlayersManager
from app.scense.component.baseInfo.UserBaseInfoComponent import UserBaseInfoComponent
#from socketFactroy.net.connectionManager import ConnectionManager
from app.scense.netInterface.pushObjectNetInterface import pushEnterMessage
from app.scense.component.mail.Mail import Mail
from app.scense.core.language.Language import Lg

class User:
    '''用户类'''
    
    def __init__(self, id,name = u'',dynamicId = -1):
        self.baseInfo = UserBaseInfoComponent(self, id)
        self.dynamicId = dynamicId
        self.characterList =[]
        self.last_character = -1
        self.initUser()
        self.initUserCharacterList()
    
    def initUser(self):
        '''初始化用户类'''
        data = dbaccess.getUserInfo(self.baseInfo.id)
        if not data:
            data = {}
            dbaccess.creatUserCharacter(self.baseInfo.id)
        self.baseInfo.setCharacter_1(data.get('character_1',0))
        self.baseInfo.setCharacter_2(data.get('character_2',0))
        self.baseInfo.setCharacter_3(data.get('character_3',0))
        self.baseInfo.setCharacter_4(data.get('character_4',0))
        self.baseInfo.setCharacter_5(data.get('character_5',0))
        self.baseInfo.setPid(data.get('pid',0))
        self.last_character = data.get('last_character',-1)
        
    def getLastCharacter(self):
        '''获取上一次登录的角色'''
        return self.last_character
        
    def updateLastCharacter(self,characterId):
        '''更新上次登录的角色'''
        self.last_character = characterId
        dbUser.updateUserInfo(self.baseInfo.id, {'last_character':characterId})
    
    def getDynamicId(self):
        '''获取用户动态ID'''
        return self.dynamicId
    
    def getVacancy(self):
        '''查找用户角色空位'''

        if not self.baseInfo.getCharacter_1():
            return 'character_1'
        elif not self.baseInfo.getCharacter_2():
            return 'character_2'
        elif not self.baseInfo.getCharacter_3():
            return 'character_3'
        elif not self.baseInfo.getCharacter_4():
            return 'character_4'
        elif not self.baseInfo.getCharacter_5():
            return 'character_5'
        else:
            return None
    
    def getCharacterFieldName(self,id):
        '''根据id 查找该角色所在用户角色关系中的字段名'''
        if id == self.baseInfo.getCharacter_1():
            return 'character_1'
        elif id == self.baseInfo.getCharacter_2():
            return 'character_2'
        elif id== self.baseInfo.getCharacter_3():
            return 'character_3'
        elif id == self.baseInfo.getCharacter_4():
            return 'character_4'
        elif id == self.baseInfo.getCharacter_5():
            return 'character_5'
        else:
            return None
        
    def initUserCharacterList(self):
        '''获取用户角色列表'''
        list=[]
        if self.baseInfo.getCharacter_1():
            list.append(self.baseInfo.getCharacter_1())
        if self.baseInfo.getCharacter_2():
            list.append(self.baseInfo.getCharacter_2())
        if self.baseInfo.getCharacter_3():
            list.append(self.baseInfo.getCharacter_3())
        if self.baseInfo.getCharacter_4():
            list.append(self.baseInfo.getCharacter_4())
        if self.baseInfo.getCharacter_5():
            list.append(self.baseInfo.getCharacter_5())
        self.characterList = list
        
    def getUserCharacterListInfo(self):
        '''获取用户角色列表信息'''
        CharacterListInfo = []
        for id in self.characterList:
            info = dbaccess.getUserCharacterInfo(id)
            if not info:
                continue
            CharacterListInfo.append(info)
        return CharacterListInfo
    
    def creatNewCharacter(self ,nickname ,profession):
        '''创建新角色
        @profession （int） 角色职业 （0 新手 1战士 2 法师 3 游侠 4 牧师）
        '''
        if profession not in range(1,5):
            return {'result':False,'message':Lg().g(589)}
        if len(nickname)<2 or len(nickname)>20:
            return {'result':False,'message':Lg().g(590)}
        for word in dbaccess.All_ShieldWord:
            if nickname.find(word[0])!=-1:
                return {'result':False,'message':Lg().g(21)}
        fieldname = self.getVacancy()
        if not fieldname:
            return {'result':False,'message':Lg().g(591)}
        result = dbaccess.getCharacterIdByNickName(nickname)
        if result:
            return {'result':False,'message':Lg().g(592)}
        result = dbaccess.creatNewCharacter(nickname, profession, self.baseInfo.id, fieldname)
        if result:
            setattr(self.baseInfo, fieldname, result)
            data = {}
            data['UserCharacterListInfo'] = self.getUserCharacterListInfo()
            data['newCharacterId'] = result
            content = Lg().g(593)
            title = Lg().g(594)
            m = Mail( title=title,type =0, senderId =-1, receiverId=result,\
                            sender = Lg().g(128),content=content)
            m.mailIntoDB()
            return {'result':True,'message':Lg().g(595),'data':data}
        else:
            return {'result':False,'message':Lg().g(596)}
        
    def deleteCharacter(self,id):
        fieldname = self.getCharacterFieldName(id)
        if not fieldname:
            return {'result':False,'message':Lg().g(597)}
        if dbCharacter.isPresident(id):
            return {'result':False,'message':Lg().g(598)}
        result = dbaccess.deleteUserCharacter(self.baseInfo.id, fieldname, id)
        if result:
#            for info in self.CharacterListInfo:
            self.initUser()
            data = {}
            data['UserCharacterListInfo'] = self.getUserCharacterListInfo()
            return {'result':True,'message':Lg().g(599),'data':data}
        return {'result':False,'message':Lg().g(600)}
    
    def dropAllCharacter(self):
        '''退出已经登陆的角色'''
        for playerID in self.characterList:
            PlayersManager().dropPlayerByID(playerID)
    
    def disconnectClient(self):
        '''断开'''
        msg = u"您账户其他地方登录"
        pushEnterMessage(msg, [self.dynamicId])
    
#    def __del__(self):
#        '''用户下线,用户的所有角色下线
#        '''
##        self.disconnectClient()
#        self.dropAllCharacter()
#        #print 'User __del__ 用户下线,用户的所有角色下线'
            