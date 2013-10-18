#coding:utf8
'''
Created on 2011-7-26
任务代理类
@author: lan
'''
from app.scense.component.quest.Quest import  Quest
class QuestProxy(object):
    '''任务代理类,由于任务的信息量过大，采用代理的模式，节省内存'''
    
    def __init__(self,id,name,tasktype):
        '''代理类初始化
        @param id: int 
        '''
        self.agentsID = id
        self.agentsName = name
        self.agentsType = tasktype
        
    def formatQuestProxy(self):
        '''格式化任务代理信息'''
        data = {}
        data['taskId'] = self.agentsID
        data['taskname'] = self.agentsName