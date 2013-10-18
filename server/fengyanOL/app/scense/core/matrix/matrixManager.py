#coding:utf8
'''
Created on 2011-8-23
阵法管理器
@author: lan
'''
from app.scense.core.singleton import Singleton
from app.scense.utils import dbaccess
from app.scense.core.matrix.matrix import Matrix

class MatrixManager:
    '''阵法管理器，存放所有阵法信息'''
    
    __metaclass__ = Singleton

    def __init__(self):
        '''初始化'''
        self.matrixs = {}
        for matrixsID in dbaccess.all_marix_info.keys():
            self.matrixs[matrixsID] = Matrix(matrixsID)
            
    def getMatrixById(self,matrixsID):
        '''根据ID获取'''
        return self.matrixs.get(matrixsID,None)
    
    def getMatrixs(self):
        '''获取阵法列表'''
        return self.matrixs
    
    def getMatrixsInfo(self):
        '''获取阵法列表信息'''
        infoList = []
        matrixsList = self.matrixs.values()
        for mat in matrixsList:
            infoList.append(mat.fromatMatrixInfo())
        return infoList
        

        