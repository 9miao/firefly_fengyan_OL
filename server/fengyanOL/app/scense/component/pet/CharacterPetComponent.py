#coding:utf8
'''
Created on 2011-12-14
角色的宠物信息
@author: lan
'''
from app.scense.component.Component import Component
from app.scense.core.character.Pet import Pet
from app.scense.utils.dbopera import dbCharacterPet,dbVIP
import math

from app.scense.netInterface.pushObjectNetInterface import pushOtherMessage
import random
from app.scense.core.language.Language import Lg

MAXPETCNT = 10 #拥有宠物的最大数量
CATCHPETTASKTYPE = 107
RATE_BASE = 100000#几率基础值

ERROR = {-5:Lg().g(159)}
PETTRAINCOINCONS = 250#宠物游戏币培养消耗的比例
PETTRAINGOLDCONS = {1:{'gold':30,'vip':1},
                2:{'gold':80,'vip':3},
                3:{'gold':200,'vip':5}}#宠物培养消耗
#技能消耗品的ID
SKILLCRYSTAL = {1:20030061,
                2:20030062,
                3:20030063,
                4:20030064,
                5:20030065}

RESURCUS = 10 #宠物复活消耗

CANCATCHPET = {1:1,2:2,3:4}

class CharacterPetComponent(Component):
    '''角色的宠物信息类'''
    
    def __init__(self,owner):
        '''init Object'''
        Component.__init__(self, owner)
        #角色的宠物列表
        self._pets = {}
        #已经收集到的宠物
        self._activepets = []
        #角色的宠物信息是否已经初始化
        self._hasInit = 0
        #获取宠物消息的队列
        self._getPetMsg = []
        #宠物的移动频率
        self._moveTag = 0
        #最后丢弃的宠物的ID
        self.lastRemove = []
        self.initCharacterPetInfo()
        
    def initCharacterPetInfo(self):
        '''初始化角色宠物信息'''
        if self._hasInit:
            return
        petlist = dbCharacterPet.getCharacterAllPet(self._owner.baseInfo.id)
        collectstr = dbCharacterPet.getCharacterCollect(self._owner.baseInfo.id)
        for petid in petlist:
            petId = petid[0]
            pet = Pet(petId = petId)
            self._pets[petId] = pet
        if collectstr is None:
            dbCharacterPet.insertCharacterCollect(self._owner.baseInfo.id)
        else:
            self._activepets = eval("[%s]"%collectstr)
        self._hasInit = 1
        
    def getNowShowCnt(self):
        '''设置现在跟随的宠物的数量'''
        return len([pet for pet in self._pets.values() if pet.getFlowFlag()])
        
    def checkCanFlow(self):
        '''检查是否还能设置宠物设置'''
        catchPetLevel = self._owner.skill.getCatchPetLevel()
        canshowcnt = CANCATCHPET.get(catchPetLevel)
        nowcnt = self.getNowShowCnt()
        if nowcnt < canshowcnt:
            return True
        return False
    
    def updateShow(self,petId):
        '''设置展示的宠物的ID'''
        viplevel = self._owner.baseInfo._viptype
        if not dbVIP.vipCertification('petflow', viplevel):
            return {'result':False,'message':Lg().g(217)}
        pet = self.getPet(petId)
        FlowFlag = pet.getFlowFlag()
        if not FlowFlag:
            canFlow = self.checkCanFlow()
            if not canFlow:
                return {'result':False,'message':Lg().g(419)}
            pet.updateFlowFlag(True)
            return {'result':True,'message':Lg().g(420),'data':False}
        else:
            pet.updateFlowFlag(False)
            return {'result':True,'message':u'','data':True}
        
    def getPets(self):
        '''获取角色的宠物列表'''
        self.initCharacterPetInfo()
        return self._pets
    
    def getHasPetTemplatelist(self):
        '''获取已经获取的宠物的模版列表
        '''
        return [pet.templateId for pet in self._pets.values()]
        
    def formatCharacterPetListInfo(self):
        '''格式或角色的宠物信息'''
        pets = self.getPets()
        return pets.values()
    
    def getCharacterPetListInfo(self):
        '''获取角色宠物列表'''
        pets = self.getPets()
        PetListInfo = {}
        PetListInfo['curPetNum'] = len(pets)
        PetListInfo['maxPetNum'] = 10
        PetListInfo['petInfo'] = []
        for pet in pets.values():
            info = {}
            info['petId'] = pet.baseInfo.getId()
            info['resPetId'] = pet.templateInfo.get('resourceid')
            info['petName'] = pet.baseInfo.getName()
            info['petLevel'] = pet.level.getLevel()
            info['icon'] = pet.templateInfo.get('icon')
            info['type'] = pet.templateInfo.get('type')
            PetListInfo['petInfo'].append(info)
        return PetListInfo
    
    def getPetNum(self):
        '''获取当前宠物的数量'''
        pets = self.getPets()
        return len(pets)
    
    def ishavepet(self):
        '''判断是否有蜻蜓猎手宠物'''
        for info in self._pets.values():
            if info.templateId==15004:
                return True
        return False
    
    def OpenPetEgg(self,level = 1):
        '''打开宠物蛋
        '''
        if level==1:
            petlist = [25085,25086,25087,25088,25089,25090,25091,25092,25093,25095,25096,25097,25098,25099,25100,25101,25102,25103,25104,25105,25106,25107,25108,25109,25110,35001,35002,35003,35004,35005,35006,25001,25002,25003,25062,25063,25064,25065,25066,25067,25068,25069,25070,25071,25072,25073,35049,35050,35051]
        else:
            petlist = [25013,25014,25015,25016,25017,25018,25019,25020,25021,25022,25025,25026,25027,25029,25030,25031,25032,25033,25034,25035,25044,25045,25046,25048,25049,25050,25051,25052,25053,25054,25055,35080,35081,35082,35083,35084,35085,35086,25001,25002,25003,25004,25062,25063,25064,25065,25066,25067,25068,25069,25070,25071,25072,25073,35049,35050,35051]
        self._OpenPetEgg(petlist)
    
    def _OpenPetEgg(self,petlist):
        '''打开宠物蛋'''
        petId = random.choice(petlist)
        quality = random.randint(1,7)
        result = self.addPet(templateId = petId, quality=quality)
        if result==-1:
            raise Exception(Lg().g(421))
        elif result==-2:
            raise Exception(Lg().g(428))
        else:
            self._owner.quest.specialTaskHandle(110)
        
    def OpenOrdEgg(self,templateId,quality = 1):
        '''打卡普通宠物蛋'''
        result = self.addPet(templateId,quality = 1)
        if result == -1:
            raise Exception(Lg().g(421))
        elif result == -2:
            raise Exception(Lg().g(428))
        else:
            self._owner.quest.specialTaskHandle(110)
            
    def openRandEgg(self,petlist,default):
        '''打开随机宠物蛋
        @param petlist: list [(宠物ID，随机区间)]随机掉落
        @param default: 宠物的ID 默认掉落
        '''
        petsrates = [petinfo[1] for petinfo in petlist]
        petid = 0
        rate = random.randint(0,RATE_BASE)
        for index in range(len(petlist)):
            if rate<sum(petsrates[:index+1]):
                petid = petlist[index][0]
                break
        if not petid:
            petid = default
        result = self.addPet(petid)
        if result==-1:
            raise Exception(Lg().g(421))
        elif result==-2:
            raise Exception(Lg().g(428))
        else:
            self._owner.quest.specialTaskHandle(110)
            
    def hasThisType(self,templateId):
        '''判断是否已经存在该种类型的宠物
        '''
        return templateId in [pet.templateId for pet in self._pets.values()]
        
    def addPet(self,templateId,quality = 1,level =1,statu = 1):
        '''添加一个宠物'''
        
        self.initCharacterPetInfo()
        if self.getPetNum()>=MAXPETCNT:
            return -1#宠物数量达到上限
        if self.hasThisType(templateId):
            return -2#已经拥有该种类型的宠物
        pet = Pet(templateId = templateId,level=level,owner = self._owner.baseInfo.id)
        result = pet.InsertIntoDB()
        if result:
            msg = Lg().g(422)%pet.baseInfo.getName()
            if statu:
                pushOtherMessage(905, msg, [self._owner.getDynamicId()])
            else:
                self._owner.msgbox.putFightTMsg(msg)
            self._pets[pet.baseInfo.id] = pet
            self._owner.daily.noticeDaily(10,0,len(self._pets))
            self.appendPetCollect(templateId)
            return pet.baseInfo.getName()
        
    def DropPet(self,petId):
        '''丢弃宠物
        @param petId: int 宠物的id
        '''
        self.initCharacterPetInfo()
        if petId not in self._pets.keys():
            return -5#不存在该宠物
        pet = self._pets.get(petId)
        result = pet.destroyByDB()
        if result:
            petTemplateId = pet.templateId
            self.appendPetCollect(petTemplateId)
            result = self._owner.matrix.dropPetInMatrix(petId)
            if result:
                self.lastRemove.append(petId)
            del self._pets[petId]
            return 1
        return 0
    
    def addLastRemove(self,petId):
        '''添加宠物移除列表
        '''
        self.lastRemove.append(petId)
    
    def popLastRemove(self):
        '''取出并清空宠物移除列表'''
        removelist = list(self.lastRemove)
        self.lastRemove = []
        return removelist
    
    def checkCanTrain(self,trainingLevel):
        '''检测是否能培养'''
        if trainingLevel==1:
            if self._owner.finance.getCoin()>2000:
                return True
            return False
        elif trainingLevel==2:
            if self._owner.finance.getGold()>2:
                return True
            return False
        elif trainingLevel==3:
            if self._owner.finance.getGold()>5:
                return True
            return False
        elif trainingLevel==4:
            if self._owner.finance.getGold()>10:
                return True
            return False
        return False
    
    def trainCons(self,trainingLevel):
        '''培养消耗处理
        '''
        if trainingLevel==1:
            self._owner.finance.addCoin(-2000)
        elif trainingLevel==2:
            self._owner.finance.consGold(2,8)#宠物培养消耗
        elif trainingLevel==3:
            self._owner.finance.consGold(5,8)#宠物培养消耗
        elif trainingLevel==4:
            self._owner.finance.consGold(10,8)#宠物培养消耗
        
    def Training(self,petId,trainingLevel):
        '''宠物培养
        @param petId: int 宠物的id
        @param trainingLevel: int 培养的层次
        '''
        if self._owner.level.getLevel()<10:#功能等级限制
            return {'result':False,'message':Lg().g(429)}
        self.initCharacterPetInfo()
        if not self.checkCanTrain(trainingLevel):
            return {'result':False,'message':Lg().g(88)}#
        if petId not in self._pets.keys():
            return {'result':False,'message':Lg().g(159)}#
        pet = self._pets.get(petId)
        data = pet.Training(trainingLevel)
        self.trainCons(trainingLevel)
        self._owner.daily.noticeDaily(24,0,-1)#每日目标通知培养宠物次数
        self._owner.schedule.noticeSchedule(14)#成功后的日程目标通知
        return {'result':True,'data':data}
    
    def Tihuan(self,petId,tihuanType):
        '''替换宠物成长
        @param petId: int 宠物的id
        @param tihuanType: int 操作类型0维持1替换
        '''
        if not tihuanType:
            return {'result':True}
        self.initCharacterPetInfo()
        if petId not in self._pets.keys():
            return {'result':False,'message':Lg().g(159)}#
        pet = self._pets.get(petId)
        result = pet.Tihuan()
        if result.get('result'):
            self._owner.quest.specialTaskHandle(120)#成功后的特殊任务通知
        return result
        
        
    def getPet(self,petId):
        '''获取指定的宠物'''
        self.initCharacterPetInfo()
        return self._pets.get(petId)
        
    def updateName(self,petId,petName):
        '''修改宠物名称'''
        self.initCharacterPetInfo()
        pet = self.getPet(petId)
        if pet.level.getLevel()<3:
            return -1
        if not pet:
            return 0
        result = pet.updateName(petName)
        return result
        
    def modifySlogan(self,petId,slogan):
        '''修改战斗宣言
        @param petId: int 宠物的id
        @param slogan: string 战斗宣言
        '''
        self.initCharacterPetInfo()
        pet = self.getPet(petId)
        result = pet.modifySlogan(slogan)
        return result
        
    def ResurPet(self,petId):
        '''复活宠物'''
        if self._owner.finance.getGold()<RESURCUS:
            return {'result':False,'message':Lg().g(190),'data':{'failType':1}}
        self.initCharacterPetInfo()
        pet = self.getPet(petId)
        if not pet:
            return {'result':False,'message':Lg().g(159),'data':{'failType':0}}
        result = pet.resurPet()
        if result.get('result'):
            self._owner.finance.addGold(-RESURCUS)
            self._owner.pushInfoChanged()
        return result
        
    def updatePetPosition(self,position,state = 1):
        '''更新所有展示的宠物的位置
        @param position: int 宠物的位置
        '''
        if not state:
            self._moveTag +=1
            if self._moveTag !=15:
                return
            else:
                self._moveTag =0
        position = self._owner.baseInfo.getPosition()
        lastposition = self._owner.baseInfo.getLastPosition()
        if position[0]-lastposition[1]>0:
            force = 0
        else:
            force = 1
        index = 1
        for petId in self._owner.matrix._matrixSetting.values():
            if petId<=0:
                continue
            pet = self.getPet(petId)
            pet.updatePosition(position,index,force = force)
            index += 1
        
    def restorationPetHP(self,Surplus):
        '''恢复所有宠物的血'''
        for petId in self._pets.keys():
            Surplus = self._pets[petId].restorationHp(Surplus)
            if Surplus ==0:
                return 0
        return Surplus
    
    def TransferExp(self,petFrom,petTo):
        '''宠物经验传承
        @param petFrom: int 传承的宠物
        @param petTo: int 被传承的宠物
        '''
        frompet = self.getPet(petFrom)
        topet = self.getPet(petTo)
        if not (frompet and topet):
            return {'result':False}
        if frompet.chuancheng:
            return {'result':False,'message':Lg().g(430)}
        if topet._chuancheng:
            return {'result':False,'message':Lg().g(431)}
        expgoal = frompet.level.getAllExp()
        _expgoal = topet.level.getAllExp()
        if _expgoal>expgoal:
            return {'result':False,'message':Lg().g(432)}
        reqCoin = (frompet.level.getLevel()+topet.level.getLevel())*500
        if self._owner.finance.getCoin()<reqCoin:
            return {'result':False,'message':Lg().g(88)}
        self._owner.finance.addCoin(-reqCoin)
        topet.level.addExp(expgoal)
        frompet.updateChuanCheng()
        topet.update_ChuanCheng()
        self._owner.schedule.noticeSchedule(15)#成功后的日程目标通知
        self._owner.quest.specialTaskHandle(126)#成功后的特殊任务通知
        return {'result':True,'message':Lg().g(433)}
    
    def getTransferLevel(self,petFrom,petTo):
        '''获取宠物传承后可以提升的等级
        @param petFrom: int 传承的宠物
        @param petTo: int 被传承的宠物
        '''
        frompet = self.getPet(petFrom)
        topet = self.getPet(petTo)
        if not (frompet and topet):
            return {'result':False}
        if frompet.chuancheng:
            return {'result':False,'message':Lg().g(430)}
        if topet._chuancheng:
            return {'result':False,'message':Lg().g(431)}
        expgoal = frompet.level.getAllExp()
        lastLevel = topet.level.ForecastLevelUp(expgoal)
        return {'result':True,'message':Lg().g(433),'data':lastLevel}
    
    def getTransferPetList(self,petFrom):
        '''获取能够被传承的宠物的信息'''
        frompet = self.getPet(petFrom)
        expgoal = frompet.level.getAllExp()
        petInfoList = []
        if frompet.chuancheng:
            return petInfoList
        for pet in self._pets.values():
            if not pet._chuancheng and pet.baseInfo.getId()!=petFrom:
                expgoal = frompet.level.getAllExp()
                _expgoal = pet.level.getAllExp()
                if _expgoal>expgoal:
                    continue
                info = {}
                info['pet'] = pet
                level1 = frompet.level.getLevel()
                level2 = pet.level.getLevel()
                info['reqCoin'] = (level1 + level2)*500
                petInfoList.append(info)
        return petInfoList
    
    def collectNotice(self,itemTemplateID,count):
        '''收集通知
        @param itemTemplateID: int 收集到的物品的ID
        '''
        petId = dbCharacterPet.PET_ITEM.get(itemTemplateID)
        if not petId:
            return False
        package = self._owner.pack._package.getPackageByType(1)
        nowCount =  package.countItemTemplateId(itemTemplateID)
        if petId in self._activepets:
            return True
        petinfo = dbCharacterPet.PET_TEMPLATE.get(petId)
        maxHun = petinfo.get('soulcount')
        if maxHun>nowCount+count:
            return False
        self._owner.pack.delItemByTemplateId(itemTemplateID,nowCount)
        self.appendPetCollect(petId)
        return True
    
    def appendPetCollect(self,petId):
        '''添加一个新收集的宠物的ID
        '''
        if petId in self._activepets:
            return
        self._activepets.append(petId)
        characterId = self._owner.baseInfo.id
        dbCharacterPet.updateCharacterCollect(characterId, self._activepets)
        self._owner.daily.noticeDaily(19,0,-1)#通知每日目标
        
    def GetTuJianPetList(self,ttype,page,limit = 7):
        '''获取图鉴信息
        @param ttype: int 图鉴的类型
        '''
        itemslist = self._owner.pack._package._PropsPagePack._items
        collectpetlist = [dbCharacterPet.PET_ITEM.get(item['itemComponent'].baseInfo.itemTemplateId)\
                    for item in itemslist]
        petlist = self._activepets + collectpetlist
        petSjlist = []
        slInfo = {}
        for petId in petlist:
            if not petId:
                continue
            petInfo = dbCharacterPet.PET_TEMPLATE.get(petId)
            if petInfo.get('attrType',1)==ttype:
                info = {}
                viewFlag = petId in self._activepets
                info['petName'] = petInfo.get('nickname',u'')
                info['petLevel'] = 1
                info['petId'] = petId
                info['viewFlag'] = viewFlag
                pet = Pet(templateId = petId)
                info['quality'] = pet.attribute.getPetQuality()
                petSjlist.append(info)
        maxPage = int(math.ceil(len(petSjlist)*1.0/7))
        if maxPage<1:
            maxPage = 1
        slInfo['sjPro'] = int(math.ceil(len(self._activepets)/len(dbCharacterPet.PET_TEMPLATE)))
        slInfo['curPage'] = page
        slInfo['maxPage'] = maxPage
        slInfo['sjListPet'] = petSjlist[(page-1)*limit:page*limit]
        return slInfo
#        maxPage = int(math.ceil(len(pets)/7))
#        if maxPage<1:
#            maxPage = 1
#        slInfo['maxPage'] = maxPage
#        slInfo['curPage'] = page
#        slInfo['sjPro'] = int(math.ceil(len(self._activepets)/len(dbCharacterPet.PET_TEMPLATE)))
#        slInfo['sjListPet'] = []
        
#        petIdlist = pets[(page-1)*limit:page*limit]
#        for petId in petIdlist:
#            petInfo = dbCharacterPet.PET_TEMPLATE.get(petId)
#            info = {}
#            viewFlag = petId in self._activepets
#            info['petName'] = petInfo.get('nickname',u'')
#            info['petLevel'] = 1
#            info['petId'] = petId
#            info['viewFlag'] = viewFlag
#            info['quality'] = petInfo.get('baseQuality')
#            slInfo['sjListPet'].append(info)
#        return slInfo
        
    def GetOnePetTuJianInfo(self,petId):
        '''获取某个宠物的收集信息
        '''
        info = {}
        petinfo = dbCharacterPet.PET_TEMPLATE.get(petId)
        info['pet'] = Pet(templateId=petId)
        requiredId = petinfo.get('soulrequired')
        info['curHun'] = self._owner.pack._package._PropsPagePack.countItemTemplateId(requiredId)
        info['maxHun'] = petinfo.get('soulcount')
        if petId in self._activepets:
            info['curHun'] = info['maxHun']
        info['reqCoin'] = self._owner.level.getLevel()*2000
        return info
        
    def ZhaoHuan(self,petId):
        '''宠物召唤信息'''
        if petId not in self._activepets:
            return {'result':False,'message':Lg().g(434)}
        if self._pets.has_key(petId):
            return {'result':False,'message':Lg().g(168)}
        if self.getPetNum()>=MAXPETCNT:
            return {'result':False,'message':Lg().g(421)}
        reqCoin = self._owner.level.getLevel()*2000
        if self._owner.finance.getCoin()<reqCoin:
            return {'result':False,'message':Lg().g(435)}
        result = self.addPet(petId)
        if result==-1:
            return {'result':False,'message':Lg().g(436)}
        elif result==-2:
            return {'result':False,'message':Lg().g(428)}
        self._owner.finance.addCoin(-reqCoin)
        self._owner.quest.specialTaskHandle(117)#特殊任务处理
        return {'result':True,'message':Lg().g(437)}
        
        
