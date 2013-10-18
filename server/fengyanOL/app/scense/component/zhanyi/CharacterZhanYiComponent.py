#coding:utf8
'''
Created on 2013-1-8
角色的战役信息
@author: lan
'''
from app.scense.component.Component import Component
from app.scense.core.character.Monster import Monster
from app.scense.core.fight.battleSide import BattleSide
from app.scense.utils.dbopera import db_zhanyi
from app.scense.core.zhanyi.zymanage import ZYManage

class CharacterZhanYiComponent(Component):
    '''角色的战役信息
    '''
    
    def __init__(self,owner):
        '''初始化爬塔信息
        '''
        Component.__init__(self, owner)
        self.currentZY = 1000#当前战役的ID
        self.currentZJ = 1000#当前章节的ID
        self.initData()
        
    def initData(self):
        ''''''
        characterId = self._owner.baseInfo.id
        result = db_zhanyi.getCharacterZhangJieInfo(characterId)
        self.currentZY = result.get('zhanyi')
        self.currentZJ = result.get('zhangjie')
        
    def getCurrentZY(self):
        '''获取角色当前战役的信息'''
        return self.currentZY
    
    def getCurrentZJ(self):
        '''获取当前章节的信息'''
        return self.currentZJ
    
    def getZhanYiInfo(self,index):
        '''获取角色的当前战役信息
        '''
        zhanyilist = ZYManage().zhanyiSet.keys()
        zhanyilist.sort()
        if index ==-1:
            zid = self.currentZY
        else:
            zid = zhanyilist[index]
        
        nowindex = zhanyilist.index(zid)
        maxpage = len(zhanyilist)
        zy = ZYManage().getZhanYiInfoById(zid)
        zyinfo = zy.formatInfo(self.currentZY,self.currentZJ)
        info = {'index':nowindex,
                'maxpage':maxpage,
                'zyinfo':zyinfo}
        return info
            
    def doZhangJie(self,zhangjieid):
        '''章节战斗
        @param zhangjieid: int 章节的
        '''
        if zhangjieid>self.currentZJ:
            return {'result':False,'message':u'当前章节未被激活'}
        from app.scense.core.fight.fight_new import Fight
        zhanjieInfo = db_zhanyi.ALL_ZHANGJIE_INFO.get(self.currentZJ)
        levelrequired = zhanjieInfo.get('levelrequired')
        if self._owner.level.getLevel()<levelrequired:
            return {'result':False,'message':u'当前等级不足'}
        ruleInfo = eval(zhanjieInfo.get('mconfig'))
        temlist,rule = ruleInfo[0],ruleInfo[1]
        i = 100
        challengers = BattleSide([self._owner])
        deffen = []
        for tem in temlist:
            i+=1 
            monser = Monster(id = i,templateId = tem)
            deffen.append(monser)
        defenders = BattleSide(deffen,state = 0)
        defenders.setMatrixPositionBatch(rule)
        data = Fight( challengers, defenders, 600)
        data.DoFight()
        if data.battleResult == 1 and zhangjieid==self.currentZJ:#如果战斗胜利
#            self._owner.quest.cleanZhanYi(zhangjieid)#通知战役通关任务
            zhanyilist = ZYManage().zhanyiSet.keys()
            zhanyilist.sort()
            zy = ZYManage().getZhanYiInfoById(self.currentZY)
            zhangjielist = zy.zhangjieSet.keys()
            zhangjielist.sort()
            index = zhangjielist.index(self.currentZJ)
            if index>=len(zhangjielist)-1:
                zhanyiindex = zhanyilist.index(self.currentZY)
                if zhanyiindex<len(zhanyilist)-1:
                    zhanyiindex = zhanyilist.index(self.currentZY)
                    self.currentZY = zhanyilist[zhanyiindex+1]
                    zy = ZYManage().getZhanYiInfoById(self.currentZY)
                    zhangjielist = zy.zhangjieSet.keys()
                    zhangjielist.sort()
                    self.currentZJ = zhangjielist[0]
            else:
                self.currentZJ = zhangjielist[index+1]
        if data.battleResult == 1:
            self._owner.quest.cleanZhanYi(zhangjieid)#通知战役通关任务
        return {'result':True,'data':{'fight':data}}

    def updateCharacterZhangjie(self):
        '''更新角色的章节信息
        '''
        characterId = self._owner.baseInfo.id
        db_zhanyi.updateCharacterZhangjie(characterId,self.currentZJ,self.currentZY)
        
    def checkClean(self,zhangjieid):
        '''检测章节是否通关
        '''
        if self.currentZJ>zhangjieid:
            return True
        return False
        
    
    
    
    
        
        