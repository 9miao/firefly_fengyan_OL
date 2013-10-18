#coding:utf8
'''
Created on 2012-5-2
角色扫荡
@author: Administrator
'''
from app.scense.component.Component import Component
from app.scense.core.fight.battleSide import BattleSide
from app.scense.applyInterface import dropout
import random
from app.scense.core.language.Language import Lg

class CharacterRaidsComponent(Component):
    '''角色扫荡'''
    
    def __init__(self,owner):
        '''初始化
        '''
        Component.__init__(self, owner)
        self.raidsfamId = 0#角色所少
        self.rounds = 0#扫荡的次数
        self.starttime = None#开始时间
        
    def doRaids(self,rounds,raidsfamId):
        '''开始扫荡
        @param rounds: int 扫荡回合数
        @param raidsfamId: int 目标副本
        '''
        if raidsfamId not in self._owner.instance.clearances:
            return {'result':False,'message':Lg().g(455)}
        from app.scense.core.instance.Instance import Instance
        if not rounds:
            rounds = self._owner.attribute.getEnergy()/5
        energyrequired = rounds*5
        if energyrequired > self._owner.attribute.getEnergy() or energyrequired==0:
            msg = Lg().g(456)
            return {'result':False,'message':msg}
#        if self._owner.baseInfo.getStatus()!=1:
#            msg = u"你正处于%s状态"%self._owner.baseInfo.getStatusName()
#            return {'result':False,'message':msg}
#        self._owner.baseInfo.setStatus(3)
        messagebox = []
        monsters = []
        instance = Instance(raidsfamId)
        for scene in instance._Scenes.values():
            for mon in scene._monsters.values():
                monsters.append(mon)
        challengers = BattleSide([self._owner])
        for index in range(rounds):
            self._owner.attribute.addEnergy(-5)#消耗活力
            msg = Lg().g(457)%(index+1)
            messagebox.append(msg)
            for monindex in range(len(monsters)):
                msg = self.doFightBound(challengers,monsters[monindex],monindex)
#                self._owner.quest.killMonster(monsters[monindex].templateId)
                messagebox.append(msg)
            msg = self.doCardBound(instance)
            self._owner.quest.clearance(raidsfamId)
            self._owner.finance.updateAddMorale(2,state=True)
            messagebox.append(msg)
        self._owner.schedule.noticeSchedule(18)#成功后的日程目标通知
        return {'result':True,'message':u'','data':messagebox}
    
    
    def doFightBound(self,challengers,monster,monindex):
        '''执行战斗奖励
        '''
#        ruleInfo = monster.getRule()
        temlist,rule = monster.getRule()
        for temId in temlist:
            self._owner.quest.killMonster(temId)
        msgHead = Lg().g(458)%(monindex+1)
        msgbox = []
        msgbox.append(msgHead)
        monstercnt = len(temlist)
        dropoutid = monster.formatInfo['dropoutid']
        expBonus = monster.formatInfo.get('expbound',100)*monstercnt
        itemsBonus = dropout.getDropByid(dropoutid)
        members = challengers.getMembers()
        for mem in members:
            if mem['characterType']==3:#宠物
                pet = self._owner.pet._pets.get(mem['chaId'])
                pet.level.addExp(expBonus)
                msg = Lg().g(459)%pet.baseInfo.getName()
            if mem['characterType']==1:
                expEff = self._owner.attribute.getExpEff()#经验加成
                plexp = expBonus* expEff
                self._owner.level.addExp(plexp,update = 0)
                msg = Lg().g(459)%self._owner.baseInfo.getNickName()
            msgbox.append(msg)
        msgbox[-1] = msgbox[-1][:-1]

        if itemsBonus:
            self._owner.pack.putNewItemInPackage(itemsBonus)
            itemtemplateid = itemsBonus.baseInfo.itemTemplateId
            itemname = itemsBonus.baseInfo.getRichName()
            stack = itemsBonus.pack.getStack()
            msg =Lg().g(460)+ u"<a href = 'event:%d'><u>%s</u></a> x %d"%(itemtemplateid,itemname,stack)
            msgbox.append(msg)
        msgbox.append(' \n')
        return u''.join(msgbox)
        
    def doCardBound(self,instance):
        '''获取翻牌奖励
        '''
        dropoutid = instance._dropoutid
        dropoutdata=dropout.getByDropOutByid(dropoutid)
        cardbound = random.choice(dropoutdata)
        dropItem = cardbound.get('item')
        coin = cardbound.get('coin',0)
        msgHead = Lg().g(461)
        if coin:
            self._owner.finance.addCoin(coin)
            msg = Lg().g(311)%coin
        elif dropItem:
            itemtemplateid = dropItem.baseInfo.itemTemplateId
            itemname = dropItem.baseInfo.getRichName()
            stack = dropItem.pack.getStack()
            self._owner.pack.putNewItemInPackage(dropItem)
            msg =Lg().g(462)+ u"<a href = 'event:%d'><u>%s</u></a> x %d"%(itemtemplateid,itemname,stack)
        else:
            msg = Lg().g(463)
        return msgHead + msg +' \n'
        
        
        
        
