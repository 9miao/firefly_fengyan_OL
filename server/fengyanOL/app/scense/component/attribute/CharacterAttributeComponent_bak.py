#coding:utf8
'''
Created on 2011-3-24

@author: sean_lan
'''
from app.scense.utils import dbaccess
from app.scense.utils.dbopera import dbVIP
from app.scense.component.Component import Component
from app.scense.netInterface.pushObjectNetInterface import pushCorpsApplication
from app.scense.core.language.Language import Lg

HPDRUG = [20000000,20000001,20000002]

class CharacterAttributeComponent(Component):
    '''角色属性组件类'''
    def __init__(self, owner, baseStr = 0, baseVit = 0, baseDex = 0, manualStr = 0, manualVit = 0, manualDex = 0, \
                 sparePoint = 0, hp = 100, mp = 100, energy = 200):
        '''
        Constructor
        '''
        Component.__init__(self, owner)
        self._baseStr = baseStr  #系统根据玩家职业赋予玩家的基础力量点数
        self._baseVit = baseVit #系统根据玩家职业赋予玩家的基础体质（耐力）点数
        self._baseDex = baseDex #系统根据玩家职业赋予玩家的基础灵巧（敏捷）点数
        self._baseWis = 0    #基础智力点
        self._baseSpi = 0    #基础精神点
        self._extraStr = 0  #被动技能力量点数
        self._extraDev = 0  #被动技能灵巧（敏捷）点数
        self._extraVit = 0  #被动技能体质（耐力）点数
        self._extraWis = 0  #被动技能智力点数
        self._extraSpi = 0  #被动加上的精神点数
#        self._sparePoint = sparePoint #剩余属性点数
        self._mallrebate = 100 #商城折扣

        self._hp = hp #当前生命:
        self._mp = mp #目前的法力ֵ
        self._energy = energy #当前活力
        self._speed_rate = 1
        self._expEff = 1 #经验获取百分比

    
    def getDiffCan(self):
        '''获取是否能够进入困难副本'''
        info = self._owner.guild.getGuildAttrExt()
        return info.get('kunnan',False)
    
    def getHeroCan(self):
        '''获取是否能够进入英雄副本'''
        info = self._owner.guild.getGuildAttrExt()
        return info.get('yingxion',False)
    
    def getLuckyCan(self):
        '''获取是否能够用幸运石强化'''
        info = self._owner.guild.getGuildAttrExt()
        return info.get('xingyun',False)
    

#===================获取当前等级一级基础属性================================
    def getExpEff(self):
        '''获取经验获取百分比'''
        effectExpEff = self._owner.effect.getEffectInfo().get('ExpEff',0)
        return self._expEff + effectExpEff
    
    def getMallrebate(self):
        '''获取商城折扣'''
        vipzhekou = dbVIP.getVipZhekou(self._owner.baseInfo._viptype)
        zhekou = self._owner.effect.getEffectInfo().get('zhekou',100)
        return 1.0*self._mallrebate*zhekou*vipzhekou/1000000

    def getLevelStr(self):
        '''获取当前等级基础力量'''
        profession = self._owner.profession.getProfession()
        level = self._owner.level.getLevel()
        levelStr = self._baseStr + level*dbaccess.tb_Profession_Config[profession]['perLevelStr']
        return levelStr
    
    def getLevelDex(self):
        '''获取当前等级基础敏捷'''
        profession = self._owner.profession.getProfession()
        level = self._owner.level.getLevel()
        levelDex = self._baseDex + level*dbaccess.tb_Profession_Config[profession]['perLevelDex']
        return levelDex
    
    def getLevelVit(self):
        '''获取当前等级基础耐力'''
        profession = self._owner.profession.getProfession()
        level = self._owner.level.getLevel()
        levelVit = self._baseVit + level*dbaccess.tb_Profession_Config[profession]['perLevelVit']
        return levelVit
    
    def getLevelWis(self):
        '''获取当前等级智力'''
        profession = self._owner.profession.getProfession()
        level = self._owner.level.getLevel()
        levelWis = self._baseWis + level*dbaccess.tb_Profession_Config[profession]['perLevelWis']
        return levelWis
    
    def getLevelSpi(self):
        '''获取当前等级精神'''
        profession = self._owner.profession.getProfession()
        level = self._owner.level.getLevel()
        Profession_Config = dbaccess.tb_Profession_Config[profession]
        levelSpi = self._baseSpi + level*Profession_Config['preLevelSpi']
        return levelSpi

#========================================================
        
    def getHp(self):
        '''获取角色当前血量'''
        if self._hp>self.getMaxHp():
            self.updateHp(self.getMaxHp())
        return self._hp
    
    def setHp(self,hp):
        '''设置角色血量值
        '''
        maxhp = self.getMaxHp()
        if hp>maxhp:
            self._hp = maxhp
        else:
            self._hp = hp
        
    def updateHp(self,hp,state = 1):
        '''更新角色血量值
        '''
        maxhp = self.getMaxHp()
        if hp>maxhp:
            hp = maxhp
        elif hp<0:
            hp=0
        self._hp = hp
        
    def PromptHP(self):
        '''血量提示'''
        if self._hp/(1.0*self.getMaxHp())<0.2:
            tag = 0
            tishiStr = Lg().g(263)
            contentStr = Lg().g(264)
            for itemId in HPDRUG:
                package = self._owner.pack._package._PropsPagePack
                cnt = package.countItemTemplateId(itemId)
                if cnt!=0:
                    caozuoStr = Lg().g(265)
                    sysOpeType = 1
                    tag = 1
                    items = package.getItemTemplateIdPositions(itemId)
                    position = items[0].get('position',0)
                    _item = package.getItemByPosition(position)
                    icon = _item.baseInfo.getItemTemplateInfo()['icon']
                    type = _item.baseInfo.getItemTemplateInfo()['type']
                    curPage,pos = package.getVirtualPostion(position)
                    break
            if not tag:
                icon = 0
                type = 0
                caozuoStr = Lg().g(266)
                pos = 0
                curPage = 0
                sysOpeType = 7
            pushCorpsApplication(self._owner.baseInfo.id, sysOpeType, tishiStr,
                                  contentStr, caozuoStr, pos = pos,curPage = curPage,
                                  icon = icon, type = type)
#            else:
#                args = (self._owner.baseInfo.id,sysOpeType, tishiStr,
#                                  contentStr, caozuoStr, {'pos':pos,'curPage':curPage})
#                self._owner.msgbox.putFightfailmsg(args)
#        dbaccess.updateCharacter(self._owner.baseInfo.id, 'hp', hp)
        
    def addHp(self,hp):
        '''加血'''
        self.updateHp(self.getHp()+hp)
        
    def getMp(self):
        '''获取角色当前魔力值'''
        if self._hp>self.getMaxMp():
            self.updateMp(self.getMaxMp())
        return self._mp
        
    def setMp(self,mp):
        '''设置角色魔力值
        '''
        if self._owner.level.getLevel() == 1 and self._owner.level.getExp()== 0:
            self.updateMp(self.getMaxMp())
        else:
            self._mp = mp
        
    def updateMp(self,mp):
        '''更新角色魔力值
        '''
        maxmp = self.getMaxMp()
        if mp>maxmp:
            mp = maxmp
        elif mp<0:
            mp=0
        self._mp = mp
        dbaccess.updateCharacter(self._owner.baseInfo.id, 'mp', mp)
        
    def addMp(self,mp):
        '''加蓝'''
        self.updateMp(self.getMp()+mp)
        
    def getEnergy(self):
        '''获取角色当前活力值'''
        return self._energy
        
    def setEnergy(self,energy):
        '''设置角色活力
        '''
        self._energy = energy
        
    def updateEnergy(self,energy):
        '''更新角色活力
        '''
        maxEnergy = 200
        if energy>maxEnergy:
            energy = maxEnergy
        elif energy<0:
            energy=0
        self._energy = energy
#        dbaccess.updateCharacter(self._owner.baseInfo.id, 'energy', energy)
        
    def addEnergy(self,energy):
        '''加活力'''
        if energy<0:
            self._owner.schedule.noticeSchedule(11,goal = -energy)#成功后的日程目标通知
        self.updateEnergy(self.getEnergy()+energy)
        
    def getCharacterExtraAttributes(self,keyName):
        '''获取附加属性
        '''
        attribute = 1#self._owner.pack._equipmentSlot.getCharacterExtraAttributes(keyName)
        return attribute
    
#==============================获取当前一级属性==================
    def getCurrentRebound(self):
        '''获取反弹'''
        return 0
        
    def getCurrentPower(self):
        '''获取当前能量'''
        return self._owner.effect.getEffectInfo().get('power',0)
    
###############
    def getCurrentVit(self):
        '''获取当前体质（耐力）= （装备的体质 + Buff效果 + 自身初始体质）* 效果百分比加成
        @param extVitper:  外部因素对属性的变换量
        '''
        effectVit = self._owner.effect.getEffectInfo().get('Vit',0)
        effectvitPercen = self._owner.effect.getEffectInfo().get('VitPercen',0)
        extraVit = self._owner.pack._equipmentSlot.getEquipmentVit()
        perlevelvit = self.getLevelVit()
        return (perlevelvit + extraVit+effectVit)*(effectvitPercen + 1)
    
    def getCurrentStr(self):
        '''获取当前力量
        @param extStrper:  外部因素对属性的变换量
        '''
        effectStr = self._owner.effect.getEffectInfo().get('Str',0)
        effectstrPercen = self._owner.effect.getEffectInfo().get('StrPercen',0) 
        extraStr = self._owner.pack._equipmentSlot.getEquipmentStr()
        perlevelstr = self.getLevelStr()
        return (perlevelstr + extraStr +effectStr)*(1+effectstrPercen)
    
    def getCurrentDex(self):
        '''获取当前灵敏（敏捷）
        @param extDexper:  外部因素对属性的变换量
        '''
        effectDex = self._owner.effect.getEffectInfo().get('Dex',0)
        effectstrPercen = self._owner.effect.getEffectInfo().get('DexPercen',0) 
        extraDex = self._owner.pack._equipmentSlot.getEquipmentDex()
        perlevelstr = self.getLevelDex()
        return (perlevelstr + extraDex + effectDex)*(effectstrPercen + 1)
    
    def getCurrentWis(self):
        '''获取当前智力
        @param extWisper:  外部因素对属性的变换量
        '''
        effectWis = self._owner.effect.getEffectInfo().get('Wis',0)
        effectwisPercen = self._owner.effect.getEffectInfo().get('WisPercen',0) 
        extraDex = self._owner.pack._equipmentSlot.getEquipmentWis()
        perlevelwis = self.getLevelWis()
        return (perlevelwis + extraDex + effectWis)*(effectwisPercen + 1)
    
    def getCurrentSpi(self):
        '''获取当前精神
        @param extSpiper:  外部因素对属性的变换量
        '''
        effectSpi = self._owner.effect.getEffectInfo().get('Spi',0)
        effectspiPercen = self._owner.effect.getEffectInfo().get('SpiPercen',0) 
        extraDex = self._owner.pack._equipmentSlot.getEquipmentSpi()
        perlevelspi = self.getLevelSpi()
        return (perlevelspi + extraDex + effectSpi) * (effectspiPercen +1)
    
#==================获取当前二级属性=======================
    
    def getMaxHp(self,preDict = {'extVitper':0,'extStrper':0,
                                 'extDexper':0,'extWisper':0,'extSpiper':0}):
        '''
                    计算当前最大HP
        '''
        effectMaxHp = self._owner.effect.getEffectInfo().get('MaxHp',0)
        effectMaxHpPercen = self._owner.effect.getEffectInfo().get('MaxHpPercen',0) 
        profession = self._owner.profession.getProfession()
        perHPVit = dbaccess.tb_Profession_Config[profession].get('perHPVit')
        extHpAdditional = self._owner.pack._equipmentSlot.getEquipmentMaxHp()
        extVitper = preDict.get('extVitper',0)
        currentVit = self.getCurrentVit()+ extVitper
        maxHp = (currentVit*perHPVit + \
                 effectMaxHp+extHpAdditional)*(effectMaxHpPercen +1)
        return int(maxHp)
        
#    def getMaxMp(self,preDict = {'extVitper':0,'extStrper':0,
#                                 'extDexper':0,'extWisper':0,'extSpiper':0}):
#        '''
#                    计算当前最大MP
#                    法力=(基础法力+(等级)*每级成长值)*(1+附加法力%)*(1+体质*0.01)+附加法力值
#        '''
#        effectMaxMp = self._owner.effect.getEffectInfo().get('MaxMp',0)
#        effectMaxMpPercen = self._owner.effect.getEffectInfo().get('MaxMpPercen',0) 
#        profession = self._owner.profession.getProfession()
#        perMPSpi = dbaccess.tb_Profession_Config[profession].get('perMPSpi')
#        extMpAdditional = self._owner.pack._equipmentSlot.getEquipmentMaxMp()
#        maxMp = (self.getCurrentSpi()*perMPSpi + effectMaxMp+\
#                 extMpAdditional)*(effectMaxMpPercen+1)
#        return maxMp
    
    def getCurrPhyAtt(self,preDict = {'extVitper':0,'extStrper':0,
                                 'extDexper':0,'extWisper':0,'extSpiper':0}):
        '''获取当前物理攻击'''
        effectPhyAtt = self._owner.effect.getEffectInfo().get('PhyAtt',0)
        effectPhyAttPercen = self._owner.effect.getEffectInfo().get('PhyAttPercen',0) 
        equipPhyAtt = self._owner.pack._equipmentSlot.getEquipmentPhyAtt()
        profession = self._owner.profession.getProfession()
        perPhyAttStr = dbaccess.tb_Profession_Config[profession].get('perPhyAttStr')
        extStrper = preDict.get('extStrper',0)
        CurrentStr = self.getCurrentStr()+extStrper
        PhyAtt = CurrentStr*perPhyAttStr + equipPhyAtt
        return (PhyAtt + effectPhyAtt)*(effectPhyAttPercen+1)
    
    def getCurrPhyDef(self,preDict = {'extVitper':0,'extStrper':0,
                                 'extDexper':0,'extWisper':0,'extSpiper':0}):
        '''获取当前物理防御'''
        effectPhyDef = self._owner.effect.getEffectInfo().get('PhyDef',0)
        effectPhyDefPercen = self._owner.effect.getEffectInfo().get('PhyDefPercen',0) 
        equipPhyDef = self._owner.pack._equipmentSlot.getEquipmentPhyDef()
        profession = self._owner.profession.getProfession()
        perPhyDefStr = dbaccess.tb_Profession_Config[profession].get('perPhyDefVit')
        perPhyDefVit = dbaccess.tb_Profession_Config[profession].get('perPhyDefVit')
        extStrper = preDict.get('extStrper',0)
        extVitper = preDict.get('extVitper',0)
        CurrentStr = self.getCurrentStr()+ extStrper
        CurrentVit = self.getCurrentVit()+extVitper
        PhyDef = CurrentVit*perPhyDefVit + CurrentStr*perPhyDefStr + equipPhyDef
        return (PhyDef + effectPhyDef)*(effectPhyDefPercen+1)
    
    def getCurrMigAtt(self,preDict = {'extVitper':0,'extStrper':0,
                                 'extDexper':0,'extWisper':0,'extSpiper':0}):
        '''获取当前魔法攻击'''
        effectMigAtt = self._owner.effect.getEffectInfo().get('MigAtt',0)
        effectMigAttPercen = self._owner.effect.getEffectInfo().get('MigAttPercen',0)
        equipMigAtt = self._owner.pack._equipmentSlot.getEquipmentMigAtt()
        profession = self._owner.profession.getProfession()
        perMigAttWis = dbaccess.tb_Profession_Config[profession].get('perMigAttWis')
        extWisper = preDict.get('extWisper',0)
        CurrentWis = self.getCurrentWis()+extWisper
        MigAtt = (CurrentWis*perMigAttWis + equipMigAtt +\
                   effectMigAtt)*(effectMigAttPercen+1)
        return MigAtt+5
    
    def getCurrMigDef(self,preDict = {'extVitper':0,'extStrper':0,
                                 'extDexper':0,'extWisper':0,'extSpiper':0}):
        '''获取当前魔法防御'''
        effectMigDef = self._owner.effect.getEffectInfo().get('MigDef',0)
        effectMigDefPercen = self._owner.effect.getEffectInfo().get('MigDefPercen',0)
        equipMigDef = self._owner.pack._equipmentSlot.getEquipmentMigDef()
        profession = self._owner.profession.getProfession()
        perMigDefWis = dbaccess.tb_Profession_Config[profession].get('perMigDefWis')
        perMigDefVit = dbaccess.tb_Profession_Config[profession].get('perMigDefVit')
        extWisper = preDict.get('extWisper',0)
        extVitper = preDict.get('extVitper',0)
        CurrentWis = self.getCurrentWis()+extWisper
        CurrentVit = self.getCurrentVit()+extVitper
        MigDef = CurrentWis*perMigDefWis+ CurrentVit*perMigDefVit + equipMigDef 
        return (MigDef +effectMigDef)*(effectMigDefPercen + 1)
    
    def getCurrHitRate(self,preDict = {'extVitper':0,'extStrper':0,
                                 'extDexper':0,'extWisper':0,'extSpiper':0}):
        '''获取当前命中'''
        effectHitRate = self._owner.effect.getEffectInfo().get('HitRate',0)
        equipHitRate = self._owner.pack._equipmentSlot.getEquipmentHitRate()
        HitRate = 100 + equipHitRate
        return HitRate*(1+effectHitRate*0.01)
    
    def getCurrDodge(self,preDict = {'extVitper':0,'extStrper':0,
                                 'extDexper':0,'extWisper':0,'extSpiper':0}):
        '''获取当前闪避'''
        effectDodge = self._owner.effect.getEffectInfo().get('Dodge',0)
        equipDodge = self._owner.pack._equipmentSlot.getEquipmentDodge()
        Dodge = equipDodge
        return Dodge*(1+ effectDodge*0.01)
    
    def getCurrCriRate(self,preDict = {'extVitper':0,'extStrper':0,
                                 'extDexper':0,'extWisper':0,'extSpiper':0}):
        '''获取当前暴击'''
        effectCriRate = self._owner.effect.getEffectInfo().get('CriRate',0)
        equipCriRate = self._owner.pack._equipmentSlot.getEquipmentCriRate()
        CriRate = 5 + equipCriRate
        return CriRate + effectCriRate
    
    def getCurrSpeed(self,preDict = {'extVitper':0,'extStrper':0,
                                 'extDexper':0,'extWisper':0,'extSpiper':0}):
        '''获取当前攻速'''
        effectSpeed = self._owner.effect.getEffectInfo().get('Speed',0)
        profession = self._owner.profession.getProfession()
        perSpeedDex = dbaccess.tb_Profession_Config[profession].get('perSpeedDex',0)
        perSpeedWis = dbaccess.tb_Profession_Config[profession].get('perSpeedWis',0)
        equipSpeed = self._owner.pack._equipmentSlot.getEquipmentSpeed()
        extDexper = preDict.get('extDexper',0)
        extWisper = preDict.get('extWisper',0)
        CurrentDex = self.getCurrentDex()+extDexper
        CurrentWis = self.getCurrentWis()+extWisper
        Speed = CurrentDex*perSpeedDex + CurrentWis*perSpeedWis
        return Speed + effectSpeed +equipSpeed
    
    def getCurrSquelch(self,preDict = {'extVitper':0,'extStrper':0,
                                 'extDexper':0,'extWisper':0,'extSpiper':0}):
        '''获取角色的当前反击'''
        effectSquelch = self._owner.effect.getEffectInfo().get('Squelch',0)
        equipSquelch = self._owner.pack._equipmentSlot.getEquipmentSquelch()
        squelch = equipSquelch
        return squelch + effectSquelch
    
    def getCurrIgnore(self,preDict = {'extVitper':0,'extStrper':0,
                                 'extDexper':0,'extWisper':0,'extSpiper':0}):
        '''获取角色的破甲属性'''
        effectIgnore = self._owner.effect.getEffectInfo().get('Ignore',0)
        equipBogey = self._owner.pack._equipmentSlot.getEquipmentBogey()
        ignore = equipBogey
        return ignore + effectIgnore
    
#=====================国属性的加成============================
    def getGuildStr(self):
        '''获取国力量的加成
        '''
        info = self._owner.guild.getGuildAttrExt()
        return info.get('str',0)
    
    def getGuildDex(self):
        '''获取国敏捷的加成
        '''
        info = self._owner.guild.getGuildAttrExt()
        return info.get('dex',0)
    
    def getGuildWis(self):
        '''获取国智力的加成
        '''
        info = self._owner.guild.getGuildAttrExt()
        return info.get('wis',0)
    
    def getGuildSpi(self):
        '''获取国精神的加成
        '''
        info = self._owner.guild.getGuildAttrExt()
        return info.get('spi',0)
    
    def getGuildVit(self):
        '''获取国耐力的加成
        '''
        info = self._owner.guild.getGuildAttrExt()
        return info.get('vit',0)
    
    def getGuildPhyAtt(self):
        '''获取国物攻的加成
        '''
        info = self._owner.guild.getGuildAttrExt()
        profession = self._owner.profession.getProfession()
        perPhyAttStr = dbaccess.tb_Profession_Config[profession].get('perPhyAttStr')
        perPhyAttDex = dbaccess.tb_Profession_Config[profession].get('perPhyAttDex')
        return info.get('phyatt',0)+perPhyAttStr*info.get('str',0)+perPhyAttDex*info.get('dex',0)
    
    def getGuildMigAtt(self):
        '''获取国魔攻的加成
        '''
        info = self._owner.guild.getGuildAttrExt()
        profession = self._owner.profession.getProfession()
        perMigAttWis = dbaccess.tb_Profession_Config[profession].get('perMigAttWis')
        return info.get('migatt',0)+perMigAttWis*info.get('vit',0)
    
        
#=================================================================

    def getRestNum(self):
        '''获取休息的次数'''
        result = dbaccess.getRestNum(self._owner.baseInfo.id)
        NumList={}
        NumList['nap'] = 1 - int(result[2])
        NumList['lightSleep'] = 1 - int(result[3])
        NumList['peacefulSleep'] = 1 - int(result[4])
        NumList['spoor'] = 2 - int(result[5])
        return NumList
        
    def doRest(self,ttype,payType,payNum):
        '''宿屋休息'''
        pid = self._owner.baseInfo.id
        profession = self._owner.profession.getProfession()
        level = self._owner.level.getLevel()
        coin = self._owner.finance.getCoin()
        gold = self._owner.finance.getGold()
        coupon = self._owner.finance.getCoupon()
        hp = self.getHp()
        mp = self.getMp()
        energy = self.getEnergy()
        count = 0

        restRecord = dbaccess.getPlayerRestRecord(pid)
        if ttype == 'meal':#用餐
            hp = self.getMaxHp(profession, pid, level)
            mp = self.getMaxMp(profession, pid, level)
            coin -= payNum
            if coin < 0:
                return {'result':False, 'message':Lg().g(267)}
            count = -1
            dbaccess.updatePlayerInfo(pid, {'hp':hp, 'mp':mp, 'coin':coin})
        elif ttype == 'nap':#小憩
            energyDelta = payNum
            result = self._doSleep(2, payType, payNum, energy, energyDelta, gold, coupon, restRecord, ttype)
            if not result['result']:
                return result
            gold = result['data']['gold']
            coupon = result['data']['coupon']
            energy = result['data']['energy']
            count = 1 - (int(restRecord[2]) + 1)
            dbaccess.updatePlayerRestRecord(pid, {'napCount':restRecord[2] + 1})
        elif ttype == 'lightSleep':#浅睡
            energyDelta = payNum
            result = self._doSleep(3, payType, payNum, energy, energyDelta, gold, coupon, restRecord, ttype)
            if not result['result']:
                return result
            gold = result['data']['gold']
            coupon = result['data']['coupon']
            energy = result['data']['energy']
            count = 1 - (int(restRecord[3]) + 1)
            dbaccess.updatePlayerRestRecord(pid, {'lightSleepCount':restRecord[3] + 1})
        elif ttype == 'peacefulSleep':#安眠
            energyDelta = payNum
            result = self._doSleep(4, payType, payNum, energy, energyDelta, gold, coupon, restRecord, ttype)
            if not result['result']:
                return result
            gold = result['data']['gold']
            coupon = result['data']['coupon']
            energy = result['data']['energy']
            count = 1 - (int(restRecord[4]) + 1)
            dbaccess.updatePlayerRestRecord(pid, {'peacefulSleepCount':restRecord[4] + 1})
        elif ttype == 'spoor':#酣睡
            energyDelta = payNum
            result = self._doSleep(5, payType, payNum, energy, energyDelta, gold, coupon, restRecord, ttype)
            if not result['result']:
                return result
            gold = result['data']['gold']
            coupon = result['data']['coupon']
            energy = result['data']['energy']
            count = 2 - (int(restRecord[5]) + 1)
            dbaccess.updatePlayerRestRecord(pid, {'spoorCount':restRecord[5] + 1})

        self.setHp(hp)
        self.setMp(mp)
        self.setEnergy(energy)
        self._owner.finance.setCoin(coin)
        self._owner.finance.setGold(gold)
        self._owner.finance.setCoupon(coupon)

        return {'result':True, 'data':{'hp':hp, 'mp':mp, 'energy':energy, 'gold':gold, \
                                      'coupon':coupon, 'coin':coin, 'type':ttype, 'count':count}}

    def _doSleep(self, index, payType, payNum, energy, energyDelta, gold, coupon, restRecord, ttype):
        pid = self._owner.baseInfo.id
        if payType == 'gold':
            gold -= payNum
            if gold < 0:
                return {'result':False, 'message':u'您的黄金量不足'}
            if ttype == 'spoor':
                if restRecord[index] >= 2:
                    return {'result':False, 'message':u'您今天不能此操作'}
            else:
                if restRecord[index] >= 1:
                    return {'result':False, 'message':u'您今天不能此操作'}
            energy += energyDelta
            if energy > 200:
                return {'result':False, 'message':u'您的活力已达上限'}
            dbaccess.updatePlayerInfo(pid, {'energy':energy, 'gold':gold})
        else:
            coupon -= payNum
            if coupon < 0:
                return {'result':False, 'message':u'您的礼券量不足'}
            energy += energyDelta
            if energy > 200:
                return {'result':False, 'message':u'您的活力已达上限'}
            dbaccess.updatePlayerInfo(pid, {'energy':energy, 'coupon':coupon})
        return {'result':True, 'data':{'gold':gold, 'coupon':coupon, 'energy':energy}}
        
        
    
        
        