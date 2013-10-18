#coding:utf8
'''
Created on 2011-12-16
角色的阵法设置信息
@author: lan
'''

from app.scense.component.Component import Component
from app.scense.utils.dbopera import dbCharacterMatrix,dbNobility
from app.scense.core.language.Language import Lg

CANCATCHPET = {1:1,2:2,3:4}
CANCATCHPETLEVEL = {1:5,2:20,3:50}

class CharacterMatrixComponent(Component):
    '''角色邮件列表组件'''
    
    def __init__(self,owner):
        '''初始化
        '''
        Component.__init__(self, owner)
        #已设置的阵法相关的信息
        self._matrixSetting = {}
        self.initMatrixInfo()
        
    def initMatrixInfo(self):
        '''初始化阵法设置信息'''
        characterId = self._owner.baseInfo.id
        matrixInfo = dbCharacterMatrix.getAllCharacterMatrix(characterId)
        if not matrixInfo:
            characterId = self._owner.baseInfo.id
            props = {'characterId':characterId,'eyes_5':0}
            dbCharacterMatrix.InsertCharacterMatrixInfo(characterId, props)
            self._matrixSetting = {'eyes_1':-1,
                                   'eyes_2':-1,'eyes_3':-1,'eyes_4':-1,'eyes_5':0,
                                   'eyes_6':-1,'eyes_7':-1,'eyes_8':-1,'eyes_9':-1}
        else:
            self._matrixSetting = matrixInfo
        
    def getMatrixMaxEyesCnt(self):
        '''获取阵法最大阵眼数
        '''
        return 9
    
    def isCZ(self):
        '''判断是否有宠物在阵法中'''
        wzlist=self._matrixSetting.values()#所有阵点上的人活着宠物  0代表人    -1代表空阵点  其他代表宠物id
        for zd in wzlist:
            if zd>0:#如果阵点上面有宠物
                return True
        return False
    
    def getNowCnt(self):
        '''获取当前阵法中的单位的数量
        '''
        cnt = 0
        pets = self._owner.pet._pets.keys()
        for petId in self._matrixSetting.values():
            if petId ==0 or petId in pets:
                cnt+=1
        return cnt
        
        
    def getMatrixListSetting(self):
        '''获取阵法列表设置'''
        MatrixListInfo = {}
        MatrixListInfo['jwDes'] = self._owner.nobility.getName()
        MatrixListInfo['curNum'] = self.getNowCnt()
        MatrixListInfo['maxNum'] = self.getMatrixMaxEyesCnt()
        MatrixListInfo['matrixTitleInfo'] = []
        for index in range(1,10):
            info = {}
            info['titlePos'] = index-1
            info['hasPet'] = False
            info['petId'] = -1
            info['type'] = 0
            info['icon'] = 0
            petId = self._matrixSetting.get('eyes_%d'%index)
            if petId==0:
                info['hasPet'] = True
                info['petId'] = 0
            elif petId>0:
                info['hasPet'] = True
                info['petId'] = petId
                pet  = self._owner.pet.getPets().get(petId)
                info['petId'] = pet.baseInfo.getId()
                info['type'] = pet.templateInfo.get('type',0)
                info['icon'] = pet.templateInfo.get('icon',0)
            MatrixListInfo['matrixTitleInfo'].append(info)
        return MatrixListInfo
                
    def updateMatrix(self,petId,operationType,fromPos,toPos):
        '''更新阵法位置信息
        @param petId: int 宠物的ID 为0时表示是角色自身
        @param operationType: int 操作类型0从宠物列表到阵法1从阵法到宠物列表2从阵法到阵法
        @param fromPos: int 起始位置
        @param toPos: int 结束位置
        '''
        characterId = self._owner.baseInfo.id
        fromEyeNo = fromPos+1
        toEyeNo = toPos+1
        if operationType==0:
            pet = self._owner.pet._pets.get(petId)
            if not pet:
                return {'result':False,'message':Lg().g(159)}
            petlevel = pet.level.getLevel()
            leveldelta = petlevel -self._owner.level.getLevel()
            if leveldelta>=5:
                return {'result':False,'message':Lg().g(366)%(petlevel)}
            
            if petId in self._matrixSetting.values():
                return {'result':False,'message':Lg().g(367)}
            if self._matrixSetting.get('eyes_%d'%toEyeNo)==0:
                return {'result':False,'message':Lg().g(368)}
            topetId = self._matrixSetting.get('eyes_%d'%toEyeNo)
            nowcnt = self.getNowCnt()
            maxcnt = self.getMatrixMaxEyesCnt()
            if nowcnt>=maxcnt:
                if topetId ==-1 or (topetId not in self._owner.pet._pets.keys()):
                    return {'result':False,'message':Lg().g(369)}
            props = {'eyes_%d'%(toEyeNo):petId}
            self._matrixSetting['eyes_%d'%(toEyeNo)] = petId
            dbCharacterMatrix.updateCharacterMatrixInfo(characterId, props)
            self._owner.quest.specialTaskHandle(109)#特殊任务处理
            return {'result':True}
        elif operationType == 1:
            
            petId = self._matrixSetting.get('eyes_%d'%fromEyeNo)
            if petId==-1:
                return {'result':False,'message':Lg().g(370)}
            if petId==0:
                return {'result':False,'message':Lg().g(368)}
            props = {'eyes_%d'%(fromEyeNo):-1}
            self._owner.pet.addLastRemove(petId)
            self._matrixSetting['eyes_%d'%(fromEyeNo)] = -1
            dbCharacterMatrix.updateCharacterMatrixInfo(characterId, props)
            return {'result':True}
        else:
            fromPid = self._matrixSetting.get('eyes_%d'%fromEyeNo,-1)
            toPid =  self._matrixSetting.get('eyes_%d'%toEyeNo,-1)
            if fromPid==-1:
                return {'result':False,'message':Lg().g(370)}
            props = {'eyes_%d'%(toEyeNo):fromPid,'eyes_%d'%(fromEyeNo):toPid}
            self._matrixSetting['eyes_%d'%(toEyeNo)] = fromPid
            self._matrixSetting['eyes_%d'%(fromEyeNo)] = toPid
            dbCharacterMatrix.updateCharacterMatrixInfo(characterId, props)
            return {'result':True}
    
    def dropPetInMatrix(self,petId):
        """丢弃阵法中的宠物
        """
        if petId not in self._matrixSetting.values():
            return False
        for eye,_petId in self._matrixSetting.items():
            if petId == _petId:
                characterId = self._owner.baseInfo.id
                props = {eye:-1}
                self._matrixSetting[eye]=-1
                dbCharacterMatrix.updateCharacterMatrixInfo(characterId, props)
                return True
        return False
        
        
        
        