#coding:utf8
'''
Created on 2011-3-24

@author: sean_lan
'''
from app.scense.core.singleton import Singleton

class UsersManager:

    __metaclass__ = Singleton

    def __init__(self):
        self._users = {}
        
    def addUser(self, user):
        """
        添加一个用户
        """
        if self._users.has_key(user.baseInfo.id):
            raise Exception("系统记录冲突")
        self._users[user.baseInfo.id] = user

    def getUserByID(self, id):
        """
        根据ID获取用户信息
        """
        try:
            user = self._users[id]
            return user
        except:
            return None
        
    def getUserByDynamicId(self,DynamicId):
        try:
            for user in self._users:
                if user.dynamicId == DynamicId:
                    return user
            return None
        except:
            return None

    def getUserByUsername(self, username):
        """
        根据用户名获取用户信息
        """
        for k in self._users.values():
            if k.baseInfo.getNickName() == username:
                return k
        return None

    def dropUser(self, user):
        """处理用户下线
        """
        key = None
        for k, v in self._users.items():
            if user is v:
                key = k
        if key is not None:
            print 'UserManager dropUser'
            self._users[k].dropAllCharacter()
            del self._users[key]
            
    def dropUserByDynamicId(self, dynamicId):
        key = None
        for k, v in self._users.items():
            if v.dynamicId == dynamicId:
                key = k
                break
        if key is not None:
            print 'UserManager类       dropUserByDynamicId()方法  删除用户%d'%key
            self._users[key].dropAllCharacter()
            del self._users[key]

    def dropUserByID(self, id):
        """
        根据用户ID处理用户下线
        """
        try:
            ##print 'UserManager类       dropUserByID()方法  删除用户'
            self._users[id].dropAllCharacter()
            del self._users[id]
        except:
            pass
        