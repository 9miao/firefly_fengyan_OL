#coding:utf8
'''
Created on 2011-3-30

@author: sean_lan
'''
MAP_WIDTH = 550
DISTANCE = 350


import random
from app.scense.core.PlayersManager import PlayersManager
from app.scense.utils.DataLoader import loader
import copy

def bubbleSort(dictor,numbers,key):
    '''冒泡排序'''
    for j in xrange(len(numbers),-1,-1):
        for i in xrange(0,j-1,1):
            if dictor[numbers[i]][key] > dictor[numbers[i+1]][key]:
                numbers[i],numbers[i+1] = numbers[i+1],numbers[i]
            if dictor[numbers[i]][key] == dictor[numbers[i+1]][key]:
                c = random.randint(0,1)
                if c == 1:
                    numbers[i],numbers[i+1] = numbers[i+1],numbers[i] 
    return numbers

class Battle:
    '''战斗类'''
    def __init__(self,challengers = [],defenders = [],BattlefieldWidth = 1000,BattlefieldHeight = 570 ,center = 1125,fightType = 1,roundLimit= 30):
        '''初始化战斗类
        @param challengers: []Character object list 挑战方成员
        @param defenders: []Character object list 防守方成员
        @param BattlefieldWidth: int 战场的宽度
        @param BattlefieldHeight: int 战场的高度
        @param center: int 战场中心
        @param fightType: int 战斗类型 1:打怪   2:决斗 3:boss战
        '''
        self.BattlefieldWidth = BattlefieldWidth
        self.BattlefieldHeight = BattlefieldHeight
        self.center = center
        self.challengers = challengers#挑战方的成员
        self.teamerNum = len(challengers)
        self.defenders = defenders #被攻击方成员列表
        self.fightType = fightType  #战斗类型
        self.battlefield = [] #战场中所有的战斗成员
        self.allFighter = {}
        self.allFighter['ch'] = []
        self.allFighter['de'] = []
        self.roundLimit= roundLimit   #战斗回合限制
        self.rounds = 0     #当前战斗回合数
        self.battleResult = 1    #表示胜利方 1 表示挑战者胜利 2 防守者胜利
        self.winners = []     #胜利成员
        self.sendList = []
        self.settlementData = []     #战斗结算数据
        self.initBattleData()     #初始化战斗信息
        self.getBattleStepData()    #生成战斗数据
        self.getBattleResult()     #获取战斗结果
        self.updateSomeDataAfterBattle() #更新战后的数据
        self.geSettlement()     #获取战斗结算数据
        
    def initBattleData(self):
        '''初始化战斗类，确定每个战斗单位在战场中的位置
        @param tag: 用来标识战斗成员在战场中的id
        '''
        if self.center - MAP_WIDTH <0:
            self.center = 550
        elif self.center + MAP_WIDTH >self.BattlefieldWidth:
            self.center = self.BattlefieldWidth-550
        c_position = [[self.center - DISTANCE,self.BattlefieldHeight/2+120],
                      [self.center - DISTANCE,self.BattlefieldHeight/2+70],
                      [self.center - DISTANCE,self.BattlefieldHeight/2+170],
                      [self.center - DISTANCE,self.BattlefieldHeight/2+20],
                      [self.center - DISTANCE,self.BattlefieldHeight/2+220],
                      [self.center - DISTANCE+150,self.BattlefieldHeight/2+120],
                      [self.center - DISTANCE+150,self.BattlefieldHeight/2+70],
                      [self.center - DISTANCE+150,self.BattlefieldHeight/2+170],
                      [self.center - DISTANCE+150,self.BattlefieldHeight/2+20],
                      [self.center - DISTANCE+150,self.BattlefieldHeight/2+220],]
        
        d_position = [[self.center + DISTANCE,self.BattlefieldHeight/2+120],
                      [self.center + DISTANCE,self.BattlefieldHeight/2+70],
                      [self.center + DISTANCE,self.BattlefieldHeight/2+170],
                      [self.center + DISTANCE,self.BattlefieldHeight/2+20],
                      [self.center + DISTANCE,self.BattlefieldHeight/2+220],
                      [self.center + DISTANCE-150,self.BattlefieldHeight/2+120],
                      [self.center + DISTANCE-150,self.BattlefieldHeight/2+70],
                      [self.center + DISTANCE-150,self.BattlefieldHeight/2+170],
                      [self.center + DISTANCE-150,self.BattlefieldHeight/2+20],
                      [self.center + DISTANCE-150,self.BattlefieldHeight/2+220],]
        if self.fightType==3:
            d_position = [[self.center+DISTANCE,285],]
        tag = 0#表示战斗中的id，动态分配
        mark = 0#分配战斗中的位置
        for character in self.challengers:
            if character.CharacterType ==1:
                player = PlayersManager().getPlayerByID(character.baseInfo.id)
                if not player:
                    continue
                #如果战斗单位的形象为角色，将角色的战斗设为战斗状态
                player.baseInfo.setStatus(4)   #角色状态设置为战斗状态
                self.sendList.append(character.dynamicId)#取出战斗中每个角色的动态id生成sendList
                #便于将战斗数据推送给每个参加战斗的角色
            #下面一段用于副本战斗评分
            self.battlefield.append(character.getDataForFight())
            self.battlefield[tag]['camp'] = 1
            self.battlefield[tag]['labelId'] = tag    #角色在战场中的id
            self.battlefield[tag]['position'] = c_position[mark]
            self.battlefield[tag]['attackNum'] = 0    #攻击次数
            self.battlefield[tag]['beDodgeNum'] = 0     #被闪避次数
            self.battlefield[tag]['dodgeNum'] = 0     #闪避次数
            self.battlefield[tag]['defenseNum']=0     #防守的次数
            self.battlefield[tag]['criNum']= 0     #暴击的次数
            self.battlefield[tag]['bogeyNum'] = 0    #破防的次数
            self.battlefield[tag]['cri_bogeyNum'] = 0     #暴击加破防的次数
            self.battlefield[tag]['died'] = 0     #角色是否死亡
            self.allFighter['ch'].append(tag)
            tag = tag + 1
            mark = mark + 1
        mark = 0
        for defender in self.defenders:
            if defender.CharacterType ==1:
                player = PlayersManager().getPlayerByID(id)
                player.baseInfo.setStatus(4)   #角色状态设置为战斗状态
                self.sendList.append(defender.dynamicId)
            self.battlefield.append(defender.getDataForFight())
            self.battlefield[tag]['camp'] = 2
            self.battlefield[tag]['labelId'] = tag     #角色在战场中的id
            self.battlefield[tag]['position'] = d_position[mark]
            self.battlefield[tag]['attackNum'] = 0    #攻击次数
            self.battlefield[tag]['beDodgeNum'] = 0     #被闪避次数
            self.battlefield[tag]['dodgeNum'] = 0     #闪避次数
            self.battlefield[tag]['defenseNum']=0     #防守的次数
            self.battlefield[tag]['criNum']= 0     #暴击的次数
            self.battlefield[tag]['bogeyNum'] = 0    #破防的次数
            self.battlefield[tag]['cri_bogeyNum'] = 0     #暴击加破防的次数
            self.battlefield[tag]['died'] = 0     #角色是否死亡
            self.allFighter['de'].append(tag)
            tag = tag + 1
            mark = mark + 1
        self.initData = copy.deepcopy(self.battlefield)
        return self.battlefield
    
    def grouping(self):
        '''把战斗成员随机分成随机个组，每个随机组的战斗单位相互战斗，与其他组的战斗可以同时进行'''
        self.rounds = self.rounds+1
        teamNum = 0
        self.all_fightTeam = None
        if len(self.allFighter['ch'])==0 or len(self.allFighter['de'])==0:
            return None
        if len(self.allFighter['ch'])> len(self.allFighter['de']):
            teamNum = random.randint(1,len(self.allFighter['de']))
        else:
            teamNum = random.randint(1,len(self.allFighter['ch']))
    
        ch = []
        de = []
        ch.extend(self.allFighter['ch'])
        de.extend(self.allFighter['de'])
        ch_member = []
        de_member = []
        all_fightTeam = {}
        for i in range(teamNum):
            ch_member.append([])
            ch_member[i].append(ch[0])
            ch.remove(ch[0])
            
            de_member.append([])
            de_member[i].append(de[0])
            de.remove(de[0])
        for i in ch:
            tag = random.randint(0,teamNum-1)
            ch_member[tag].append(i)
        for i in de:
            tag = random.randint(0,teamNum-1)
            de_member[tag].append(i)
        
        
        for i in range(teamNum):
            all_fightTeam[i] = {}
            all_fightTeam[i]['ch'] =[]
            all_fightTeam[i]['ch'].extend(ch_member[i])
            all_fightTeam[i]['de'] =[]
            all_fightTeam[i]['de'].extend(de_member[i])
                                                           
        self.all_fightTeam = all_fightTeam
        
    def getBattleStepData(self):
        '''获取战斗步骤信息'''
        self.StepData = []
        stepNo = 0
        while True:
            self.grouping()
            if not self.all_fightTeam or (self.rounds >=self.roundLimit):
                return self.StepData
            step = self.goFight()
            stepNo += 1
            self.StepData.append(step)
        return self.StepData
    
    
    def goFight(self):
        '''每一轮的战斗信息'''
        stepdata = []
        for tag in self.all_fightTeam.values():
            teamData = []
            groupMenber = []
            for fighter in tag['ch']:
                groupMenber.append(fighter)
            for fighter in tag['de']:
                groupMenber.append(fighter)
            fighterMenber = bubbleSort(self.battlefield , groupMenber,'speed')
            for ch_id in fighterMenber:
                if self.battlefield[ch_id]['camp']== 1:
                    de_id = random.choice(tag['de'])
                    FightData = self.Fight(ch_id,de_id,tag)
                    if FightData:
                        teamData.append(FightData)
                else:
                    de_id = random.choice(tag['ch'])
                    FightData = self.Fight(ch_id,de_id,tag)
                    if FightData:
                        teamData.append(FightData)
            stepdata.append(teamData)
        return stepdata
        
    def Fight(self,ch ,de ,tag):
        '''产生每一个行动者的战斗数据'''
        if self.battlefield[ch]['died'] == 1:
            return {}
        if self.battlefield[de]['died'] == 1:
            return {}
        
        self.battlefield[ch]['attackNum'] = self.battlefield[ch]['attackNum'] + 1
        self.battlefield[de]['defenseNum'] = self.battlefield[de]['defenseNum'] +1
        
        owner = self.battlefield[ch]
        opponent = self.battlefield[de]
        data = {}
        data['actorsDBId'] = self.battlefield[ch]['id']
        data['actors'] = ch
        data['actType'] = 103# 行动类型 
        data['isCrit']= 0
        data['actorsFightType'] = self.battlefield[ch]['fightType']#角色的攻击类型，由角色的职业来决定 1 为近战 2为远程
        data['actorsFigure'] = self.battlefield[ch]['figure'] #攻击者的形象
        #---------------*------技能特效相关-------*----------------
        data['skillId'] = -1# 技能id -1 表示没有使用技能
        data['skillReleaseEffect'] = -1 #发动技能时自身产生的特效
        data['skillthrowEffect'] = -1 # 技能投射的特效ID
        
        data['fixedPointEffectId'] = -1 # 定点特效ID
        
        data['startPosition'] = self.battlefield[ch]['position']#起始坐标
        data['endPosition'] = [0,0]#结束坐标
        data['actorsHp'] = self.battlefield[ch]['hp']#行动者当前血量值
        data['actorsMp'] = self.battlefield[ch]['mp']#行动者当前魔力值
        data['actorsMaxHp']= self.battlefield[ch]['maxHp']#行动者最大血量值
        data['actorsMaxMp']= self.battlefield[ch]['maxMp']#行动者最大魔力值
        data['actorLostHp'] = 0#行动者丢失血量
        data['actorLostMp'] = 0#行动者丢失魔力
        #--------------------*----受攻击者信息-----*---------------
        data['victimDBId'] = self.battlefield[de]['id']
        data['victim'] = de#受伤者的id
        data['victimFigure'] = self.battlefield[de]['figure']   #受攻击者的形象
        data['victimPosition'] = self.battlefield[de]['position']#受伤者所处的位置
        data['skillBearEffect'] = -1 #技能承受时产生的特效
        data['victimFixedPointEffectId'] = -1#受伤者定点特效ID
        data['injuredType'] = 104#受伤者的受伤类型  104 受攻击 105 死亡 #106 miss   #暴击 4破防 5暴击+破防 6 闪避 7 死亡
        data['victimHp'] = self.battlefield[de]['hp']#受攻击者当前血量
        data['victimMp'] = self.battlefield[de]['mp']#受攻击者当前魔力
        data['victimMaxHp'] = self.battlefield[de]['maxHp']#受攻击者最大血量
        data['victimMaxMp'] = self.battlefield[de]['maxMp']#受攻击者最大魔力
        data['victimLostHp'] = 0#受攻击者丢失血量
        data['victimLostMp'] = 0#受攻击者丢失魔力
        
        if self.battlefield[ch]['camp'] == 1:
            data['endPosition'] = [data['victimPosition'][0]-100,data['victimPosition'][1]]
        else:
            data['endPosition'] = [data['victimPosition'][0]+100,data['victimPosition'][1]]
        #开始计算伤害
        damageType = 104
        skillId = self.ProcessSkill(owner)
        skillInfo = loader.getById('attackSkill',skillId,'*')
        
        data['skillId'] = skillId
        data['skillReleaseEffect'] = skillInfo['skillReleaseEffect']
        data['skillthrowEffect'] = skillInfo['skillthrowEffect']
        data['skillBearEffect'] = skillInfo['skillBearEffect']
        #damage = 0
        damage = self.doSkill(skillId, owner, opponent)
        reduction = opponent['defense']
        
        isMissed = 0 #是否miss 0未miss 1 miss
        if skillId == owner['OrdinarySkills']:
            hitRate = (95 + owner['hitRate'] - opponent['dodgeRate'])
            r = random.uniform(0, 100)
            if r <= hitRate:#是否命中  命中
                tag_cri = 0  #暴击标识   0未暴击 1暴击
                tag_bogey = 0 #破防标识  0 未破防 1破防
                
                r = random.uniform(0, 100)
                if r <= 30 and self.battlefield[ch]['figure'] in [1,2,3,4]:#owner['criRate']:#是否暴击
                    tag_cri = 1
                    self.battlefield[ch]['criNum'] = self.battlefield[ch]['criNum']+1
                    damage = damage * 1.5
                    data['isCrit'] =1
                    
                r = random.uniform(0, 100)#是否破防  
                if r <= owner['bogeyRate']:
                    tag_bogey = 1
                    self.battlefield[ch]['bogeyNum'] = self.battlefield[ch]['bogeyNum']+1
                    reduction = 0 #破防后减伤为 0
                    
                if tag_cri==1 and tag_bogey==1:
                    self.battlefield[ch]['cri_bogeyNum'] = self.battlefield[ch]['cri_bogeyNum']+1
                    
            else:#未命中
                self.battlefield[ch]['beDodgeNum'] = self.battlefield[ch]['beDodgeNum']+1
                self.battlefield[de]['dodgeNum'] = self.battlefield[de]['dodgeNum']+1
                damageType = 104
                isMissed = 1
                damage = 0
                
        if isMissed !=1: #是否miss
            damage = damage - (float(reduction) * 0.000215)
            if damage < 1: #如果没有miss 造成的最终伤害小于1时，强制掉血1点
                damage = 1
                
        opponent['hp'] = opponent['hp'] - damage
        
        if opponent['hp']<=0 :#受攻击者的血量小于或等于0 死亡
            damageType =105
            #print "one fighter died %d"%de
            self.battlefield[de]['hp'] = 0
            opponent['hp'] = 0
            
        if owner['hp'] <= 0:
            owner['hp'] =0
            
        data['victimLostHp'] = -(data['victimHp'] - opponent['hp'])
        data['victimLostMp'] = -(data['victimMp'] - opponent['mp'])
        
        data['actorLostHp'] = -(data['actorsHp'] - owner['hp'])
        data['actorLostMp'] = -(data['actorsMp'] - owner['mp'])
        data['injuredType'] = damageType
        #记录保留战斗后的数据
        self.battlefield[de]['hp'] = opponent['hp']
        self.battlefield[de]['mp'] = opponent['mp']
        self.battlefield[ch]['hp'] = owner['hp']
        self.battlefield[ch]['mp'] = owner['mp']
        if damageType == 105:
            self.battlefield[de]['died'] = 1
            #print "% id died"%de
            if opponent['camp'] ==1:
                self.allFighter['ch'].remove(de)
            else:
                self.allFighter['de'].remove(de)
                
        return data
    
    def ProcessSkill(self,user):
        '''选择技能进行攻击，如果没触发技能则使用普通攻击'''
        skill = []
        charweapon = user['weaponType']
        mp = user['mp']
        for sk in user['activeSkill']:
            if sk['weapon']!= charweapon:
                continue
            if sk['useMp']>mp:
                continue
            r = random.randint(0, 100000)
            if r > skill['useRate']:
                continue
            skill.append(sk['id'])
        if not skill:
            return user['OrdinarySkills']
        return random.choice(skill)
    
    def doSkill(self,skillId ,owner ,opponent):
        '''技能事件'''
        damage = random.uniform(float(owner['minAttack']), float(owner['maxAttack']))
        damage = damage - float(opponent['defense']) * 0.000215
        return damage
        
    def getBattleResult(self):
        '''获取战斗结果'''
        chHp = 0   #挑战方的血量
        deHp = 0   #防守方的血量
        for i in self.allFighter['ch']:
            chHp = chHp+self.battlefield[i]['hp']
        for i in self.allFighter['de']:
            deHp = deHp+self.battlefield[i]['hp']
        if chHp<deHp:
            self.battleResult = 2
            self.winners.extend(self.allFighter['de'])
        else:
            self.battleResult = 1
            self.winners.extend(self.allFighter['ch'])
            
    def updateSomeDataAfterBattle(self):
        '''更新战斗后的数据'''
        for member in self.battlefield:
            if  member['CharacterType']==1:
                player = PlayersManager().getPlayerByID(member['id'])
                player.attribute.updateHp(int(member['hp']))
                player.attribute.updateMp(int(member['mp']))
                if member['died']:
                    player.status.updateLifeStatus(0)
        
    def geSettlement(self):
        '''获取战斗结算数据'''
        if self.battleResult==2:
            return
        exGoal = 20000
        coinGoal = 0
        goldGoal = 0
        itemGoal = []
        defenders = [defende for defende in self.battlefield if defende['camp']==2]
        if self.fightType== 1:#打怪
            for defender in defenders:
                exGoal = exGoal + defender['expBonus']
                coinGoal = coinGoal +defender['coinBonus']
                goldGoal = goldGoal+ defender['goldBonus']
                itemGoal.append(defender['dropItemId'])
                
        self.winners = [self.battlefield[winner] for winner in self.winners if self.battlefield[winner]['CharacterType']==1]
        
        for winner in self.winners:
            settlementData = {}
            attackLostGoal = 0
            if winner['attackNum']!=0:
                attackLostGoal = float(winner['beDodgeNum'])/float(winner['attackNum'])*100
            defenseGoal = float(winner['hp'])/float(winner['maxHp'])*100
            defenseGetGoal = 0
            if winner['defenseNum']!=0:
                defenseGetGoal = float(winner['dodgeNum'])/float(winner['defenseNum'])*100
            
            settlementData['id'] = winner['id']
            settlementData['expBonus'] = exGoal/len(self.winners)
            settlementData['coinBonus'] = coinGoal/len(winner)
            settlementData['goldBonus'] = goldGoal/len(winner)
            settlementData['attackGoal'] = int(100-attackLostGoal)
            settlementData['defenseGoal'] = int(defenseGoal + defenseGetGoal)
            if settlementData['defenseGoal']>100:
                settlementData['defenseGoal']=100
            settlementData['slayGoal'] = winner['criNum']+winner['bogeyNum']+winner['cri_bogeyNum']*3
            if settlementData['slayGoal']>100:
                settlementData['slayGoal']=100
            settlementData['popularity'] = 5
            settlementData['itemsBonus'] = None  #奖励的物品
            player = PlayersManager().getPlayerByID(winner['id'])
            if self.fightType ==1:
                itemDropConfig = random.choice(itemGoal)
                if itemDropConfig:
                    dropItem = None
                    dropItem = player.dropping.getItemByDropping(itemDropConfig) #根据掉落配置得到物品
                    if dropItem:
                        #print dropItem
                        player.pack.putNewItemInPackage(dropItem)
                        settlementData['itemsBonus']=dropItem#.formatItemInfo()
            
#            player.attribute.updateHp(int(winner['hp']))
#            player.attribute.updateMp(int(winner['mp']))
            if winner['died']:
                player.status.updateLifeStatus(0)
            player.level.updateExp(player.level.getExp()+settlementData['expBonus'],status = 0)
            player.finance.updateCoin(player.finance.getCoin()+settlementData['coinBonus'])
            player.finance.updateGold(player.finance.getGold()+settlementData['goldBonus'])
            player.updatePlayerInfo(statu=0)
            self.settlementData.append(settlementData)

        
