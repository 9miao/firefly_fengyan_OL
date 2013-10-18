#coding:utf8
'''
Created on 2011-4-16

@author: sean_lan
'''
from app.scense.component.baseInfo.BaseInfoComponent import BaseInfoComponent
from app.scense.utils.DataLoader import loader

class SkillBaseInfoComponet(BaseInfoComponent):
    '''技能基础信息组件'''
    
    def __init__(self,owner,id,name,templateId):
        '''
        @param id: int 技能的id
        @param name: str 技能的名称
        @param templateId: int 技能的模板id
        '''
        BaseInfoComponent.__init__(self, owner, id, name)
        
    def initSkillBaseInfo(self):
        '''初始化技能基础信息'''
        skillInfo = loader.getById('skill', self.templateId, '*')
        if not skillInfo:
            raise "skill(%d) not found "%self.templateId
        self.setName(skillInfo['name'])
        
    def getSkillBaseInfo(self):
        '''获取技能基础信息'''
        return loader.getById('skill', self.templateId, '*')
        