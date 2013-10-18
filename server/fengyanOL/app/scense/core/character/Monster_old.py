#coding:utf8
'''
Created on 2011-4-6

@author: sean_lan
'''
import random
from app.scense.utils.DataLoader import loader,connection
from app.scense.core.character.Character import Character
from app.scense.utils.dbopera import dbMonster 
from app.scense.core.language.Language import Lg

def RandomAssignment(queue):
    lst = []
    down = 0
    up = 0
    for item in queue:
        down = up
        up += item["probability"]
        assert up <= 1
        lst.append((item, down, up))
    randomnumber = random.random()
    for i in lst:
        if i[1] <= randomnumber < i[2]:
            return i[0]

class Monster(Character):
    '''怪物类
    '''
    TotalSeed = 100000.0
    def __init__(self,id = -1,name='',templateId= 0,x = 300,y = 400):
        '''初始化怪物类
        '''
        Character.__init__(self, id, name)
        self.CharacterType = 2
        self.templateId = templateId
        self.baseInfo.setPosition((x,y))
        data = loader.getById('npc',templateId, '*')
        self.formatInfo = {}
        if data:
            self.initialise(data)
            
    def initialise(self,data):
        '''初始化怪物信息
        '''
        levelgroup = data['levelGroup'].split(';')
        encounteroddgroup = data['encounterOddGroup'].split(';')
        dropitemidgroup = data['dropItemIdGroup'].split(';')
        levelQueue = []

        assert len(levelgroup) == len(encounteroddgroup) == len(dropitemidgroup)

        last_probability = 0
        for i in range(len(levelgroup)):
            levelMap = {}
            encounterodd_S = int(encounteroddgroup[i]) / self.TotalSeed
            levelMap["level"] = int(levelgroup[i])
            levelMap["dropItemId"] = int(dropitemidgroup[i])
            this_probability = 1 - last_probability
            probability = this_probability * encounterodd_S
            levelMap['probability'] = probability
            last_probability = last_probability + probability
            levelQueue.append(levelMap)

        monster_group_id = data['monsterGroupId']
        
        element = RandomAssignment(levelQueue)
        monster_level = element['level']
        monster_dropitem_id = element['dropItemId']

        cursor = connection.cursor()
        cursor.execute("select * from `monster_instance` where groupId=%d and level=%d" % (monster_group_id, monster_level))
        monsters = cursor.fetchall()
        cursor.close()
        if(len(monsters) <= 0):
            raise Exception('没有找到怪物实例')
            return None
        monster_instance = monsters[0]

        self.formatInfo['id'] = self.baseInfo.id
        self.baseInfo.setName(data['name'])
        self.formatInfo['name'] = data['name']
        self.formatInfo['level'] = monster_level
        self.formatInfo['figure'] = self.templateId#monster_instance['figure']

        self.formatInfo['hp'] = int(monster_instance['hp'])
        self.formatInfo['mp'] = int(monster_instance['mp'])

        self.formatInfo['maxHp'] = int(monster_instance['hp'])
        self.formatInfo['maxMp'] = int(monster_instance['mp'])

        self.formatInfo['speed'] = int(monster_instance['speed'])
        self.formatInfo['OrdinarySkills'] = int(data['skillId'])
        self.formatInfo['maxAttack'] = int(monster_instance['maxAttack'])
        self.formatInfo['minAttack'] = int(monster_instance['minAttack'])
        self.formatInfo['defense'] = int(monster_instance['defense'])
        self.formatInfo['abs_damage'] = 0
        self.formatInfo['damagePercent'] = 0

        self.formatInfo['hitRate'] = monster_instance['hitRate']
        self.formatInfo['dodgeRate'] = monster_instance['dodgeRate']
        self.formatInfo['criRate'] = monster_instance['criRate']
        self.formatInfo['bogeyRate'] = monster_instance['bogeyRate']

        self.formatInfo['expBonus'] = monster_instance['expBonus']
        self.formatInfo['coinBonus'] = monster_instance['coinBonus']
        self.formatInfo['goldBonus'] = monster_instance['goldBonus']
        self.formatInfo['dropItemId'] = monster_dropitem_id
        self.formatInfo['_instance'] = self

        self.initialiseToo(self.templateId) #取出数据库里面怪物的值 进行覆盖
        
        
    def initialiseToo(self,id):
        '''取出数据库里面怪物的值 进行覆盖
            @param id: int 怪物id
        '''
        data=dbMonster.getById(id)
        if data:
            self.formatInfo['name'] = data['nickname']
            self.formatInfo['level'] = data['level']
            self.formatInfo['hp'] = data['hp']
            self.formatInfo['mp'] = data['mp']
            self.formatInfo['speed'] = data['Speed']
            self.formatInfo['maxHp'] = data['hp']
            self.formatInfo['maxMp'] = data['mp']
            self.formatInfo['hitRate'] = data['Hit']
            self.formatInfo['criRate']=data['Force']
            self.formatInfo['dodgeRate']=data['Dodge']
            self.formatInfo['type']=data['viptype']
    
    
    def updateLocation(self):
        '''随机更新怪物的位置'''
        
        position = self.baseInfo.getStaticPosition()
        x = position[0]+random.randint(-100,100)
        y = position[1]+random.randint(-50,50)
        self.baseInfo.setPosition((x,y))
        
    def getDataForFight(self):
        '''获取角色战斗中需要的数据'''
        values = {}
        #-------------------基础信息----------------#
        values['id'] = self.baseInfo.id  #角色的id
        values['name'] = self.formatInfo['name'] #角色的名称
        values['CharacterType'] = 2 #角色的类型   1 玩家角色  2 怪物  3 宠物（待定）
        values['figure'] = self.templateId #角色的形态
        values['level'] = self.formatInfo['level'] #角色的等级
        values['hp'] = self.formatInfo['hp'] #角色当前血量
        values['mp'] = self.formatInfo['mp'] #角色当前mp值
        values['maxHp'] = self.formatInfo['maxHp'] #最大血量值
        values['maxMp'] = self.formatInfo['maxMp'] #最大魔力值
        
        #-------------------装备武器信息------------------#
        values['weaponName'] = Lg().g(504)#角色武器名称
        values['weaponType'] = Lg().g(505)#武器类型
        
        #-------------------战斗类型--------------------#
        values['fightType'] = 1 #角色的攻击类型，由角色的职业来决定 1 为近战 2为远程
    
        #--------------------几率相关-------------------#
        
        values['hitRate'] = self.formatInfo['hitRate']#获取命中几率
        values['criRate'] = self.formatInfo['criRate']#获取暴击
        values['bogeyRate'] = self.formatInfo['bogeyRate']#获取破防
        values['dodgeRate'] = self.formatInfo['dodgeRate']#获取躲避几率
        
        #--------------------伤害防御相关属性-----------------------#
        values['speed'] = self.formatInfo['speed'] #获取角色的攻速
        values['defense'] = self.formatInfo['defense']#获取防御属性
        values['maxAttack'] = self.formatInfo['maxAttack']#获取最大攻击
        values['minAttack'] = self.formatInfo['minAttack']#获取最小攻击
        values['abs_damage'] = self.formatInfo['abs_damage']#获取被动技能伤害加成数值
        values['damagePercent'] = self.formatInfo['damagePercent']#获取被动技能伤害加成百分比
        #-------------------技能相关--------------------#
        values['activeSkill'] = []
        values['OrdinarySkills'] =  self.formatInfo['OrdinarySkills']#普通攻击技能
        #-------------------战胜后的奖励----------------#
        values['expBonus'] = self.formatInfo['expBonus']
        values['coinBonus'] = self.formatInfo['coinBonus']
        values['goldBonus'] = self.formatInfo['goldBonus']
        values['dropItemId'] = self.formatInfo['dropItemId']

        return values
    
    def getFightData(self):
        '''获取怪物战斗数据'''
        fightdata = {}
        fightdata['chaId'] = self.baseInfo.id               #角色的ID
        fightdata['chaName'] = self.formatInfo['name']  #角色的昵称
        fightdata['chaBattleId'] = 0                        #角色在战场中的id
        fightdata['chaProfessionType'] = self.baseInfo.id#角色的角色形象ID
        fightdata['chaDirection'] = 1#(角色在战斗中的归属阵营)1--(主动方)玩家朝向右，朝向右。2(被动方)--玩家朝向左
        fightdata['chaCurrentHp'] = self.formatInfo['hp']#角色当前血量
        fightdata['chaCurrentPower'] = 0#角色的当前能量
        fightdata['chaTotalHp'] = self.formatInfo['hp']#角色的最大血量
        fightdata['chaTotalPower'] = 100#角色的最大能量
        fightdata['chaPos'] = (0,0)#角色的坐标
        fightdata['physicalAttack'] = self.attribute.getCurrPhyAtt()#角色的物理攻击
        fightdata['magicAttack'] = self.attribute.getCurrMigAtt()#角色的魔法攻击
        fightdata['physicalDefense'] = self.attribute.getCurrPhyDef()#角色的物理防御
        fightdata['magicDefense'] = self.attribute.getCurrMigDef()#角色的魔法防御
        fightdata['speed'] = self.attribute.getCurrSpeed()#角色的攻速
        fightdata['squelch'] = self.attribute.getCurrSquelch()#角色的反击
        fightdata['ignore'] = self.attribute.getCurrIgnore()#角色的破甲
        fightdata['chaLevel'] = self.level.getLevel()#角色的等级
        fightdata['ActiveSkillList'] = [610101,610201,610301,610401]#self.skill#角色的主动攻击技能
        fightdata['ordSkill'] = 610101#角色的普通攻击技能
        
        
    
    
