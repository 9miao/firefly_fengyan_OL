#coding:utf8
'''
Created on 2011-7-25
任务目的类
@author: lan
'''
from utils.dbopera import dbtask
class QuestGoal(object):
    '''任务目的类
    @param templateInfo: dict 任务目标的基本信息 
    '''
    def __init__(self,goalID,IDinDB = 0):
        self.goalID = goalID
        self.IDinDB = IDinDB
        self.templateInfo = {}
        self.goalType = 1
        self.questRecordId = 0
        self.talkCount = 0
        self.killCount = 0
        self.useCount = 0
        self.collectCount = 0
        self.qualityLevel = 0
        
    def initGoalInfo(self):
        '''初始化任务的目标信息'''
        self.templateInfo = dbtask.getQuestGoaltemplateInfoById(self.goalID)
        self.goalType = self.templateInfo['goalType']
        
    def formatGoalInfo(self):
        '''格式化任务目的模板信息'''
        if not self.templateInfo:
            self.initGoalInfo()
        processGoalInfo = {}
        processGoalInfo['questGoalId'] = self.goalID
        processGoalInfo['trackDesc'] = self.templateInfo.get('trackDesc',u'万恶的策划，这里没填信息')
        if self.templateInfo['goalType']==1:#任务是谈话任务时
            processGoalInfo['requireNum'] = self.templateInfo['talkNum']
            processGoalInfo['achieveNum'] = self.talkCount
        elif self.templateInfo['goalType']==2:#任务时杀怪任务时
            processGoalInfo['requireNum'] = self.templateInfo['killNum']
            processGoalInfo['achieveNum'] = self.killCount
        elif self.templateInfo['goalType']==3:#任务时收集任务时
            processGoalInfo['requireNum'] = self.templateInfo['collectNum']
            processGoalInfo['achieveNum'] = self.collectCount
        elif self.templateInfo['goalType']==4:#任务是使用物品类任务时
            processGoalInfo['requireNum'] = self.templateInfo['useNum']
            processGoalInfo['achieveNum'] = self.useCount
        elif self.templateInfo['goalType']==5:#任务是强化装备类任务时
            processGoalInfo['requireNum'] = self.templateInfo['goalQualityLevel']
            processGoalInfo['achieveNum'] = self.qualityLevel
        else:
            processGoalInfo['requireNum'] = self.templateInfo['talkNum']
            processGoalInfo['achieveNum'] = self.talkCount
        return processGoalInfo
        
    def SerializationQuesGoaltInfo(self,bearer):
        '''将自己的所有属性序列号付给Message对象
        @param bearer: Message Object 承载者
        '''
        data = self.formatGoalInfo()
#        filednames = ['questGoalId','requireNum','achieveNum','trackDesc']
#        for f
        for item in data.items():
            setattr(bearer, item[0], item[1])
        return bearer
        
        
        
        