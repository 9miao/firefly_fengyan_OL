#coding:utf8
'''
Created on 2012-6-7
命格类
@author: Administrator
'''
from app.scense.utils.dbopera import dbCharacterFate

class Fate:
    
    def __init__(self,id = 0,templateId = 0,insData = {}):
        '''初始化命格信息
        @param templateinfo: dict 命格的基本信息
        @param fid: int 命格的实例ID
        @param templateId: int 命格的模板ID
        @param level: int 命格的当前等级
        @param exp: int 命格的当前经验
        '''
        self.templateinfo = {}
        self.id = id
        self.templateId = templateId
        self.level = 1
        self.exp = 0
        self.initFateData(insData)
        
    def initFateData(self,insData):
        '''初始化命格数据'''
        if insData:
            self.id = insData['id']
            self.templateId = insData['tempalteId']
            self.level = insData['level']
            self.exp = insData['exp']
        self.templateinfo = dbCharacterFate.FATE_TEMPLATE.get(self.templateId)
        
    def InsertIntoDB(self,characterId,equip = -2,position = -1):
        '''在数据库中插入命格信息
        '''
        templateId = self.templateId
        self.id = dbCharacterFate.insertFateInfo(templateId, characterId,equip,position)
        if self.id:
            return True
        return False
    
    def destroyByDB(self):
        '''删除宠物在数据库中的数据'''
        result = dbCharacterFate.DelFateInfo(self.id)
        return result
        
    def getMaxExp(self):
        '''获取最大经验
        '''
        quality = self.templateinfo.get('quality')
        maxExp = quality*120*self.level
        return maxExp
    
    def addExp(self,exp):
        '''添加经验'''
        self.exp += exp
        self.updateExp(self.exp)
        
    def updateExp(self,exp):
        '''更新经验值
        '''
        status = 0
        while self.exp >= self.getMaxExp():
            self.exp -= self.getMaxExp()
            self.level += 1
            status = 1
        if status:
            self.updateFateInfo({'exp':self.exp,'level':self.level})
        else:
            self.updateFateInfo({'exp':self.exp})
    
    def getAllExp(self):
        '''获取该命格能贡献的所有经验'''
        quality = self.templateinfo.get('quality')
        baseexp = quality*30+self.exp
        level = self.level
        while level>1:
            baseexp += quality*120*level
            level -= 1
        return baseexp
    
    def updateFateInfo(self,prop):
        '''更新命格信息
        '''
        dbCharacterFate.updateFateInfo(self.id, prop)
        
    def fromatFateInfo(self):
        '''格式化命格信息
        '''
        info = {}
        info['id'] = self.id
        info['tempalteId'] = self.templateId
        info['name'] = self.templateinfo.get('name')
        info['desc'] = self.templateinfo.get('desc')
        info['icon'] = self.templateinfo.get('icon')
        info['type'] = self.templateinfo.get('type')
        info['quality'] = self.templateinfo.get('quality')
        info['level'] = self.level
        info['exp'] = self.exp
        info['maxExp'] = self.getMaxExp()
        info['price'] = self.templateinfo.get('price')
        return info
        
    def SerializationFateInfo(self,bearer):
        '''序列化命格信息
        '''
        info = self.fromatFateInfo()
        bearer.xyId = info.get('id')
        bearer.xytemId = info.get('tempalteId')
        try:
            bearer.xyName = info.get('name')
        except:
            bearer.xyName = info.get('name').decode('utf8')
        desc = self.getDesc()
        try:
            bearer.xyDes = desc
        except:
            bearer.xyDes = desc.decode('utf8')
        bearer.icon = info.get('icon')
        bearer.type = info.get('type')
        bearer.exp = info.get('exp')
        bearer.quality = info.get('quality')
        bearer.level = info.get('level')
        bearer.maxexp = info.get('maxExp')
        bearer.price = info.get('price')
        return bearer
    
    def getDesc(self):
        '''获取自身的描述
        '''
        level = self.level
        desc = self.templateinfo.get('desc')
        effectstr = self.templateinfo.get('effectstr')
        effect = eval(effectstr)
        if effect:
            try:
                desc = desc+"+%d"%(effect.values()[0])
            except:
                pass
        return desc
        
    def getFateAttr(self):
        '''获取命格属性
        '''
        level = self.level
        effect = eval(self.templateinfo.get('effectstr'))
        return effect
        
        