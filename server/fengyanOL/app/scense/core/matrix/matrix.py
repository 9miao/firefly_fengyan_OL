#coding:utf8
'''
Created on 2011-8-23
阵法类
@author: lan
'''
from app.scense.utils import dbaccess
from app.scense.core.matrix.frontEye import FrontEye

class Matrix:
    '''阵法'''
    
    def __init__(self,id):
        '''初始化阵法类
        @param id: int 阵法的ID
        @param name: str 阵法的名称
        @param description: 阵法的描述
        @param levelrequired: int 阵法等级需求
        @param noweffect: int 阵法正在使用的效果 0 为没有使用效果
        @param frontEyes: dict 阵法的阵眼信息
        '''
        self.id = id
        self.name = ''
        self.description = ''
        self.levelrequired = 1
        self.noweffect = 0
        self.frontEyes = {}
        self.initMatrixInfo()
        
    def initMatrixInfo(self):
        '''初始化阵法信息'''
        for i in range(1,10):
            self.frontEyes[i]=FrontEye(i)
        formatinfo = dbaccess.all_marix_info[self.id]
        self.name = formatinfo['name']
        self.description = formatinfo['description']
        self.levelrequired = formatinfo['levelrequired']
        for i in range(1,6):
            info = eval('['+formatinfo['frontEye_%d'%i]+']')
            self.frontEyes[info[0]].setIsOpened(True)
            self.frontEyes[info[0]].setEffect(info[1])
            self.frontEyes[info[0]].setEffectPercen(info[2])
            
    def checkCanUse(self,level):
        '''检测是否能使用该阵法'''
        if self.levelrequired>level:
            return False
        return True
            
    def getNowEffect(self):
        '''设置阵法当前使用效果'''
        return self.noweffect
        
    def setNowEffect(self,noweffect):
        '''设置阵法当前使用效果'''
        self.noweffect = noweffect
        
    def setFrontEye(self,pos,characterID):
        '''设置阵眼'''
        self.frontEyes[pos].setCharacterId(characterID)
        
    def getFrontEye(self,pos):
        '''获取指定阵眼的信息'''
        return self.frontEyes.get(pos)
        
    def getMatrixInfo(self):
        '''获取阵法信息'''
        info = {}
        info['matrixId'] = self.id
        info['matrixName']= self.name
        info['matrixDes'] = self.description
        info['frontEyes'] = self.frontEyes
        info['levelrequired'] = self.levelrequired
        return info
        
        
    def fromatMatrixInfo(self):
        '''格式化阵法信息'''
        info = {}
        info['matrixId'] = self.id
        info['matrixname']= self.name
        info['description'] = self.description
        info['noweffect'] = self.noweffect
        info['frontEyeList'] = []
        for eye in self.frontEyes.values():
            eyeInfo = eye.fromatFrontEye()
            info['frontEyeList'].append(eyeInfo)
        return info
    
    def dropMember(self,characterId):
        '''清除成员'''
        eye = self.findMemberEyeNo(characterId)
        if eye:
            self.frontEyes[eye].setCharacterId(-1)
        
    def addMember(self,characterId):
        '''默认方式的添加角色到阵法中'''
        eye = self.findFrontEyeSpace()
        if eye:
            self.frontEyes[eye].setCharacterId(characterId)
    
    def findMemberEyeNo(self,characterId):
        '''检测成员在阵法中的位置'''
        for eye in self.frontEyes.keys():
            if self.frontEyes[eye].getIsOpened() and self.frontEyes[eye].getCharacterId()==characterId:
                return eye
        return 0
    
    def findFrontEyeSpace(self):
        '''查找阵法空位'''
        for eye in [5,1,2,3,4,6,7,8,9]:
            if self.frontEyes[eye].getIsOpened() and self.frontEyes[eye].getCharacterId()==-1:
                return eye
        return 0
            
    def clearUpMatrix(self,members):
        '''清理阵法'''
        for eye in self.frontEyes.keys():
            if self.frontEyes[eye].getIsOpened() and self.frontEyes[eye].getCharacterId() not in [members]:
                self.frontEyes[eye]._characterId = -1
    
    def updateMatrixInfo(self,members):
        '''更新阵法信息'''
        self.clearUpMatrix(members)
        for mem in members:
            if not self.findMemberEyeNo(mem):
                eye = self.findFrontEyeSpace()
                if eye:
                    self.frontEyes[eye].setCharacterId(mem)
        
    def getMemberList(self):
        '''获取所有的成员列表'''
        return [frontEye.getCharacterId() for frontEye in self.frontEyes.values()\
                 if frontEye.getCharacterId()!=-1]
        
    def getMemberCnt(self):
        '''获取成员数量'''
        return len([frontEye.getCharacterId() for frontEye in self.frontEyes.values()\
                 if frontEye.getCharacterId()!=-1])
        
        
        
        