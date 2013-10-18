#coding:utf8
'''
Created on 2012-5-15
角色的神格属性
@author: Administrator
'''
from app.scense.component.Component import Component
from app.scense.utils.dbopera import dbGodhead
from app.scense import util
from twisted.python import log
from app.scense.core.language.Language import Lg

class CharacterGodheadComponent(Component):
    '''神格'''
    
    def __init__(self,owner):
        '''初始化
        @param activated: list[int] 已经激活的神格
        '''
        Component.__init__(self, owner)
        self.activated = []
        self.godheadAttr = None
        self.initGodhead()
        
    def initGodhead(self):
        '''初始化角色神格信息
        '''
        characterId = self._owner.baseInfo.id
        self.activated = dbGodhead.getCharacterAllGodhead(characterId)
        
    def getGodheadInfo(self,headtype):
        '''获取所有的神格信息
        @param headtype: int 神格的类型
        '''
        godheadinfos = {}
        godheadinfos['douqi'] = self._owner.finance.getMorale()#斗气值
        godheadinfos['des'] = dbGodhead.ALL_HEADTYPE[headtype].get('typedes')#神格的描述
        godheadinfos['curPage'] = headtype#当前页数
        godheadinfos['maxPage'] = 7#最大页数
        godheadinfos['shenGeList'] = []#神格列表
        godheadinfos['nextBtnFlag'] = True
        
        for headinfo in dbGodhead.ALL_GODHEAD.values():
            if headinfo['headtype'] != headtype:
                continue
            info = {}
            info['sgID'] = headinfo['id']#神格的ID
            info['sgType'] = headinfo['headtype']#神格的类型
            info['sgName'] = headinfo['name']#神格的名称
            info['sgDes'] = headinfo['desc']#神格的描述
            info['activateFlag'] = info['sgID'] in self.activated
            info['reqDQ'] = headinfo['consumption']
            info['level'] = headinfo['levelrequired']
            godheadinfos['shenGeList'].append(info)
        godheadinfos['shenGeList'].sort(key = lambda d:d['sgID'])
        return {'result':True,'data':godheadinfos}
    
    def ActiveGodhead(self,godheadId):
        '''激活神格
        @param godheadId: int 神格的ID
        '''
        if godheadId in self.activated:
            return {'result':False,'message':Lg().g(330)}
        godheadinfo = dbGodhead.ALL_GODHEAD.get(godheadId)
        if not godheadinfo:
            return {'result':False,'message':Lg().g(331)}
        if godheadinfo.get('levelrequired')>self._owner.level.getLevel():
            return {'result':False,'message':Lg().g(332)}
        before = godheadinfo.get('priorityID')
        consumption = godheadinfo.get('consumption')
        douqi = self._owner.finance.getMorale()
        if before and before not in self.activated:
            return {'result':False,'message':Lg().g(333)}
        if consumption>douqi:
            return {'result':False,'message':Lg().g(334)}
        characterId = self._owner.baseInfo.id
        self._owner.finance.addMorale(-consumption)
        dbGodhead.activeGodhead(characterId, godheadId)
        self.activated.append(godheadId)
        try:
            exec(godheadinfo['triggerEffect'])
        except:
            log.err("godhead trigger errot ID:%d"%godheadId)
        try:
            msg = Lg().g(335)%godheadinfo.get('name')
        except:
            msg = Lg().g(335)%(godheadinfo.get('name').decode('utf8'))
        self._owner.quest.specialTaskHandle(111)#特殊任务处理
        self.updateGodheadAttribute()
        self._owner.daily.noticeDaily(17,0,len(self.activated))
        self._owner.schedule.noticeSchedule(6)#成功后的日程目标通知
        return {'result':True,'message':msg}
        
    def updateGodheadAttribute(self):
        '''更新所有神格的属性加成
        '''
        info = {}
        for godheadId in self.activated:
            godheadinfo = dbGodhead.ALL_GODHEAD.get(godheadId,{})
            godheadattr = eval(godheadinfo.get('attributeEffect','{}'))
            info = util.gs.addDict(info, godheadattr)
        self.godheadAttr = info

    def getGodheadAttribute(self):
        '''获取所有神格的属性加成
        '''
        if self.godheadAttr is None:
            self.updateGodheadAttribute()
        return self.godheadAttr
        
        
        