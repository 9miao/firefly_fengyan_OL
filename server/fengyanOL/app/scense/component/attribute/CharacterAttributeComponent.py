#coding:utf8
'''
Created on 2012-5-14

@author: Administrator
'''
from app.scense.utils import dbaccess
from app.scense.utils.dbopera import dbVIP
from app.scense.component.Component import Component
from app.scense.netInterface.pushObjectNetInterface import pushCorpsApplication
from app.scense.netInterface.pushPrompted import pushPromptedMessageByCharacter
from app.scense.core.language.Language import Lg

HPDRUG = [20000000,20000001,20000002]


class CharacterAttributeComponent(Component):
    MAXENERGY = 200
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
#        self._baseSpi = 0    #基础精神点
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
        elif hp<=0:
            hp=1
        self._hp = hp
        
    def PromptHP(self):
        '''血量提示'''
        if self._hp/(1.0*self.getMaxHp())<0.5:
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
                    itype = _item.baseInfo.getItemTemplateInfo()['type']
                    curPage,pos = package.getVirtualPostion(position)
                    break
            if not tag:
                icon = 0
                itype = 0
                caozuoStr = Lg().g(266)
                pos = 0
                curPage = 0
                sysOpeType = 7
            pushCorpsApplication(self._owner.baseInfo.id, sysOpeType, tishiStr,
                                  contentStr, caozuoStr, pos = pos,curPage = curPage,
                                  icon = icon, type = itype)
        
    def addHp(self,hp):
        '''加血'''
        self.updateHp(self.getHp()+hp)
        
    def Restoration(self):
        '''恢复角色满状态
        '''
        self.setHp(self.getMaxHp())
        
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
        if energy>200:
            self._energy = 200
        else:
            self._energy = energy
        
    def updateEnergy(self,energy):
        '''更新角色活力
        '''
        maxEnergy = self.MAXENERGY
        if energy>maxEnergy:
            energy = maxEnergy
        elif energy<0:
            energy=0
        self._energy = energy
        self._owner.pushInfoChanged()
        
    def addEnergy(self,energy):
        '''加活力'''
        if energy>0:
            msg=Lg().g(268)%energy
            pushPromptedMessageByCharacter(msg,[self._owner.baseInfo.getId()])
        self.updateEnergy(self.getEnergy()+energy)
        
    def getCharacterExtraAttributes(self,keyName):
        '''获取附加属性
        '''
        attribute = 1#self._owner.pack._equipmentSlot.getCharacterExtraAttributes(keyName)
        return attribute
    
#==============================获取当前一级属性==================
#    def getCurrentRebound(self):
#        '''获取反弹'''
#        return 0
#        
#    def getCurrentPower(self):
#        '''获取当前能量'''
#        return self._owner.effect.getEffectInfo().get('power',0)
#    
################
#    def getCurrentVit(self):
#        '''获取当前体质（耐力）= （装备的体质 + Buff效果 + 自身初始体质）* 效果百分比加成
#        @param extVitper:  外部因素对属性的变换量
#        '''
#        effectVit = self._owner.effect.getEffectInfo().get('Vit',0)
#        effectvitPercen = self._owner.effect.getEffectInfo().get('VitPercen',0)
#        extraVit = self._owner.pack._equipmentSlot.getEquipmentVit()
#        perlevelvit = self.getLevelVit()
#        return (perlevelvit + extraVit+effectVit)*(effectvitPercen + 1)
#    
#    def getCurrentStr(self):
#        '''获取当前力量
#        @param extStrper:  外部因素对属性的变换量
#        '''
#        effectStr = self._owner.effect.getEffectInfo().get('Str',0)
#        effectstrPercen = self._owner.effect.getEffectInfo().get('StrPercen',0) 
#        extraStr = self._owner.pack._equipmentSlot.getEquipmentStr()
#        perlevelstr = self.getLevelStr()
#        return (perlevelstr + extraStr +effectStr)*(1+effectstrPercen)
#    
#    def getCurrentDex(self):
#        '''获取当前灵敏（敏捷）
#        @param extDexper:  外部因素对属性的变换量
#        '''
#        effectDex = self._owner.effect.getEffectInfo().get('Dex',0)
#        effectstrPercen = self._owner.effect.getEffectInfo().get('DexPercen',0) 
#        extraDex = self._owner.pack._equipmentSlot.getEquipmentDex()
#        perlevelstr = self.getLevelDex()
#        return (perlevelstr + extraDex + effectDex)*(effectstrPercen + 1)
#    
#    def getCurrentWis(self):
#        '''获取当前智力
#        @param extWisper:  外部因素对属性的变换量
#        '''
#        effectWis = self._owner.effect.getEffectInfo().get('Wis',0)
#        effectwisPercen = self._owner.effect.getEffectInfo().get('WisPercen',0) 
#        extraDex = self._owner.pack._equipmentSlot.getEquipmentWis()
#        perlevelwis = self.getLevelWis()
#        return (perlevelwis + extraDex + effectWis)*(effectwisPercen + 1)
    
#    def getCurrentSpi(self):
#        '''获取当前精神
#        @param extSpiper:  外部因素对属性的变换量
#        '''
#        effectSpi = self._owner.effect.getEffectInfo().get('Spi',0)
#        effectspiPercen = self._owner.effect.getEffectInfo().get('SpiPercen',0) 
#        extraDex = self._owner.pack._equipmentSlot.getEquipmentSpi()
#        perlevelspi = self.getLevelSpi()
#        return (perlevelspi + extraDex + effectSpi) * (effectspiPercen +1)
    
#==================获取当前二级属性=======================
    
    def getMaxHp(self,preDict = {'extVitper':0,'extStrper':0,
                                 'extDexper':0,'extWisper':0,'extSpiper':0}):
        '''
                    计算当前最大HP
        '''
        EquipAttr = self._owner.pack._equipmentSlot.getAllEquipttributes()#所有装备的属性效果（包括套装）
        EffectAttr = self._owner.effect.getEffectInfo()#所有Buff的属性效果
        GodHead = self._owner.godhead.getGodheadAttribute()#所有神格属性加成
        GuildAttr = self._owner.guild.getGuildAttrExt()
        profession = self._owner.profession.getProfession()
        attrper = dbaccess.tb_Profession_Config[profession]
        fateattrs = self._owner.fate.getAllFateAttr()
        nobilityAttr = self._owner.nobility.getAttribute()
        baseVit = self.getLevelVit()+EquipAttr.get('Vit',0)+EffectAttr.get('Vit',0)+\
                  GodHead.get('Vit',0)+GuildAttr.get('Vit',0)+preDict.get('extVitper')+\
                  fateattrs.get('Vit',0)+nobilityAttr.get('Vit',0)
        nowVit = int(baseVit*(1+EquipAttr.get('VitPercen',0)+\
                              EffectAttr.get('VitPercen',0))+GodHead.get('VitPercen',0)+fateattrs.get('VitPercen',0))
        baseMaxHp = int(nowVit*attrper.get('perHPVit',1)+\
                        EquipAttr.get('MaxHp',0)+EffectAttr.get('MaxHp',0)+GodHead.get('MaxHp',0))+\
                        nobilityAttr.get('MaxHp',0)+fateattrs.get('MaxHp',0)
        MaxHp = int(baseMaxHp*(1+EquipAttr.get('MaxHpPercen',0)+\
                               EffectAttr.get('MaxHpPercen',0)+GodHead.get('MaxHpPercen',0)+\
                               nobilityAttr.get('MaxHpPercen',0)+fateattrs.get('MaxHpPercen',0)))
        return MaxHp
    
    def getCharacterAttr(self,preDict = {'extVitper':0,'extStrper':0,
                                 'extDexper':0,'extWisper':0,'extSpiper':0}):
        '''获取角色的所有属性
        '''
        EquipAttr = self._owner.pack._equipmentSlot.getAllEquipttributes()#所有装备的属性效果（包括套装）
        EffectAttr = self._owner.effect.getEffectInfo()#所有Buff的属性效果
        GodHead = self._owner.godhead.getGodheadAttribute()#所有神格属性加成
        GuildAttr = self._owner.guild.getGuildAttrExt()#国加成
        profession = self._owner.profession.getProfession()
        attrper = dbaccess.tb_Profession_Config[profession]
        fateattrs = self._owner.fate.getAllFateAttr()
        nobilityAttr = self._owner.nobility.getAttribute()
        info = {}
        baseStr = self.getLevelStr()+EquipAttr.get('Str',0)+EffectAttr.get('Str',0)+\
                  GodHead.get('Str',0)+GuildAttr.get('Str',0)+preDict.get('extStrper')+\
                  fateattrs.get('Str',0)+nobilityAttr.get('Str',0)
        baseDex = self.getLevelDex()+EquipAttr.get('Dex',0)+EffectAttr.get('Dex',0)+\
                  GodHead.get('Dex',0)+GuildAttr.get('Dex',0)+preDict.get('extDexper')+\
                  fateattrs.get('Dex',0)+nobilityAttr.get('Dex',0)
        baseVit = self.getLevelVit()+EquipAttr.get('Vit',0)+EffectAttr.get('Vit',0)+\
                  GodHead.get('Vit',0)+GuildAttr.get('Vit',0)+preDict.get('extVitper')+\
                  fateattrs.get('Vit',0)+nobilityAttr.get('Vit',0)
        baseWis = self.getLevelWis()+EquipAttr.get('Wis',0)+EffectAttr.get('Wis',0)+\
                  GodHead.get('Wis',0)+GuildAttr.get('Wis',0)+preDict.get('extWisper')+\
                  fateattrs.get('Wis',0)+nobilityAttr.get('Wis',0)
        #一级属性
        info['Str'] = int(baseStr*(1+EquipAttr.get('StrPercen',0)+\
                                   EffectAttr.get('StrPercen',0)+ GodHead.get('StrPercen',0)+\
                                   fateattrs.get('StrPercen',0)+nobilityAttr.get('StrPercen',0)))
        info['Dex'] = int(baseDex*(1+EquipAttr.get('DexPercen',0)+\
                                   EffectAttr.get('DexPercen',0)+ GodHead.get('DexPercen',0)+\
                                   fateattrs.get('DexPercen',0)+nobilityAttr.get('DexPercen',0)))
        info['Vit'] = int(baseVit*(1+EquipAttr.get('VitPercen',0)+\
                                   EffectAttr.get('VitPercen',0)+ GodHead.get('VitPercen',0)+\
                                   fateattrs.get('VitPercen',0)+nobilityAttr.get('VitPercen',0)))
        info['Wis'] = int(baseWis*(1+EquipAttr.get('WisPercen',0)+\
                                   EffectAttr.get('WisPercen',0)+ GodHead.get('WisPercen',0)+\
                                   fateattrs.get('WisPercen',0)+nobilityAttr.get('WisPercen',0)))
        #过渡参数
        baseMaxHp = int(info['Vit']*attrper.get('perHPVit',1)+\
                        EquipAttr.get('MaxHp',0)+\
                        EffectAttr.get('MaxHp',0)+ \
                        GodHead.get('MaxHp',0)+fateattrs.get('MaxHp',0)+nobilityAttr.get('MaxHp',0))
        basePhyAtt = int(info['Str']*attrper.get('perPhyAttStr',1)+\
                         EquipAttr.get('PhyAtt',0)+\
                         EffectAttr.get('PhyAtt',0)+ \
                         GodHead.get('PhyAtt',0)+fateattrs.get('PhyAtt',0)+nobilityAttr.get('PhyAtt',0))
        basePhyDef = int(info['Str']*attrper.get('perPhyDefStr',1)+\
                         info['Vit']*attrper.get('perPhyDefVit',1)+\
                         EquipAttr.get('PhyDef',0)+\
                         EffectAttr.get('PhyDef',0)+\
                         GodHead.get('PhyDef',0)+fateattrs.get('PhyDef',0)+nobilityAttr.get('PhyDef',0))
        baseMigAtt = int(info['Wis']*attrper.get('perMigAttWis',1)+\
                         EquipAttr.get('MigAtt',0)+\
                         EffectAttr.get('MigAtt',0)+\
                         GodHead.get('MigAtt',0)+fateattrs.get('MigAtt',0)+nobilityAttr.get('MigAtt',0))
        baseMigDef = int(info['Wis']*attrper.get('perMigDefWis',1)+\
                         info['Vit']*attrper.get('perMigDefVit',1)+\
                         EquipAttr.get('MigDef',0)+\
                         EffectAttr.get('MigDef',0)+\
                         GodHead.get('MigDef',0)+fateattrs.get('MigDef',0)+nobilityAttr.get('MigDef',0))
        #二级属性
        info['MaxHp'] = int(baseMaxHp*(1+EquipAttr.get('MaxHpPercen',0)+\
                                       EffectAttr.get('MaxHpPercen',0)+\
                                       +fateattrs.get('MaxHpPercen',0)+nobilityAttr.get('MaxHpPercen',0)))
        info['power'] = 50+EquipAttr.get('power',0) + EffectAttr.get('power',0)\
                                       +fateattrs.get('power',0)+nobilityAttr.get('power',0)
        info['PhyAtt'] = int(basePhyAtt*(1+EquipAttr.get('PhyAttPercen',0)+\
                                         EffectAttr.get('PhyAttPercen',0)+\
                                         GodHead.get('PhyAttPercen',0)+\
                                         fateattrs.get('PhyAttPercen',0)+nobilityAttr.get('PhyAttPercen',0)))
        info['PhyDef'] = int(basePhyDef*(1+EquipAttr.get('PhyDefPercen',0)+\
                                         EffectAttr.get('PhyDefPercen',0)+\
                                         GodHead.get('PhyDefPercen',0)+\
                                         fateattrs.get('PhyDefPercen',0)+nobilityAttr.get('PhyDefPercen',0)))
        info['MigAtt'] = int(baseMigAtt*(1+EquipAttr.get('MigAttPercen',0)+\
                                         EffectAttr.get('MigAttPercen',0)+\
                                         GodHead.get('MigAttPercen',0)+\
                                         fateattrs.get('MigAttPercen',0)+nobilityAttr.get('MigAttPercen',0)))
        info['MigDef'] = int(baseMigDef*(1+EquipAttr.get('MigDefPercen',0)+\
                                         EffectAttr.get('MigDefPercen',0)+\
                                         GodHead.get('MigDefPercen',0)+\
                                         fateattrs.get('MigDefPercen',0)+nobilityAttr.get('MigDefPercen',0)))
        info['HitRate'] = 100 + EquipAttr.get('HitRate',0)+\
                        EffectAttr.get('HitRate',0)+GodHead.get('HitRate',0)+\
                        fateattrs.get('HitRate',0)+nobilityAttr.get('HitRate',0)
        info['Dodge'] = EquipAttr.get('Dodge',0)+EffectAttr.get('Dodge',0)\
                                        +GodHead.get('Dodge',0)+\
                                        fateattrs.get('Dodge',0)+nobilityAttr.get('Dodge',0)
        info['CriRate'] = 5 + EquipAttr.get('CriRate',0)+EffectAttr.get('CriRate',0)\
                                        +GodHead.get('CriRate',0)+\
                                        fateattrs.get('CriRate',0)+nobilityAttr.get('CriRate',0)
        info['Speed'] = int(info['Dex']*attrper.get('perSpeedDex',1) +\
                            EquipAttr.get('Speed',0)+EffectAttr.get('Speed',0))\
                            +GodHead.get('Speed',0)+fateattrs.get('Speed',0)+nobilityAttr.get('Speed',0)
        info['Block'] = EquipAttr.get('Block',0)+EffectAttr.get('Block',0)\
                            +GodHead.get('Block',0)+fateattrs.get('Block',0)+nobilityAttr.get('Block',0)
        return info
    
#=====================国属性的加成============================
    def getGuildStr(self):
        '''获取国力量的加成
        '''
        info = self._owner.guild.getGuildAttrExt()
        return info.get('Str',0)
    
    def getGuildDex(self):
        '''获取国敏捷的加成
        '''
        info = self._owner.guild.getGuildAttrExt()
        return info.get('Dex',0)
    
    def getGuildWis(self):
        '''获取国智力的加成
        '''
        info = self._owner.guild.getGuildAttrExt()
        return info.get('Wis',0)
    
    def getGuildVit(self):
        '''获取国耐力的加成
        '''
        info = self._owner.guild.getGuildAttrExt()
        return info.get('Vit',0)
    
    def getGuildPhyAtt(self):
        '''获取国物攻的加成
        '''
        info = self._owner.guild.getGuildAttrExt()
        profession = self._owner.profession.getProfession()
        perPhyAttStr = dbaccess.tb_Profession_Config[profession].get('perPhyAttStr')
        return info.get('PhyAtt',0)+perPhyAttStr*info.get('Str',0)
    
    def getGuildMigAtt(self):
        '''获取国魔攻的加成
        '''
        info = self._owner.guild.getGuildAttrExt()
        profession = self._owner.profession.getProfession()
        perMigAttWis = dbaccess.tb_Profession_Config[profession].get('perMigAttWis')
        return info.get('MigAtt',0)+perMigAttWis*info.get('Wis',0)
    
    
        
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
        
        