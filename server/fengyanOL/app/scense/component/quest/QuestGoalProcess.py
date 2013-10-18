#coding:utf8
'''
Created on 2011-7-26
任务进度
@author: lan
'''
class QuestGoalProcess(object):
    '''任务的进度'''
    def __init__(self,goalID):
        '''初始化任务的进度'''
        self.goalType = 1
        self.goalID = 0
        self.questRecordId = 0
        self.talkCount = 0
        self.killCount = 0
        self.useCount = 0
        self.collectCount = 0
        self.qualityLevel = 0
        