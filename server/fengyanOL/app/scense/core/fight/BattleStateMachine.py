#coding:utf8
'''
Created on 2011-9-5
战斗状态机
@author: lan
'''
from app.scense.core.fight.StateBuffer import StateBuffer
from app.scense.utils.dbopera import dbSkill

all_skillInfo = dbSkill.ALL_SKILL_INFO

class BattleStateMachine(object):
    '''战斗状态机'''
    MAXBUFNUM = 5#每个角色最多的buf个数
    StatePool = {}#状态池，保存战斗角色的buff状态
    
    def __init__(self,owner = None):
        '''战斗状态机
        @param fight: Fight object 战斗实例
        '''
        self.owner = owner
        
    def putBuff(self,target,buffId):
        '''给指定的目标添加一个buff
        @param target: int 目标的id
        @param buffId: int buff的ID
        '''
        buff = StateBuffer(buffId)
        if not self.StatePool.has_key(target):
            self.StatePool[target] = []
        self.replaceBuff(target, buff)
        self.seizeBuffSpace(target, buff)
        actor = self.owner.fighters[target]
        #print "【%s】获得BUF[%s]"%(actor['chaName'],buff.getName())
        self.StatePool[target].append(buff)
        actor = self.owner.fighters[target]
        exec(buff.getEffectFormula())
        #print "【%s】BUF[%s]效果触发"%(self.owner.fighters[target]['chaName'],buff.getName())
        
        
            
            
    def replaceBuff(self,target,buf):
        '''替换buff
        @param target: int 目标的id
        @param buf: buff object buff实例
        '''
        canReplaceBuffList  = buf.getCanReplaceBuffList()
        for buff in self.StatePool[target]:
            if buff.getID() in canReplaceBuffList:
                self.clearBuffById(target, buff.getID())
        
    def seizeBuffSpace(self,target,buf):
        '''抢占buff位置
        @param target: int 目标的id
        @param buf: buff object
        '''
        actor = self.owner.fighters[target]
        if len(self.StatePool[target])>=self.MAXBUFNUM:
            buffID = self.StatePool[target][-1].getID()
            self.clearBuffById(target, buffID)
            self.StatePool[target].append(buf)
            
#    def addBuffById(self,target,buf):
#        '''添加一个buff'''
        
    def clearBuffById(self,target,buffID):
        '''根据buff的ID清除buff
        '''
        if not self.StatePool.has_key(target):
            return
        actor = self.owner.fighters[target]
        for buff in self.StatePool[target]:
            if buff.getID()==buffID:
                self.StatePool[target].remove(buff)
                exec(buff.getEffectFormula())
                #print "【%s】BUF[%s]被清除"%(self.owner.fighters[target]['chaName'],buff.getName())
        
    def clearBuffByType(self,target,buffType):
        '''根据buff的ID清除buff
        '''
        for buff in self.StatePool[target]:
            if buff.getBuffType()==buffType:
                self.clearBuffById(target, buff.getID())
                
    def getTargetBuffList(self,target):
        '''获取目标的bufflist
        @param target: int 目标的id
        '''
        buffList = []
        if self.StatePool.has_key(target):
            buffList = [buff.getID() for buff in self.StatePool[target]]
        return buffList
    
    def getTargetBuffInfoList(self,target):
        '''获取目标的的buff信息列表'''
        buffList = []
        if self.StatePool.has_key(target):
            buffList = [{'buffId':buff.getID(),'buffLayerCount':buff.getStack(),\
                         'buffRemainRoundCount':buff.getTraceCD()}\
                         for buff in self.StatePool[target]]
        return buffList
    
    def executeBuffEffects(self,target):
        '''处理角色身上所有的buff效果'''
        if not self.StatePool.has_key(target):
            return
        for buff in self.StatePool[target]:
            self.OneBuffCDProcess(target, buff.getID())
            self.executeBuffEffect(target, buff)
                
    def executeBuffEffect(self,target,buff):
        '''进行buff效果(计算buff伤害)
        @param target: int 目标的id
        @param buffId: int buff的ID
        '''
        dotHotFormula = buff.getDotHotFormula()
        if not dotHotFormula:
            return
        data = {}
        data['chaId'] = -1#角色的Id
        data['chaBattleId']= -1#角色战斗ID
        data['chaProfessionType'] = -1
        data['actionId'] = 0#动作ID
        data['counterHitActionId'] = 0
        data['isDeathOfCounterHit'] = 0
        data['txtEffectId'] = 0#文字特效（暴击等闪避）
        
#        data['skillId'] = -1#技能的ID
        data['chaEffectId'] = 0#角色释放技能特效
        data['chaEnemyEffectId'] = 0#角色技能承受特效
        data['chaThrowEffectId'] = 0
        data['chaAoeEffectId'] = 0#角色技能投射特效
        
        data['chaBuffArr'] = []#角色身上的buff
        data['chaBuffShowList'] = []#角色身上buff显示信息
        
        data['chaPowerUp'] = 0#+20 power增加
        data['chaPowerDown'] = 0#-20 power减少
        data['chaCurrentPower'] = 0#当前能量
        data['chaChangeHp'] = 0#±20 正负HP，可能有加血技能
        data['chaCurrentHp'] = 0#角色的当前血量
        data['chaExpendHp'] = 0#角色技能消耗的血量
        data['chaStartPos'] = (0,0)#角色的起始坐标
        data['chaTargetPos'] = (0,0)#角色的目标坐标
        
        data['chaAttackType'] = 2
        data['isCriticalBlow'] = False
        data['enemyChaArr'] = []#所有受攻击者的信息
        
        info = {}
        enemy = self.owner.fighters[target]
        info['enemyChaId'] = enemy['chaId']#受攻击者的角色的id
        info['enemyBattleId'] = target#受攻击者的战场id
        info['enemyActionId'] = enemy['chaProfessionType']*1000+560#受攻击者的动作id
        info['enemyTxtEffectId'] = 0#受攻击者的文字特效
        
#        info['enemySkillId'] = enemy['ordSkill']#受攻击者的技能id(通常反击时为普通攻击)
        info['chaEffectId'] = all_skillInfo[enemy['ordSkill']]['releaseEffect']
        info['chaEnemyEffectId'] = all_skillInfo[enemy['ordSkill']]['bearEffect']
        info['chaThrowEffectId'] = all_skillInfo[enemy['ordSkill']]['throwEffectId']
        info['chaEnemyAoeEffectId'] = all_skillInfo[enemy['ordSkill']]['aoeEffectId']
        
        info['enemyBuffArr'] = []#受攻击者的buff列表
        info['enemyBuffShowList'] = []
        
        info['enemyPowerUp'] = 0#受攻击者的能量增量
        info['enemyCurrentPower'] = enemy['chaCurrentPower']#受攻击者的当前能量
        info['enemyChangeHp'] = 0#受攻击者丢失的血量
        info['enemyCurrentHp'] = enemy['chaCurrentHp']#受攻击者的当前血量
        info['enemyCounterHit'] = 0#受攻击者是否反击 0没有 1反击
        info['enemyStartPos'] = enemy['chaPos']#受攻击者的起始坐标
        info['enemyTargetPos'] = enemy['chaPos']#受攻击者的目标坐标
        info['enemyDirection'] = enemy['chaDirection']#玩家朝向右，朝向右。2--玩家朝向左
        #print "【%s】当前血量为%d"%(enemy['chaName'],enemy['chaCurrentHp'])
        
        attributeType = buff.getAttributeType()
        attack = 0
        defense = 0
        damage = 0
        if attributeType == 1:
            defense = enemy['physicalDefense']
        else:
            defense = enemy['magicDefense']
        if not damage:
            defensePercent = defense/(defense+100*(enemy['chaLevel']-8))*1.0
            damage = attack*abs(defensePercent)
        
        try:
            exec(dotHotFormula)
        except Exception as e:
            #print e
            return
        
        
        info['enemyChangeHp'] = damage
        #print "【%s】受[%s]伤害为%d"%(enemy['chaName'],buff.getName(),info['enemyChangeHp'])
        enemy['chaCurrentHp'] += info['enemyChangeHp']
        #print "【%s】受[%s]伤害后的血量为%d"%(enemy['chaName'],buff.getName(),enemy['chaCurrentHp'])
        if enemy['chaCurrentHp']<=0:
            #print "【%s】受[%s]BUF致死"%(enemy['chaName'],buff.getName())
            enemy['died'] = 1
            enemy['died']=1#角色死亡
            info['enemyActionId'] = enemy['chaProfessionType']*1000+580
            self.owner.order.remove(target)
            if enemy['chaDirection']==1:
                self.owner.activeList.remove(target)
            else:
                self.owner.passiveList.remove(target)
        info['enemyBuffArr'] = self.getTargetBuffList(target)
        info['enemyBuffShowList'] = self.getTargetBuffInfoList(target)
        data['enemyChaArr'].append(info)
        
        #资源列表收集使用到的资源
        self.owner.resourceCollect(data)
        self.owner.FightData.append(data)
        
        
    def produceBuffEffect(self,target,actor):
        '''被动产生buff效果
        @param target: int 目标的id
        @param actor: int 行动者的id
        '''
        
    def buffCDProcess(self,target):
        '''buff的CD处理
        @param target: int 目标的id
        '''
        for buff in self.StatePool[target]:
            self.OneBuffCDProcess(target,buff.getID())
                
    def OneBuffCDProcess(self,target,buffID):
        '''buff的CD处理
        @param target: int 目标的id
        @param buffID: buff 的id
        '''
        for buff in self.StatePool[target]:
            if buff.getID() == buffID:
                result = buff.cutTraceCD()
                if not result:
                    self.clearBuffById(target, buff.getID())
    
    
                

        
