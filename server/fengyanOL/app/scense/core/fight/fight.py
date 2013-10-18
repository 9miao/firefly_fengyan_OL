#coding:utf8
'''
Created on 2011-9-2
战斗类
战场ID分配规则
2位数 第一位 表示战斗阵营 1主动 2被动方
后一位表示阵眼的位置
@author: lan
'''
import random,math
from app.scense.core.fight.BattleStateMachine import BattleStateMachine
from app.scense.utils.dbopera import dbSkill
import copy

all_skillInfo = dbSkill.ALL_SKILL_INFO

class Fight(object):
    '''战斗类'''
    
    WIDTH = 1000    #战场的宽度
    HEIGHT = 570    #战场的高度
    MOVEABLE = 350  #活动区域的起始纵坐标
    DISTANCE_X = 50    #角色在X轴上得距离
    DISTANCE_Y = 50     #角色在Y轴上得距离
    DISTANCE_PHA = 200  #方阵到中心点的间距
    MAX_ROUND = 15  #战斗的最大回合数
    
    def __init__(self,activeSide,passiveSide,center):
        '''初始化战斗类
        @param center: int 碰撞点的坐标
        @param activeSide: 攻击方
        @param passiveSide: 防守方
        '''
        self.ActiveSidePosition = {}    #主动方的方阵坐标
        self.PassiveSidePosition = {}   #被动方的方阵坐标
        self.activeSide = activeSide    #主动方对象
        self.passiveSide = passiveSide  #被动方对象
        self.fighters = {}              #所有战斗成员数据{chaBattleId:fightdata}
        self.center = center            #战斗碰撞点的坐标
        self.activeList = []            #主动方的成员的战场id列表
        self.passiveList = []           #被动方得成员的战场id列表
        self.order = []                 #战斗序列
        self.now_round = 1              #战斗的当前回合数
        self.FightData = []             #战斗产生的数据
        self.initData = []
        self.battleStateMachine = BattleStateMachine(self)#战斗的状态机
        self.initBattlefield()          #划分战场位置
        self.fixBattleSidePosition()    #初始化战场
        self.resources = set()             #战斗中用到的资源列表
        self.battleResult = 1           #战斗结果
        self.initOrder()                #安排出手顺序
        
        
    def initBattlefield(self):
        '''初始化战场，确定战场中的每个位置'''
        
        #print '初始化战场，确定战场中的每个位置...'
        
        if self.center<500:
            self.center=550
        x = 1
        y = 1
        for grid in range(1,10):
            apos = [self.center-self.DISTANCE_X*x-self.DISTANCE_PHA,self.MOVEABLE+y*self.DISTANCE_Y]#生成的主动方坐标
            ppos = [self.center+self.DISTANCE_X*x+self.DISTANCE_PHA,self.MOVEABLE+y*self.DISTANCE_Y]#生成的被动方坐标
            self.ActiveSidePosition[grid] = apos
            self.PassiveSidePosition[grid]= ppos
            y += 1
            if grid%3 ==0:
                x +=1
                y = 1
                
    def fixBattleSidePosition(self):
        '''确定战斗成员的位置,初始化战场,初始化角色技能CD
        '''
        #print '确定战斗成员的位置,初始化战场,初始化角色技能CD...'
        for activeMember in self.activeSide.getMembers():#初始化主动方
            eyeNo = self.activeSide.getCharacterEyeNo(activeMember['chaId'])
            activeMember['chaPos'] = self.ActiveSidePosition[eyeNo]#初始角色的在战场中的位置
            activeMember['chaDirection'] = 1#设置角色的阵营
            activeMember['chaBattleId'] = 10 + eyeNo#分配角色的战场Id
            activeMember['died'] = 0#角色是否死亡
            activeMember['nextReleaseSkill'] = 0#角色下次释放的技能序号
            activeMember['skillIDByAttack '] = 0#角色遭受的攻击的技能id
            activeMember['skillCDRecord'] = [{'skillID':skillID,'traceCD':0} for skillID in activeMember['ActiveSkillList']]
            self.initData.append(copy.deepcopy(activeMember))
            self.fighters[10 + eyeNo] = activeMember
            self.activeList.append(10 + eyeNo)
            
        for passiveMember in self.passiveSide.getMembers():#初始化主动方
            eyeNo = self.passiveSide.getCharacterEyeNo(passiveMember['chaId'])
            passiveMember['chaPos'] = self.PassiveSidePosition[eyeNo]
            passiveMember['chaDirection'] = 2
            passiveMember['chaBattleId'] = 20 + eyeNo
            passiveMember['died'] = 0#角色是否死亡
            passiveMember['nextReleaseSkill'] = 0#角色下次释放的技能序号
            passiveMember['skillIDByAttack '] = 0#角色遭受的攻击的技能id
            passiveMember['skillCDRecord'] = [{'skillID':skillID,'traceCD':0}\
                                              for skillID in passiveMember['ActiveSkillList']]#角色是否技能的CD记录
            self.initData.append(copy.deepcopy(passiveMember))
            self.fighters[20 + eyeNo] = passiveMember
            self.passiveList.append(20 + eyeNo)
            
#        #print '请战斗成员们有点素质，站好自己的位置，那边的，说你呢，还动...'
            
    def initOrder(self):
        '''初始化战斗次序'''
        #print '开始初始化战斗次序...'
        self.order = sorted(self.fighters.keys(),key = lambda d:self.fighters[d]['speed'])
        #print '战斗行动者的顺序为：'
        #print ''.join(["【%s】"%self.fighters[targetID]['chaName'] for targetID in self.order])
        #print '请让规则出招'
        
    def findTarget(self,actorId,targetType=2,rule = 1):
        '''寻找目标
        @param actorId: int 行动者的ID
        @param targetType: int 目标的类型  1己方 2敌方
        @param rule: int 查找规则 1单体 2全体
        '''
        #print '行动者 【%s】开始寻找目标，不知会瞄上谁...'%self.fighters[actorId]['chaName']
        enemyList = []#敌方
        ownList = []#友方
        targetList = []#技能作用目标
        
        actorId_EyeNo = actorId%10      #根据行动者的id得到行动者所在阵法的位置
        actorId_Camp = actorId/10       #根据行动者的id得到行动者所在战场的阵营
        actorId_line = 0                #行动者所在阵法的行号
        if actorId_Camp ==1:
            enemyList = self.passiveList
            ownList = self.activeList
        else:
            enemyList = self.activeList
            ownList = self.passiveList
            
        if targetType == 1:#当目标位己方时
            if rule == 1:#目标为单体时
                targetList.append(actorId)
                #==================================================
                #print '行动者 【%s】连自己也不放过,禽兽行径啊...'%self.fighters[actorId]['chaName']
                #==================================================
            elif rule ==2:#目标为全体时
                targetList = ownList
                #==================================================
                #print '行动者 【%s】要对自己的队员下手了...'%self.fighters[actorId]['chaName']
                #print '被点名的几位兄弟小心了...'
                #print '他们是:'
                #print ''.join(["【%s】"%self.fighters[targetID]['chaName'] for targetID in targetList])
            #print '不要担心,让他的**来滋润你吧...'
            #==================================================
            return targetList
        
        lines = [[1,4,7],[2,5,8],[3,6,9]]#所有的行数
        ruleDict = {1:[1,2,3],2:[2,1,3],3:[3,2,1]}#不同行列的寻找对手规则
        for line in lines:
            if actorId_EyeNo in line:
                actorId_line = lines.index(line)+1
                break
        dd = ruleDict.get(actorId_line)
        sequence = lines[dd[0]-1]+lines[dd[1]-1]+lines[dd[2]-1]
        enemyList.sort(key= lambda d: sequence.index(d%10))
        
        if not enemyList:
            return []
        if rule == 1:#单体时为当前目标
            targetList = [enemyList[0]]
            #==================================================
            #print '行动者 【%s】要对【%s】下手了...'%(self.fighters[actorId]['chaName'],self.fighters[enemyList[0]]['chaName'])
            #print '等待菊花的绽放吧！！'
            #==================================================
            
        elif rule == 2:#全体时为全部敌方目标
            targetList = enemyList
            
        return targetList
    
    def skillCDProcess(self):
        '''所有角色的技能CD处理'''
        for actor in self.order:
            self.actorSkillCDProcess(actor)
                    
    def actorSkillCDProcess(self,actor):
        '''行动者技能CD处理'''
        #==================================================
        #print '【%s】的所有强力技能CD减1'%self.fighters[actor]['chaName']
        #==================================================
        for skill in self.fighters[actor]['skillCDRecord']:
            if skill['traceCD']>0:
                skill['traceCD']-=1
            
    def canDoSkill(self,actor,releaseNo,skillID):
        '''判断是否能使用技能
        @param actor: int 行动者的ID
        @param releaseNo: 行动者释放技能的序号
        @param skillID: int 技能的ID
        '''
        skillName = all_skillInfo[skillID]['skillName']
        if self.fighters[actor]['skillCDRecord'][releaseNo]['traceCD']>1:
            #==================================================
            #print "【%s】的技能[%s]还在调息中"%(self.fighters[actor]['chaName'],skillName)
            #print "调息剩余回合%d"%self.fighters[actor]['skillCDRecord'][releaseNo]['traceCD']
            #==================================================
            return False
#        skillDistanceType = all_skillInfo[skillID]['distanceType']#技能的距离类型 1远程 2近身
#        skillRangeType = all_skillInfo[skillID]['rangeType']#技能的范围类型 1单体 2全体 ..
        skillAttributeType = all_skillInfo[skillID]['attributeType']#技能的属性类型 1物理 2魔法
#        skillTargetType = all_skillInfo[skillID]['targetType']#技能的目标类型 1己方 2敌方
        skillExpendPower = all_skillInfo[skillID]['expendPower']#技能能量消耗
        
        if self.fighters[actor]['chaCurrentPower']< skillExpendPower:#能量不够时
            #==================================================
            #print '能量不足，直接上吧...'
            #==================================================
            return False
        if not self.fighters[actor]['canDoPhysicalSkill'] and skillAttributeType==1:
            return False
        if not self.fighters[actor]['canDoMagicSkill'] and skillAttributeType==2:
            return False
        return True
        
    def canDoOrdSkill(self,actor,OrdSkill):
        '''判断是否能静心普通的攻击
        @param actor: int 行动者的ID
        @param OrdSkill: int 普通技能的ID
        '''
        if self.fighters[actor]['canDoOrdSkill']:
            return True
        return False
    
    def CanBeAttacked(self,target):
        '''判断目标是否是可被攻击的'''
        if self.fighters[target]['canBeAttacked']:
            return True
        return False
    
    def DoFight(self):
        '''战斗计算
        '''
        while True:#如果一方的所有成员死亡，或者总回合数超过15回合，战斗结束
            #==================================================
            #print '主动方列表',self.activeList
            #print '被动方列表',self.passiveList
            #print '行动者列表',self.order
            #==================================================
            if (not self.activeList) or (not self.passiveList)  or (not self.order) or self.now_round>15:
                break
            self.now_round +=1
            self.RoundProcess()#每回合处理
            #==================================================
            #print "第[%d]回合结束 。。"%self.now_round
            #print '\n'
            #==================================================
        #print self.resources
        
    def RoundProcess(self):
        '''回合处理'''
        for actor in self.order:
            if (not self.activeList) or (not self.passiveList) or self.now_round>15:
                break
            self.doBufferEffect(actor)
            if (not self.activeList) or (not self.passiveList) or self.now_round>15:
                break
            self.actorSkillCDProcess(actor)
            self.goFight(actor)
    
    def doBufferEffect(self,actor):
        '''处理buff效果
        @param actor: int 行动者的ID
        '''
        self.battleStateMachine.executeBuffEffects(actor)
            
    def goFight(self,actor):
        '''开始战斗计算
        @param actor: int 行动者的ID
        '''
        if self.fighters[actor]['died']:
            return
        OrdSkill = self.fighters[actor]['ordSkill']#角色的普通攻击技能
        releaseNo = self.fighters[actor]['nextReleaseSkill']#角色释放技能的序号
        skillID = self.fighters[actor]['ActiveSkillList'][releaseNo]#角色要释放的战斗技能
        releaseSkill = 0#将要释放的技能（包括战斗技能和普通攻击的技能）
        
        if self.canDoSkill(actor,releaseNo,skillID):#判断是否能释放技能
            releaseSkill = skillID
        elif self.canDoOrdSkill(actor, OrdSkill):#判断是否能进行
            releaseSkill = OrdSkill
        else:
            return
        self.doSkill(actor,releaseSkill)

    def doSkill(self,actorId,skillId):
        '''进行技能攻击'''
        data = {}
        actor = self.fighters[actorId]
        data['chaId'] = actor['chaId']#角色的Id
        data['chaBattleId']= actor['chaBattleId']#角色战斗ID
        data['chaProfessionType'] = actor['chaProfessionType']#角色的
        data['actionId'] = actor['chaProfessionType']*1000\
        + {True:560,False:570}.get(skillId==actor['ordSkill'])#动作ID
        data['counterHitActionId'] = actor['chaProfessionType']*1000 + 580
        data['isDeathOfCounterHit'] = 0 #攻击方是否被反击致死 0:否，1：是
        data['txtEffectId'] = 0#文字特效（暴击等闪避）
#        data['skillId'] = skillId#技能的ID
        data['chaEffectId'] = all_skillInfo[skillId]['releaseEffect']#角色释放技能特效
        data['chaEnemyEffectId'] = all_skillInfo[skillId]['bearEffect']#角色技能承受特效
        data['chaThrowEffectId'] = all_skillInfo[skillId]['throwEffectId']#角色技能投射特效
        data['chaAoeEffectId'] = all_skillInfo[skillId]['aoeEffectId']#角色技能投射特效
        data['chaBuffArr'] = []#角色身上的buff
        data['chaBuffShowList'] = []#角色身上buff显示信息
        data['chaPowerUp'] = 0#+20 power增加
        data['chaPowerDown'] = 0#-20 power减少
        data['chaCurrentPower'] = actor['chaCurrentPower']#当前能量
        data['chaChangeHp'] = 0#±20 正负HP，可能有加血技能
        data['chaCurrentHp'] = actor['chaCurrentHp']#角色的当前血量
        data['chaExpendHp'] = 0#角色技能消耗的血量
        data['chaStartPos'] = actor['chaPos']#角色的起始坐标
        data['chaTargetPos'] = actor['chaPos']#角色的目标坐标
        data['chaAttackType'] = 3-all_skillInfo[skillId]['distanceType']
        data['isCriticalBlow'] = False
        data['chaDirection'] = actor['chaDirection']#玩家朝向右，朝向右。2--玩家朝向左
        data['enemyChaArr'] = []#所有受攻击者的信息
        
        skillDistanceType = all_skillInfo[skillId]['distanceType']#技能的距离类型 1远程 2近身
        skillName = all_skillInfo[skillId]['skillName']
        skillRangeType = all_skillInfo[skillId]['rangeType']#技能的范围类型 1单体 2全体 ..
        skillAttributeType = all_skillInfo[skillId]['attributeType']#技能的属性类型 1物理 2魔法
        skillTargetType = all_skillInfo[skillId]['targetType']#技能的目标类型 1己方 2敌方
        releaseCD = all_skillInfo[skillId]['releaseCD']#技能的调息时间
        skillExpendPower = all_skillInfo[skillId]['expendPower']#技能能量消耗
        skillExpendHp = all_skillInfo[skillId]['expendHp']#技能血量消耗
        skillFormula = all_skillInfo[skillId]['effect']['formula']#技能计算公式
        clearBuffId= all_skillInfo[skillId]['effect']['clearBuffId']#清除buff的id
        addBuffId = all_skillInfo[skillId]['effect']['addBuffId']#添加buff的ID
        
        targetList = self.findTarget(actorId, rule = skillRangeType)
        if skillTargetType == 2:
            for target in targetList:
                if not self.CanBeAttacked(target):#如果目标不能被攻击则从目标列表中移除
                    #==================================================
                    #print '【%s】从目标列表中移除'%self.fighters[target]['chaName']
                    #==================================================
                    targetList.remove(target)
        if not targetList:
            return
        #==================================================
        #print "【%s】的当前血量为%d"%(actor['chaName'],data['chaCurrentHp'])
        #print "【%s】使用了技能[%s]"%(actor['chaName'],skillName)
        #==================================================
        nowReleaseSkill = actor['nextReleaseSkill']
        actor['skillCDRecord'][nowReleaseSkill]['traceCD'] = releaseCD
        actor['nextReleaseSkill']+=1#下次释放技能的序号指向下一个技能
        if actor['nextReleaseSkill']>=len(actor['ActiveSkillList']):
            actor['nextReleaseSkill']=0
        data['chaPowerDown'] = -skillExpendPower
        data['chaExpendHp'] = -skillExpendHp
        actor['chaCurrentPower'] -= skillExpendPower
        actor['chaCurrentHp'] -= skillExpendHp
        
        if skillDistanceType==2:#根据技能距离判断攻击者的最终位置
            if self.fighters[targetList[0]]['chaDirection']==1:
                data['chaTargetPos'] = [self.fighters[targetList[0]]['chaPos'][0]+10,self.fighters[targetList[0]]['chaPos'][1]]
            else:
                data['chaTargetPos'] = [self.fighters[targetList[0]]['chaPos'][0]-10,self.fighters[targetList[0]]['chaPos'][1]]
            #添加移动的资源
            self.resources.add(actor['chaProfessionType']*1000 +550)
            
        
        #对每个受攻击者的数据进行计算
        for target in targetList:
            info = {}
            enemy = self.fighters[target]
            enemy['skillIDByAttack'] = skillId
            info['enemyChaId'] = enemy['chaId']#受攻击者的角色的id
            info['enemyBattleId'] = target#受攻击者的战场id
            info['enemyActionId'] = enemy['chaProfessionType']*1000+580#受攻击者的动作id
            info['enemyCounterHitActionId'] = enemy['chaProfessionType']*1000+560#反击时的动作ID
            info['enemyTxtEffectId'] = 0#受攻击者的文字特效
#            info['enemySkillId'] = enemy['ordSkill']#受攻击者的技能id(通常反击时为普通攻击)
            info['chaEffectId'] = all_skillInfo[enemy['ordSkill']]['releaseEffect']
            info['chaEnemyEffectId'] = all_skillInfo[enemy['ordSkill']]['bearEffect']
            info['chaThrowEffectId'] = all_skillInfo[enemy['ordSkill']]['throwEffectId']
            info['chaEnemyAoeEffectId'] = all_skillInfo[enemy['ordSkill']]['aoeEffectId']
            info['enemyBuffArr'] = []#受攻击者的buff列表
            info['enemyBuffShowList'] = []#受攻击者的buff信息列表
            info['enemyPowerUp'] = 0#受攻击者的能量增量
            info['enemyCurrentPower'] = enemy['chaCurrentPower']#受攻击者的当前能量
            info['enemyChangeHp'] = 0#受攻击者丢失的血量
            info['enemyCurrentHp'] = enemy['chaCurrentHp']#受攻击者的当前血量
            info['enemyCounterHit'] = 0#受攻击者是否反击 0没有 1反击
            info['enemyStartPos'] = enemy['chaPos']#受攻击者的起始坐标
            info['enemyTargetPos'] = enemy['chaPos']#受攻击者的目标坐标
            info['enemyDirection'] = enemy['chaDirection']#玩家朝向右，朝向右。2--玩家朝向左
            if skillTargetType == 2:#判断是否被闪避（己方成员的辅助技能不会闪避）
                hitRate = actor['hitRate']/enemy['dodgeRate'] 
                rate = random.randint(1,100)
                if rate <hitRate:
                    #==================================================
                    #print "【%s】闪避了【%s】的攻击"%(enemy['chaName'],actor['chaName'])
                    #==================================================
                    info['enemyActionId']= 201 #闪避
                    info['enemyTxtEffectId'] = 201 #闪避
                    continue
            
            
            if skillAttributeType == 1:
                attack = actor['physicalAttack']
                defense = enemy['physicalDefense']
            else:
                attack = actor['magicAttack']
                defense = enemy['magicDefense']
            defensePercent = defense/(defense+100*(enemy['chaLevel']-8))*1.0
            #==================================================
            #print "【%s】攻击力为 %d"%(actor['chaName'],attack)
            #print "【%s】防御力为 %d"%(enemy['chaName'],defense)
            #==================================================
            
            rate = random.randint(1,100)#判断破甲
            if rate <actor['ignore']:
                #==================================================
                #print "【%s】被【%s】破甲"%(enemy['chaName'],actor['chaName'])
                #==================================================
                info['enemyActionId']= 202 #破甲
                info['enemyTxtEffectId'] = 202 #破甲
                defensePercent *= 0.7
            #==================================================
            #print "防御最终减免为",(defensePercent)
            #==================================================
            damage = attack*abs(defensePercent)
            
            rate = random.randint(1,100)#判断暴击
            if rate <actor['ignore']:
                #==================================================
                #print "【%s】被【%s】暴击"%(enemy['chaName'],actor['chaName'])
                #==================================================
                info['enemyActionId']= 202 #暴击
                info['enemyTxtEffectId'] = 202 #暴击
                data['isCriticalBlow'] = True
                if skillAttributeType==1:
                    damage *= 2
                else:
                    damage *= 1.5
            nowdamage = damage
            try:
                exec(skillFormula)
            except Exception as e:
                #print e
                return
            if damage==nowdamage:
                defensePercent = defense/(defense+100*(enemy['chaLevel']-8))*1.0
                damage = attack*abs(defensePercent)
                    
            damage = int(math.ceil(damage))
            #==================================================
            #print "【%s】受到【%s】的最终伤害为%d"%(enemy['chaName'],actor['chaName'],damage)
            #print "【%s】的当前血量为%d"%(enemy['chaName'],enemy['chaCurrentHp'])
            #==================================================
            info['enemyPowerUp'] = 100#受攻击者的能量增量
            info['enemyChangeHp'] = -damage
            #==================================================
            #print "【%s】血量变化为%d"%(enemy['chaName'],info['enemyChangeHp'])
            #==================================================
            enemy['chaCurrentHp'] += info['enemyChangeHp']
            enemy['chaCurrentPower'] += info['enemyPowerUp']
            #==================================================
            #print "【%s】受击后血量为%d"%(enemy['chaName'],enemy['chaCurrentHp'])
            #==================================================
            if enemy['chaCurrentHp']<=0:
                #print "【%s】被【%s】杀死"%(enemy['chaName'],actor['chaName'])
                info['enemyActionId'] = enemy['chaProfessionType']*1000+590
                enemy['died']=1#角色死亡
                self.order.remove(target)
                if enemy['chaDirection']==1:
                    self.activeList.remove(target)
                else:
                    self.passiveList.remove(target)
#                continue
            
            #-------------受攻击buff触发处理-------------
            if clearBuffId:
                self.battleStateMachine.clearBuffById(target, clearBuffId)
            if addBuffId:
                self.battleStateMachine.putBuff(target, addBuffId)
            produceResult = self.battleStateMachine.produceBuffEffect(target, actorId)
#            if produceResult:
#                continue
            #--------------反击处理----------------
            if skillDistanceType==2 and skillRangeType==1 and skillTargetType ==2 and enemy['died']!=1:#近身攻击 单体攻击 目标位己方
                rate = random.randint(1,100)#判断反击
                if rate <enemy['squelch']:
                    #print "【%s】采取了反击"%(enemy['chaName'])
                    #print "大吼一声：“鼠辈，竟敢伤我！”"
                    info['enemyCounterHit'] = 1
                    toSkill = enemy['ordSkill']
                    toSkillAttributeType = all_skillInfo[toSkill]['attributeType']
                    if toSkillAttributeType == 1:
                        attack = enemy['physicalAttack']
                        defense = actor['physicalDefense']
                    else:
                        attack = enemy['magicAttack']
                        defense = actor['magicDefense']
                    defensePercent = defense/(defense+100*(actor['chaLevel']-8))
                
                    rate = random.randint(1,100)#判断破甲
                    if rate <enemy['ignore']:
                        data['txtEffectId'] = 202 #破甲
                        defensePercent *= 0.7
                    damage = attack*defensePercent
            
                    rate = random.randint(1,100)#判断暴击
                    if rate <enemy['ignore']:
                        data['txtEffectId'] = 203 #暴击
                        if skillAttributeType==1:
                            damage *= 2
                        else:
                            damage *= 1.5
                    damage = int(math.ceil(damage))
                    data['chaChangeHp'] = -damage
                    data['chaPowerUp'] = 20
                    #print "【%s】的当前血量为%d"%(actor['chaName'],actor['chaCurrentHp'])
                    #print "【%s】受到反击伤害%d"%(actor['chaName'],damage)
                    actor['chaCurrentHp'] += data['chaChangeHp']
                    #print "【%s】的受反击后血量为%d"%(actor['chaName'],actor['chaCurrentHp'])
                    actor['chaCurrentPower'] += data['chaPowerUp']
                    if actor['chaCurrentHp']<=0:
                        #print "【%s】被【%s】反击杀死"%(actor['chaName'],enemy['chaName'])
                        actor['died']=1#角色死亡
                        data['counterHitActionId'] = actor['chaProfessionType']*1000 + 590
                        data['isDeathOfCounterHit'] = 1
                        self.order.remove(actorId)
                        if actor['chaDirection']==1:
                            self.activeList.remove(actorId)
                        else:
                            self.passiveList.remove(actorId)
                
            
            info['enemyBuffArr'] = self.battleStateMachine.getTargetBuffList(target)
            info['enemyBuffShowList'] = self.battleStateMachine.getTargetBuffInfoList(target)
            data['enemyChaArr'].append(info)
            
        data['chaBuffArr'] = self.battleStateMachine.getTargetBuffList(actorId)
        data['chaBuffShowList'] = self.battleStateMachine.getTargetBuffInfoList(actorId)
        self.resourceCollect(data)
        self.FightData.append(data)
        #print ''
        
    def resourceCollect(self,data):
        '''资源收集处理
        @param data: dict 战斗的数据
        '''
        self.resources.add(data['actionId'])
        self.resources.add(data['counterHitActionId'])
        self.resources.add(data['chaEffectId'])
        self.resources.add(data['chaEnemyEffectId'])
        self.resources.add(data['chaThrowEffectId'])
        
        self.resources = self.resources | set(data['chaBuffArr'])
        for enemyData in data['enemyChaArr']:
            self.resources.add(enemyData['enemyActionId'])
            self.resources.add(enemyData['enemyTxtEffectId'])
            self.resources.add(enemyData['chaEffectId'])
            self.resources.add(enemyData['chaEnemyEffectId'])
            self.resources.add(enemyData['chaThrowEffectId'])
            self.resources = self.resources | set(enemyData['enemyBuffArr'])
            
            
        
        
        
        
        
