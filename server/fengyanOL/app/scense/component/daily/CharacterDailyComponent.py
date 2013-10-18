#coding:utf8
'''
Created on 2012-5-3
角色每日任务
@author: Administrator
'''
from app.scense.component.Component import Component
from app.scense.utils.dbopera import dbdaily
from app.scense.utils import dbaccess
from app.scense.core.Item import Item
import datetime
from app.scense.core.language.Language import Lg
"""
1=角色等级(升级触发)
2=国等级
3=宠物等级
4=加入国
5=杀死怪物
6=通关副本
7=穿戴装备
8=强化装备
9=获得道具
10=得到宠物
11=开启技能
12=技能等级
13=使用道具
14=收集道具
15=结交好友
16=完成任务
17=神格开启
18=爵位升级
19=收集宠物图鉴
20=使用矿洞
21=探宝次数
22=军营训练
23=抢夺副本
24=培养宠物次数
"""

class CharacterDailyComponent(Component):
    '''角色每日任务
    '''
    
    def __init__(self,owner):
        '''初始化
        @param dailygoal: dict 角色每日目标
        '''
        Component.__init__(self, owner)
        self.dailygoal = {}
        self.initDaily()
        
    def initDaily(self):
        '''初始化每日目标
        '''
        characterId = self._owner.baseInfo.id
        data = dbdaily.getCharacterAllDaily(characterId)
        for daily in data:
            info = {}
            info['current'] = daily[3]
            info['received'] = daily[4]
            self.dailygoal[daily[2]] = info
        
    def noticeDaily(self,dailytype,associatedId,count):
        '''目标通知
        @param dailytype: int 目标类型
        @param associatedId: int 关联的ID
        @param count: int 变更的数量
        '''
        dailylist = dbdaily.getDailyForToday(dailytype,self._owner.creatTime)#符合今日的目标
        characterId = self._owner.baseInfo.id
        if not dailylist:
            return
        for daily in dailylist:
            if daily['dailytype']!=dailytype or (associatedId !=0 and associatedId !=daily['associatedId']):
                continue
            if not self.dailygoal.has_key(daily['id']):
                self.dailygoal[daily['id']] = {'current':0,'received':0}
                dbdaily.insertCharacterDaily(characterId, daily['id'])
            mydaily = self.dailygoal.get(daily['id'])
            if count<0:
                count = mydaily['current']-count
            if mydaily['current']<daily['goal']:
                mydaily['current'] = min(count,daily['goal'])
                dbdaily.updateCharacterDaily(characterId, daily['id'], {'current':mydaily['current']})
    
    def checkFinished(self,dailyID):
        '''检测是否完成
        @param dailyID: int 
        '''
        
        finished = False
        daily = dbdaily.ALL_DAILY.get(dailyID)
        createtime = self._owner.creatTime
        thisdate = datetime.date.today()
        daysdelta = (thisdate - createtime.date()).days+1
        if not self.dailygoal.has_key(daily['id']):
            characterId = self._owner.baseInfo.id
            self.dailygoal[daily['id']] = {'current':0,'received':0}
            dbdaily.insertCharacterDaily(characterId, daily['id'])
        if daysdelta < daily['dateindex']:#不能提前完成任务
            return False
        mydaily = self.dailygoal.get(dailyID)
        if daily['dailytype']==2 and daysdelta >= daily['dateindex']:
            if self._owner.guild.getGuildLevel()>=daily['goal']:
                finished = True
        else:
            if mydaily and mydaily['current']>=daily['goal']:
                finished = True
        return finished
        
    def receiveBound(self,dailyId):
        '''领取奖励
        @param dailyId: int 目标ID
        '''
        dailyInfo = dbdaily.ALL_DAILY.get(dailyId)
        if not dailyInfo:
            return {'result':False,'message':Lg().g(285)}
        if not self.checkFinished(dailyId):
            return {'result':False,'message':Lg().g(286)}
        mydaily = self.dailygoal.get(dailyId)
        if mydaily['received']:
            return {'result':False,'message':Lg().g(287)}
        expbound = dailyInfo.get('expbound')
        coinbound = dailyInfo.get('coinbound')
        goldbound = dailyInfo.get('goldbound')
        itembound = eval('[%s]'%dailyInfo.get('itembound'))
        spacerequired = len(itembound)
        if self._owner.pack._package._PropsPagePack.findSparePositionNum()<spacerequired:
            return {'result':False,'message':Lg().g(16)}
        self._owner.level.addExp(expbound)
        self._owner.finance.addCoin(coinbound)
        self._owner.finance.addGold(goldbound)
        for item in itembound:
            self._owner.pack.putNewItemsInPackage(item[0],item[1])
        self.dailygoal[dailyId]['received'] = 1
        dbdaily.updateCharacterDaily(self._owner.baseInfo.id, dailyId, {'received':1})
        return {'result':True,'message':Lg().g(288)}
        
    def getDailyInfo(self,dateindex):
        '''获取指定日期的目标
        @param dateindex: int 日期序号
        '''
        dailylist = dbdaily.getDailyForDateindex(dateindex)
        dailylistInfo = []
        dailylistInfo
        for daily in dailylist:
            info = {}
            info['dailyId'] = daily['id']
            info['name'] = daily['dailyname']
            info['desc'] = daily['dailydesc']
            info['type'] = daily['type']
            info['icon'] = daily['icon']
            info['finished'] = self.checkFinished(daily['id'])
            mydaily = self.dailygoal.get(daily['id'])
#            info
#            if daily['dailytype']==2:
#                if self._owner.guild.getGuildLevel()>=daily['goal']:
#                    info['finished'] = True
#            else:
#                if mydaily and mydaily['current']>=daily['goal']:
#                    info['finished'] = True
            info['received'] = bool(mydaily['received'])
            info['expbound'] = daily['expbound']
            info['coinbound'] = daily['coinbound']
            info['goldbound'] = daily['goldbound']
            info['itembound'] = []
            bounditems = eval('[%s]'%daily('itembound'))
            for info in bounditems:
                item = Item(itemTemplateId = info[0])
                item.pack.setStack(info[1])
            dailylistInfo.append(info)
        return dailylistInfo
            
    def getAllDailyInfo(self):
        '''获取所有的每日目标
        '''
        alldailysinfo = []#每日的目标列表信息
        dbdaily.DAILY_INDEX.keys().sort()
        for dateindex in dbdaily.DAILY_INDEX.keys():
            dateInfo = {}#每一天的目标列表信息
            dateInfo['isOpenFlag']= True
            dateInfo['isSucFlag'] = True
            dateInfo['dayListTaskInfo'] = []
            for daily in dbdaily.DAILY_INDEX.get(dateindex):
                info = {}
                info['taskId'] = daily['id']
                info['icon'] = unicode(daily['icon'])
                info['taskDes'] = daily['dailydesc']
                mydaily = self.dailygoal.get(daily['id'])
                if self.checkFinished(daily['id']):
                    info['isCompleteFlag'] = True
                else:
                    info['isCompleteFlag'] = False
                    dateInfo['isSucFlag'] = False
                if mydaily and mydaily['received']:
                    info['isObtainFlag']=True
                else:
                    info['isObtainFlag']=False
                info['rewardInfo'] = []
                if daily['expbound']:
                    bound = {}
                    bound['rewardType'] = 4
                    bound['stack'] = daily['expbound']
                    info['rewardInfo'].append(bound)
                if daily['coinbound']:
                    bound = {}
                    bound['rewardType'] = 1
                    bound['stack'] = daily['coinbound']
                    info['rewardInfo'].append(bound)
                if daily['goldbound']:
                    bound = {}
                    bound['rewardType'] = 2
                    bound['stack'] = daily['goldbound']
                    info['rewardInfo'].append(bound)
                for itemId,stack in eval("[%s]"%daily['itembound']):
                    bound = {}
                    bound['itemId'] = itemId
                    iteminfo = dbaccess.all_ItemTemplate.get(itemId)
                    bound['icon'] = iteminfo.get('icon',0)
                    bound['stack'] = stack
                    bound['type'] = iteminfo.get('type',0)
                    bound['rewardType'] = 0
                    info['rewardInfo'].append(bound)
                dateInfo['dayListTaskInfo'].append(info)
            alldailysinfo.append(dateInfo)
        return {'result':True,'data':alldailysinfo}
                    
                    
             
        
        
