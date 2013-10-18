#coding:utf8
'''
Created on 2012-3-31

@author: Administrator
'''
from firefly.utils.singleton import Singleton

class ChatRoomManager:
    ''''''
    __metaclass__ = Singleton

    def __init__(self):
        '''init'''
        self.rooms = {}
        
    def joinRoom(self,clientId,roomId):
        '''
        @param clientId: int client id
        @param roomId: int room id
        '''
        room = self.rooms.get(roomId)
        if room is None:
            self.rooms[roomId] = set()
        self.rooms[roomId].add(clientId)
            
    def leaveRoom(self,clientId,roomId):
        '''
        @param clientId: int client id
        @param roomId: int room id
        '''
        room = self.rooms.get(roomId)
        if room is None:
            return
        room.remove(clientId)
        if roomId<5000 and not room:
            del self.rooms[roomId]
            
    def getRoomMember(self,roomId):
        '''
        @param roomId: int room d
        '''
        targetList = self.rooms.get(roomId)
        if not targetList:
            return []
        return targetList
            
        