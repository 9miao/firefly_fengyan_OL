#coding:utf8
'''
Created on 2011-8-23
阵眼类
@author: lan
'''
from app.scense.core.PlayersManager import PlayersManager

CHARACTERTYPE_PPLAYER = 1
CHARACTERTYPE_MONSTER = 2
CHARACTERTYPE_PET = 3

class FrontEye(object):
    '''阵眼，阵法中每一格的数据结构'''
    
    def __init__(self,pos,isOpened = False,characterId = -1,effect = 0,effectPercen = 0):
        '''初始化
        @param pos: int 阵眼在阵法中的位置
        @param isOpened: int 阵眼是否开启
        @param characterId: int 阵眼摆放的玩家的ID
        @param effect: int 阵眼的效果类型  1,2,3,4,5,6,7,8
        1=魔攻，2=物防御,3=魔防，4=攻速,5=闪避，6=反击,7=破甲,8=物攻击
        @param effectPercen: 效果的增幅值
        '''
        self._pos = pos
        self._isOpened = isOpened
        self._characterId = characterId
        self._characterType = 1
        self._effect = effect
        self._effectPercen = effectPercen
        
        
    def setIsOpened(self,isOpened):
        '''设置阵眼的开启状态
        '''
        self._isOpened = isOpened
        
    def getIsOpened(self):
        '''获取阵眼的开启状态'''
        return self._isOpened
    
    def setCharacterId(self,characterId,characterType = 1):
        '''安排阵眼上的玩家'''
        self._characterId = characterId
        self._characterType = characterType
        
    def getCharacterId(self):
        '''获取阵眼上的玩家ID'''
        return self._characterId
    
    def setEffect(self,effect):
        '''设置阵眼上的效果类型'''
        self._effect = effect
        
    def getEffect(self):
        '''获取阵眼上的效果类型'''
        return self._effect
    
    def setEffectPercen(self,effectPercen):
        '''设置效果的增幅值%'''
        self._effectPercen = effectPercen
        
    def getEffectFormula(self):
        '''获取效果的计算公式'''
        effectStr = ''
        if self._effect ==1:
            effectStr = "member['magicAttack'] =member['magicAttack']*(1+0.01*%d)"%self._effectPercen
        elif self._effect ==2:
            effectStr = "member['physicalDefense'] = member['physicalDefense']*(1+0.01*%d)"%self._effectPercen
        elif self._effect ==3:
            effectStr = "member['magicDefense'] = member['magicDefense']*(1+0.01*%d)"%self._effectPercen
        elif self._effect ==4:
            effectStr = "member['speed'] = member['speed']*(1+0.01*%d)"%self._effectPercen
        elif self._effect ==5:
            effectStr = "member['dodgeRate'] =member['dodgeRate']*(1+0.01*%d)"%self._effectPercen
        elif self._effect ==6:
            effectStr = "member['physicalDefense'] = member['physicalDefense']*(1+0.01*%d)"%self._effectPercen
        elif self._effect ==7:
            effectStr = "member['physicalDefense'] = member['physicalDefense']*(1+0.01*%d)"%self._effectPercen
        elif self._effect ==8:
            effectStr = "member['physicalAttack'] = member['physicalAttack']*(1+0.01*%d)"%self._effectPercen
        return effectStr
        
    def getEffectPercen(self):
        '''获取效果的增幅值'''
        return self._effectPercen
    
    def fromatFrontEye(self):
        '''格式化阵眼的信息'''
        info = {}
        player = PlayersManager().getPlayerByID(self._characterId)
        info['isOpened'] = self._isOpened
        info['effectPercen'] = self._effectPercen
        info['pos'] = self._pos
        info['isHaveRole'] = False
        info['roleInfo'] = {}
        if player:
            info['isHaveRole'] = True
            info['roleInfo']['roleId'] = self._characterId
            info['roleInfo']['profession'] = player.profession.getFigure()
            info['roleInfo']['profession'] = player.baseInfo.getNickName()
            info['roleInfo']['rolelevel'] = player.level.getLevel()
        return info
        
        