#coding:utf8
'''
Created on 2012-6-7

@author: Administrator
'''
from app.scense.component.Component import Component
from app.scense.component.fate.Fate import Fate
import datetime,random
from app.scense.utils.dbopera import dbCharacterFate
from app.scense.util.gs import addDict

from app.scense.netInterface.pushObjectNetInterface import pushOtherMessage
from app.scense.core.language.Language import Lg

FATERATE = {0:1000,1:683,2:203,3:108,4:37,5:0}
LEVELNAME = {1:Lg().g(290),2:Lg().g(291),3:Lg().g(292),4:Lg().g(293),5:Lg().g(294)}
ZHANXING_CONFIG_CONS = {1:10000,2:20000,3:30000,4:50000,5:100000}
MAXOUTSIDE = 18
MAXPACK = 20

def choiceFate(fatelevel):
    '''随机获取星运
    '''
    quality = 0
    if fatelevel ==1:
        rate = random.randint(1,100)
        if rate<=70:
            quality=0
        elif 70<rate<=98:
            quality=2
        else:
            quality=3
    elif fatelevel==2:
        rate = random.randint(1,100)
        if rate<=75:
            quality=0
        elif 75<rate<=98:
            quality=2
        elif 98<rate<=99:
            quality=3
        else:
            quality=4
    elif fatelevel==3:
        rate = random.randint(1,100)
        if rate<=80:
            quality=0
        elif 80<rate<=90:
            quality=2
        elif 90<rate<=95:
            quality=3
        elif 95<rate<=99:
            quality=4
        else:
            quality=5
    elif fatelevel==4:
        rate = random.randint(1,100)
        if rate<=70:
            quality=0
        elif 70<rate<=75:
            quality=2
        elif 75<rate<=90:
            quality=3
        elif 90<rate<=95:
            quality=4
        elif 95<rate<=99:
            quality=5
        else:
            quality=6
    elif fatelevel==5:
        rate = random.randint(1,100)
        if rate<=20:
            quality=3
        elif 20<rate<=80:
            quality=4
        elif 80<rate<=85:
            quality=5
        elif 85<rate<=99:
            quality=6
        else:
            quality=7
    else:
        quality = 0
    choicelist = dbCharacterFate.FATE_GROUP.get(quality,[])
    if not choicelist:
        fateId = random.choice(dbCharacterFate.FATE_TEMPLATE.keys())
    else:
        fateId = random.choice(choicelist)
    return fateId
    

class CharacterFateComponent(Component):
    '''角色命格信息
    '''
    
    def __init__(self,owner):
        '''初始化
        '''
        Component.__init__(self, owner)
        self.fates = {}#角色所有的命格
        self.outside = []#未拾取的命格
        self.fatepack = {}#命格包裹
        self.equiped = {}#已经装备的命格
        self.score = 0#命格积分
        self.fateLevel = 1#当前可使用的高等级占星等级
        self.freedate = datetime.date(2012,6,6)#上次使用免费的日期
        self.freetimes = 0#已经使用的免费次数
        self.initData()
        
    def initData(self):
        '''初始化角色的命格信息'''
        characterId = self._owner.baseInfo.id
        data = dbCharacterFate.getCharacterFate(characterId)#获取角色所有的命格
        settingdate = dbCharacterFate.getCharacterFateSetting(characterId)#获取角色占星相关信息
        if settingdate:
            self.score = settingdate['score']
            self.freetimes = settingdate['freetimes']
            self.freedate = settingdate['freedate']
            self.fateLevel = settingdate['fateLevel']
        else:#没有的话插入角色命格相关信息表
            dbCharacterFate.insertCharacterFateSetting(characterId)
        for fateInfo in data:
            fate = Fate(insData = fateInfo)
            self.fates[fate.id] = fate
            if fateInfo['equip'] ==-2:#未拾取的命格
                self.outside.append(fate.id)
            elif fateInfo['equip'] ==-1:#包裹中的命格
                self.fatepack[fateInfo['position']] = fate.id
            elif fateInfo['equip'] ==0:#角色装备的命格
                self.equiped[fateInfo['position']] = fate.id
            else:#宠物装备的命格
                pet = self._owner.pet.getPet(fateInfo['equip'])
                if not pet:
                    continue
                pet.updateFate(fateInfo['position'],fate.id)
                
    def iszbfw(self):
        '''是否已经装备符文'''
        if len(self.equiped)>0:
            return True
        return False
                
    def addFate(self,templateId):
        '''获得一个命格
        @param templateId: int 命格的模板ID
        '''
        fate = Fate(templateId = templateId)
        characterId = self._owner.baseInfo.id
        fate.InsertIntoDB(characterId)
        self.fates[fate.id] = fate
        self.outside.append(fate.id)
        return fate.id
        
    def planFateLevel(self,fatelevel):
        '''计算下次占星的可使用的最高等级'''
        ratelow = FATERATE.get(fatelevel)
        ratehigh = FATERATE.get(fatelevel-1)
        rate = random.randint(0,1000)
        if rate < ratelow:
            self.fateLevel +=1
        elif ratehigh>rate>ratelow:
            self.fateLevel = fatelevel
        else:
            self.fateLevel = 1
    
    def ZhanXing(self,fatelevel):
        '''开始占星
        '''
        dynamicId = self._owner.dynamicId
        if self._owner.level.getLevel()<16:#功能等级开放限制
            msg = Lg().g(295)
            pushOtherMessage(905, msg, [dynamicId])
            return {'result':False,'message':msg}
        if fatelevel>1 and self.fateLevel!=fatelevel:
            msg = Lg().g(296)
            pushOtherMessage(905, msg, [dynamicId])
            return {'result':False,'message':msg}
        if len(self.outside)>=MAXOUTSIDE:
            return {'result':False,'message':Lg().g(297)}
        cons = ZHANXING_CONFIG_CONS.get(fatelevel,10000)
        if cons>self._owner.finance.getCoin():
            msg = Lg().g(88)
            pushOtherMessage(905, msg, [dynamicId])
            return {'result':False,'message':msg}
        templateId = choiceFate(fatelevel)
        fateId = self.addFate(templateId)
        self.planFateLevel(fatelevel)
        self.score += 1
        fate = self.fates.get(fateId)
        data ={'showIndex':self.fateLevel,'maxCount':self.score,'fateIns':fate}
        self._owner.finance.addCoin(-cons)
        self._owner.daily.noticeDaily(21,0,-1)#通知每日目标
        name = fate.templateinfo['name']
        levelname = LEVELNAME.get(self.fateLevel)
        if self.fateLevel>1:
            try:
                msg =Lg().g(298)%(name,levelname)
            except:
                msg =Lg().g(298)%(name.decode('utf8'),levelname)
        else:
            try:
                msg = Lg().g(299)%(name)
            except:
                msg = Lg().g(299)%(name.decode('utf8'))
        
        pushOtherMessage(905, msg, [dynamicId])
        self._owner.schedule.noticeSchedule(9)#成功后的日程目标通知
        characterId = self._owner.baseInfo.id
        prop = {'score':self.score}
        dbCharacterFate.updateCharacterFateSetting(characterId, prop)
        return {'result':True,'data':data}
    
    def getZhanXingInfo(self):
        '''获取占星信息
        '''
        if self._owner.level.getLevel()<16:#功能等级开放限制
            return {'result':False,'message':Lg().g(295)}
        info = {}
        info['maxCount'] = self.score
        info['showIndex'] = self.fateLevel
        info['xyList'] = []
        for fateId in self.outside:
            fate = self.fates.get(fateId)
            if fate:
                info['xyList'].append(fate)
        return {'result':True,'data':info}
    
    def SellFate(self,fateId):
        '''卖掉命格
        @param fateId: int 命格的ID
        '''
        fate = self.fates.get(fateId)
        if not fate:
            return False
        price = fate.templateinfo.get('price')
        fate.destroyByDB()
        del self.fates[fateId]
        self.outside.remove(fateId)
        self._owner.finance.addCoin(price)
        name = fate.templateinfo.get('name')
        try:
            msg = Lg().g(300)%(name,price)
        except:
            msg = Lg().g(300)%(name.decode('utf8'),price)
        dynamicId = self._owner.dynamicId
        pushOtherMessage(905, msg, [dynamicId])
        return True
    
    def PickupFate(self,fateId):
        '''拾取星运
        '''
        if fateId not in self.outside:
            return False#{'result':False,'message':u'星运信息部存在'}
        fate = self.fates.get(fateId)
        if not fate:
            return False#{'result':False,'message':u'星运信息部存在'}
        position = self.findZhanXingPackPosition()
        if position == -1:
            return False#{'result':False,'message':Lg().g(297)}
        self.outside.remove(fateId)
        prop = {'equip':-1,'position':position}
        fate.updateFateInfo(prop)
        self.fatepack[position] = fateId
        return True#{'result':True,'message':u'拾取成功'}
                
    def getZhanXingPack(self):
        '''获取占星包裹信息
        '''
        fatepacklist = []
        for pack in self.fatepack.items():
            fate = self.fates.get(pack[1])
            if fate:
                info = {'position':pack[0],'fate':fate}
                fatepacklist.append(info)
        return fatepacklist
        
    def findZhanXingPackPosition(self):
        '''获取占星包裹空位'''
        for index in xrange( 0,MAXPACK):
            if not self.fatepack.has_key(index):
                return index
        return -1
        
    def ExchangeFate(self,templateId):
        '''积分兑换命格
        '''
        if self._owner.level.getLevel()<50:#功能等级开放限制
            return {'result':False,'message':Lg().g(301)}
        fateInfo = dbCharacterFate.FATE_TEMPLATE.get(templateId)
        if not fateInfo:
            return {'result':False,'message':Lg().g(302)}
        scorerequired = fateInfo['score']
        if scorerequired>self.score:
            return {'result':False,'message':Lg().g(303)}
        position = self.findZhanXingPackPosition()
        if position ==-1:
            return {'result':False,'message':Lg().g(297)}
        characterId = self._owner.baseInfo.id
        fate = Fate(templateId = templateId)
        fate.InsertIntoDB(characterId, equip = -1, position = position)
        self.fates[fate.id] = fate
        self.fatepack[position] = fate.id
        self.score -= scorerequired
        prop = {'score':self.score}
        dbCharacterFate.updateCharacterFateSetting(characterId, prop)
        return {'result':True,'message':Lg().g(304)}
    
    def MoveFateInPack(self,frompos,topos):
        '''移动包裹中的命格
        @param frompos: int 移动的起始位置
        @param topos: int 移动的目标位置
        '''
        fromfateId = self.fatepack.get(frompos)
        if not fromfateId:
            return {'result':False,'message':Lg().g(305)}
        fromfate = self.fates.get(self.fatepack.get(frompos,-1))
        if not fromfate:
            return {'result':False,'message':Lg().g(305)}
        tofateId = self.fatepack.get(topos)
        if not tofateId:
            prop = {'equip':-1,'position':topos}
            self.fates[fromfateId].updateFateInfo(prop)
            self.fatepack[topos] = fromfateId
            del self.fatepack[frompos]
        else:
            if self.fates[fromfateId].templateinfo['quality']>self.fates[tofateId].templateinfo['quality']:
                maxexp = self.fates[tofateId].getAllExp()
                self.fates[fromfateId].addExp(maxexp)
                self.fates[tofateId].destroyByDB()
                del self.fates[tofateId]
                prop = {'position':topos}
                self.fates[fromfateId].updateFateInfo(prop)
                self.fatepack[topos] = fromfateId
                del self.fatepack[frompos]
            else:
                maxexp = self.fates[fromfateId].getAllExp()
                self.fates[tofateId].addExp(maxexp)
                self.fates[fromfateId].destroyByDB()
                del self.fates[fromfateId]
                del self.fatepack[frompos]
        return {'result':True,'data':0}
        
    def equipFate(self,opear,frompos,topos):
        '''装备命格
        @param opear: int 装备星运者的ID
        @param frompos: int 包裹的起始位置
        @param topos: 装备栏的位置
        '''
        fromfateId = self.fatepack.get(frompos)
        if not fromfateId:
            return {'result':False,'message':Lg().g(305)}
        fromfate = self.fates.get(self.fatepack.get(frompos,-1))
        nowtype = fromfate.templateinfo['attrtype']
        if not fromfate:
            return {'result':False,'message':Lg().g(305)}
        if not opear:#操作对象为角色时
            tofateId = self.equiped.get(topos,0)
            tofate = self.fates.get(tofateId)
            for _fateId in self.equiped.values():#检测有角色身上是否同类型的符文
                    _fate = self.fates.get(_fateId)
                    if _fate.templateinfo['attrtype']==nowtype and not tofate:
                        return {'result':False,'message':Lg().g(306)}
        else:#操作对象为宠物时
            pet = self._owner.pet.getPet(opear)
            if not pet:
                return {'result':False,'message':Lg().g(159)}
            tofateId = pet.fate.get(topos,0)
            tofate = self.fates.get(tofateId)
            for _fateId in pet.fate.values():#检测有宠物身上是否同类型的符文
                _fate = self.fates.get(_fateId)
                if _fate.templateinfo['attrtype']==nowtype  and not tofate:
                    return {'result':False,'message':Lg().g(306)}
        if not tofate:#目标位置不存在星运时
            if not opear:
                self.equiped[topos] = fromfateId
            else:
                pet.fate[topos] = fromfateId
            prop = {'equip':opear,'position':topos}
            fromfate.updateFateInfo(prop)
        else:#目标位置存在星运时
            if fromfate.templateinfo['quality']>tofate.templateinfo['quality']:
                maxexp = tofate.getAllExp()
                self.fates[fromfateId].addExp(maxexp)
                tofate.destroyByDB()
                del self.fates[tofateId]
                prop = {'equip':opear,'position':topos}
                self.fates[fromfateId].updateFateInfo(prop)
                if not opear:
                    self.equiped[topos] = fromfateId
                else:
                    pet.fate[topos] = fromfateId
            else:
                maxexp = fromfate.getAllExp()
                self.fates[tofateId].addExp(maxexp)
                fromfate.destroyByDB()
                del self.fates[fromfateId]
                if not opear:
                    self.equiped[topos] = tofateId
                else:
                    pet.fate[topos] = tofateId
        del self.fatepack[frompos]
        self._owner.quest.specialTaskHandle(123)#装备成功后的特殊任务通知
        return {'result':True,'data':opear}
    
    def UnloadFate(self,opear,frompos,topos):
        '''卸下命格信息
        '''
        tofateId = self.fatepack.get(topos)
        if not opear:#操作的是角色时
            fromfateId = self.equiped.get(frompos)
            if not fromfateId:
                return {'result':False,'message':Lg().g(305)}#False
            del self.equiped[frompos]
        else:#操作的是宠物时
            pet = self._owner.pet.getPet(opear)
            if not pet:
                return {'result':False,'message':Lg().g(159)}
            fromfateId = pet.fate.get(frompos)
            if not fromfateId:
                return {'result':False,'message':Lg().g(305)}
            del pet.fate[frompos]
        
        if not tofateId:#当卸下的目的地没有命格时
            self.fatepack[topos] = fromfateId
            self.fates[fromfateId].updateFateInfo({'equip':-2,'position':topos})
        else:#当卸下的目的地有命格时
            if self.fates[fromfateId].templateinfo['quality']>self.fates[tofateId].templateinfo['quality']:#吞噬
                maxexp = self.fates[tofateId].getAllExp()
                self.fates[fromfateId].addExp(maxexp)
                self.fates[tofateId].destroyByDB()
                del self.fates[tofateId]
                prop = {'equip':-2,'position':topos}
                self.fates[fromfateId].updateFateInfo(prop)
                self.fatepack[topos] = fromfateId
            else:#被吞噬
                maxexp = self.fates[fromfateId].getAllExp()
                self.fates[tofateId].addExp(maxexp)
                self.fates[fromfateId].destroyByDB()
                del self.fates[fromfateId]
        return {'result':True,'data':opear}
    
    def moveInEquipSlot(self,opear,frompos,topos):
        '''在装备栏中移动
        '''
        if not opear:#操作的是角色时
            fromfateId = self.equiped.get(frompos)
            if not fromfateId:
                return {'result':False,'message':Lg().g(305)}
            del self.equiped[frompos]
            tofateId = self.equiped.get(topos)
            if not tofateId:
                self.equiped[topos] = fromfateId
                prop = {'position':topos}
                self.fates[fromfateId].updateFateInfo(prop)
            else:#目标存在星运时
                if self.fates[fromfateId].templateinfo['quality']>self.fates[tofateId].templateinfo['quality']:#吞噬
                    self.equiped[topos] = fromfateId
                    maxexp = self.fates[tofateId].getAllExp()
                    self.fates[fromfateId].addExp(maxexp)
                    self.fates[tofateId].destroyByDB()
                    del self.fates[tofateId]
                    prop = {'position':topos}
                    self.fates[fromfateId].updateFateInfo(prop)
                else:
                    maxexp = self.fates[fromfateId].getAllExp()
                    self.fates[tofateId].addExp(maxexp)
                    self.fates[fromfateId].destroyByDB()
                    del self.fates[fromfateId]
        else:#操作的是宠物时
            pet = self._owner.pet.getPet(opear)
            if not pet:
                return {'result':False,'message':Lg().g(159)}
            fromfateId = pet.fate.get(frompos)
            if not fromfateId:
                return {'result':False,'message':Lg().g(305)}
            del pet.fate[frompos]
            tofateId = pet.fate.get(topos)
            if not tofateId:
                pet.fate[topos] = fromfateId
                prop = {'position':topos}
                self.fates[fromfateId].updateFateInfo(prop)
            else:#目标存在星运时
                if self.fates[fromfateId].templateinfo['quality']>self.fates[tofateId].templateinfo['quality']:#吞噬
                    pet.fate[topos] = fromfateId
                    maxexp = self.fates[tofateId].getAllExp()
                    self.fates[fromfateId].addExp(maxexp)
                    self.fates[tofateId].destroyByDB()
                    del self.fates[tofateId]
                    prop = {'position':topos}
                    self.fates[fromfateId].updateFateInfo(prop)
                else:
                    maxexp = self.fates[fromfateId].getAllExp()
                    self.fates[tofateId].addExp(maxexp)
                    self.fates[fromfateId].destroyByDB()
                    del self.fates[fromfateId]
        return {'result':True,'data':opear}
            
            
    def PickUpAll(self):
        '''一键拾取
        '''
        fateList = []
        for fateId in list(self.outside):
            fate = self.fates.get(fateId)
            if not fate or fate.templateinfo['quality']<=0:
                continue
            result = self.PickupFate(fateId)
            if result:
                fateList.append(fateList)
            else:
                break
        return fateList
        
    def SellAll(self):
        '''一键卖出'''
        fateList = []
        fatelist = list(self.outside)
        for fateId in fatelist:
            fate = self.fates.get(fateId)
            if not fate or fate.templateinfo['quality']>0:
                continue
            result = self.SellFate(fateId)
            if result:
                fateList.append(fateList)
        return fateList
        
    def AutoZhanXing(self):
        '''一键占星'''
#        if self._owner.level.getLevel()<50:#功能等级开放限制
#            return {'result':False,'message':Lg().g(301)}
        zhanxingInfolist = []
        while True:
            data = self.ZhanXing(self.fateLevel)
            if not data.get('result'):
                break
            info = data.get('data')
            zhanxingInfolist.append(info)
        return {'result':True,'data':zhanxingInfolist}
            
    def HeChengAll(self):
        '''一键合成'''
        fatelist = list(self.fatepack.items())
        if len(fatelist)<2:
            return {'result':False}
        fatelist.sort( key=lambda d:self.fates[d[1]].templateinfo['quality'])
        rootfate = fatelist[-1]
        maxExp = 0
        for fateitem in fatelist[:-1]:
            maxExp += self.fates[fateitem[1]].getAllExp()
            self.fates[fateitem[1]].destroyByDB()#删除星运实例
            del self.fates[fateitem[1]]
        self.fates[rootfate[1]].addExp(maxExp)
        self.fatepack = {0:rootfate[1]}
        prop = {'equip':-1,'position':0}
        self.fates[rootfate[1]].updateFateInfo(prop)
        return {'result':True}
            
    def GetRoleAndPetFateList(self):
        '''获取角色和宠物的星运装备栏信息
        '''
        fateEquipList = []
        characterFate = {}
        characterFate['rpId'] = self._owner.baseInfo.id
        characterFate['rpName'] = self._owner.baseInfo.getName()
        characterFate['rpLevel'] = self._owner.level.getLevel()
        characterFate['icon'] = self._owner.profession.getFigure()
        characterFate['rpType'] = 1
        characterFate['xyBody1'] = self.fates.get(self.equiped.get(1,-1))
        characterFate['xyBody2'] = self.fates.get(self.equiped.get(2,-1))
        characterFate['xyBody3'] = self.fates.get(self.equiped.get(3,-1))
        characterFate['xyBody4'] = self.fates.get(self.equiped.get(4,-1))
        characterFate['xyBody5'] = self.fates.get(self.equiped.get(5,-1))
        characterFate['xyBody6'] = self.fates.get(self.equiped.get(6,-1))
        fateEquipList.append(characterFate)
        for pet in self._owner.pet._pets.values():
            info = {}
            info['rpId'] = pet.baseInfo.id
            info['rpName'] = pet.baseInfo.getName()
            info['rpLevel'] = pet.level.getLevel()
            info['icon'] = pet.templateInfo['icon']
            info['rpType'] = 2
            equiped = pet.fate
            info['xyBody1'] = self.fates.get(equiped.get(1,-1))
            info['xyBody2'] = self.fates.get(equiped.get(2,-1))
            info['xyBody3'] = self.fates.get(equiped.get(3,-1))
            info['xyBody4'] = self.fates.get(equiped.get(4,-1))
            info['xyBody5'] = self.fates.get(equiped.get(5,-1))
            info['xyBody6'] = self.fates.get(equiped.get(6,-1))
            fateEquipList.append(info)
        return fateEquipList
        
    def MoveFate(self,opeType,opear,frompos,topos):
        '''移动星运
        @param opeType: int 操作类型 0从角色身上到背包1从背包到角色身上2从角色身上到角色身上3从背包到背包
        @param opear: int 操作对象id
        @param frompos: int 包裹的起始位置
        @param topos: 装备栏的位置
        '''
        if opear ==self._owner.baseInfo.id:
            opear = 0
        if opeType==0:
            result = self.UnloadFate(opear, frompos, topos)
            if result.get('result') and opear==0:
                self._owner.pushInfoChanged()
        elif opeType==1:
            result = self.equipFate(opear, frompos, topos)
            if result.get('result') and opear==0:
                self._owner.pushInfoChanged()
        elif opeType==2:
            result = self.moveInEquipSlot(opear, frompos, topos)
            if result.get('result') and opear==0:
                self._owner.pushInfoChanged()
        elif opeType==3:
            result = self.MoveFateInPack(frompos, topos)
        return result
    
    def getAllFateAttr(self):
        '''获取所有的命格属性
        '''
        attrs = {}
        for fateId in self.equiped.values():
            fate = self.fates.get(fateId)   
            if not fate:
                continue
            info = fate.getFateAttr()
            attrs = addDict(attrs, info)
        return attrs
    
