#coding:utf8
'''
Created on 2012-9-20
消费监控
@author: Administrator
'''
from app.scense.core.singleton import Singleton
from app.scense.core.language.Language import Lg
import datetime

from app.scense.utils.dbopera import dbBill

class ConsMonitor:
    '''消费管理类
    '''
    
    __metaclass__ = Singleton
    
    def __init__(self):
        '''初始化消费记录列表
        '''
        self.consRecords = [] #聊天记录
        
    def addConsRecord(self,characterId,consType,consGold,consDesc,itemId):
        '''添加一条消费记录
        @param characterId: int 角色的ID
        @param consType: int 角色的消费类型
        1.祈祷N次总消费XX钻
        2.在商城中购买YYYY消费XXX钻
        3.竞技场消费XX钻，消耗冷却时间
        4.宠物商店刷新宠物消费XXX钻
        5.铁矿洞中立即完成N次消费XXX钻
        6.国升级军徽N次消费XX钻
        7.购买活力值N次消费XX钻
        8.宠物培养N次消费XX钻
        9.军营中立即完成X次消费XX钻
        10.军营中加急训练N次消费XX钻
        11.铁矿洞点石成金N次消费XX钻
        12.其他消费XX钻
        @param consGold: int 角色消费的钻数
        @param consDesc: str 角色的消费说明
        @param itemId: int 关联到的物品的ID
        '''
        if consType==1:
            consDesc = Lg().g(661)%(consGold)
        elif consType==2:
            from app.scense.utils import dbaccess
            iteminfo = dbaccess.all_ItemTemplate.get(itemId)
            if not iteminfo:
                itemname = '????'
            else:
                itemname = iteminfo.get('name','????')
            consDesc = Lg().g(662)%(itemname,consGold)
        elif consType==3:
            consDesc = Lg().g(663)%(consGold)
        elif consType==4:
            consDesc = Lg().g(664)%(consGold)
        elif consType==5:
            consDesc = Lg().g(665)%(consGold)
        elif consType==6:
            consDesc = Lg().g(666)%(consGold)
        elif consType==7:
            consDesc = Lg().g(667)%(consGold)
        elif consType==8:
            consDesc = Lg().g(668)%(consGold)
        elif consType==9:
            consDesc = Lg().g(669)%(consGold)
        elif consType==10:
            consDesc = Lg().g(670)%(consGold)
        elif consType==11:
            consDesc = Lg().g(671)%(consGold)
        args = (characterId,consType,consGold,consDesc,str(datetime.datetime.now()),itemId)
        self.consRecords.append(args)
        
    def insertConsRecord(self):
        '''记录消费记录
        '''
        valuelist = []
        while self.consRecords:
            args = self.consRecords.pop()
            msgstr = "(%d,%d,%d,'%s','%s',%d),"%args
            valuelist.append(msgstr) 
        valueStr = ''.join(valuelist)
        valueStr = valueStr[:-1]
        if valueStr:
            dbBill.InsertRecords(valueStr)
        
    
        
        
        
        
        
        