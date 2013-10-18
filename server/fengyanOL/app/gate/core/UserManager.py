#coding:utf8
'''
Created on 2011-3-24

@author: sean_lan
'''
from firefly.utils.singleton import Singleton

class UsersManager:

    __metaclass__ = Singleton

    def __init__(self):
        self._users = {}
        self._users_dy = {}
        
    def addUser(self, user):
        """添加一个用户
        """
        if self._users.has_key(user.id):
            self._users[user.id].disconnectClient()
            self.dropUserByID(user.id)
        self._users[user.id] = user
        self._users_dy[user.dynamicId] = user

    def getUserByID(self, id):
        """根据ID获取用户信息
        """
        try:
            user = self._users[id]
            return user
        except:
            return None
        
    def getUserByDynamicId(self,dynamicId):
        '''根据客户端的动态ID获取user实例'''
        return self._users_dy.get(dynamicId)

    def getUserByUsername(self, username):
        """根据用户名获取用户信息
        """
        for k in self._users.values():
            if k.getNickName() == username:
                return k
        return None

    def dropUser(self, user):
        """处理用户下线
        """
        userId = user.id
        dynamicId = user.dynamicId
        try:
            del self._users[userId]
            del self._users_dy[dynamicId]
        except Exception,e:
            print e
            
    def dropUserByDynamicId(self, dynamicId):
        user = self.getUserByDynamicId(dynamicId)
        if user:
            self.dropUser(user)

    def dropUserByID(self, userId):
        """根据用户ID处理用户下线
        """
        user = self.getUserByID(userId)
        if user:
            self.dropUser(user)
