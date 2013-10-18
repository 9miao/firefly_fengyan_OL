#coding:utf8
'''
Created on 2011-4-18

@author: sean_lan
'''

from app.scense.utils.dbopera import dbSkill

class Skill:
    '''技能类
    @param _groupId: int 技能所属组的id
    @param _level: int 技能的等级
    '''
    def __init__(self,id):
        '''技能类初始化
        @param id: int 技能的ID
        '''
        self.id = id
        self.name = ''
        self.format = {}
        
    def initSkill(self):
        '''初始化技能的相关信息
        '''
        self.format = dbSkill.ALL_SKILL_INFO[self.id]
        self.name = self.format['skillName']
        
    def formatSkillInfo(self):
        '''格式化技能信息'''
        self.format = dbSkill.ALL_SKILL_INFO[self.id]
        
#    def doSkill(self):
#        '''技能执行'''
        
        
        
        
        
    
    