#coding:utf8
'''
Created on 2011-3-24

@author: sean_lan
'''

from app.scense.utils import dbaccess
from app.scense.utils.dbopera import dbCharacter
from app.scense.component.Component import Component
from app.scense.netInterface.pushPrompted import pushPromptedMessage
from app.scense.netInterface import pushObjectNetInterface
from app.scense.core.language.Language import Lg

class CharacterFinanceComponent(Component):
    '''
    finance component for character
    '''
    MAXCOIN = 99999999
    
    def __init__(self,owner,coin=0,gold=0,coupon=0,contribution = 0,prestige=0,morale=0):
        '''
        Constructor
        '''
        Component.__init__(self,owner)
        self._coin = coin #角色的金币
        self._gold = gold #角色的钻
        self._coupon = coupon #角色的礼券
        self._prestige=prestige #当前威望值
        self._morale=morale #当前斗气值
        
    def getPrestige(self):#获得威望值
        return self._prestige
    
    def setPrestige(self,val):#设置威望值（限初始化使用）
        self._prestige=val
    
    def updatePrestige(self,val,state=1):#设置威望值
        if self._prestige<val:
            msg = Lg().g(307)%abs(val-self._prestige)
        else:
            msg = Lg().g(308)%abs(val-self._prestige)
        self._prestige=val
#        dbaccess.updateCharacter(self._owner.baseInfo.id, 'prestige', val)
        pushObjectNetInterface.pushUpdatePlayerInfo(self._owner.getDynamicId())
        if state:
            pushPromptedMessage( msg, [self._owner.getDynamicId()])
        else:
            self._owner.msgbox.putFightMsg(msg)#将消息加入战后消息处理中
            
    def addPrestige(self,val,state=1):
        """添加威望
        """
        prestige = self._prestige + val
        self.updatePrestige(prestige,state = state)
        
    
    def getMorale(self):#获得当前斗气值
        return self._morale
    
    def setMorale(self,val):#设置斗气值(限初始化使用)
        self._morale=val
        
    def updateMorale(self,val,state=1):#设置斗气值
        if self._morale<val:
            msg = Lg().g(309)%abs(val-self._morale)
        else:
            msg = Lg().g(310)%abs(val-self._morale)
        self._morale=val
#        dbaccess.updateCharacter(self._owner.baseInfo.id, 'morale', val)
        pushObjectNetInterface.pushUpdatePlayerInfo(self._owner.getDynamicId())
        if state:
            pushPromptedMessage( msg, [self._owner.getDynamicId()])
        else:
            self._owner.msgbox.putFightMsg(msg)#将消息加入战后消息处理中
    
    def updateAddMorale(self,val,state=False):#添加斗气值
        '''添加斗气值
        @param val: int 添加的斗气数量
        @param state: bool  true战后提示，False马上提示
        '''
        msg = Lg().g(309)%abs(val)
        
        self._morale+=val
        pushObjectNetInterface.pushUpdatePlayerInfo(self._owner.getDynamicId())
        if state:
            pushPromptedMessage( msg, [self._owner.getDynamicId()])
        else:
            self._owner.msgbox.putFightMsg(msg)#将消息加入战后消息处理中
    
    def addMorale(self,val,state=1):
        """添加或扣除斗气
        """
        morale = self._morale + val
        self.updateMorale(morale,state = state)
    
        
        
    #--------------------------coin------------------
    def getCoin(self):
        return self._coin
    
    def setCoin(self,coin):
        self._coin = coin
        
    
    def updateCoin(self,coin,state=1):
        if coin ==self._coin:
            return
        if coin-self._coin>0:
            msg = Lg().g(311)%abs(coin-self._coin)
        else:
            msg = Lg().g(312)%abs(coin-self._coin)
        if coin>= self.MAXCOIN:
            msg = msg.join(["\n",Lg().g(313)])
            self._coin = self.MAXCOIN 
        else:
            self._coin = coin
#        dbaccess.updateCharacter(self._owner.baseInfo.id, 'coin', self._coin)
        pushObjectNetInterface.pushUpdatePlayerInfo(self._owner.getDynamicId())
        if state:
            pushPromptedMessage( msg, [self._owner.getDynamicId()])
        else:
            self._owner.msgbox.putFightMsg(msg)#将消息加入战后消息处理中
        
    def addCoin(self,coin,state = 1):
        coin = self._coin + coin
        self.updateCoin(coin,state = state)
    
    #--------------------------gold------------
    def getGold(self):
        return self._gold
    
    def reloadGold(self,gold):
        '''重新读取角色钻数量'''
        addgold = dbCharacter.getRepurchaseGold(self._owner.baseInfo.id)
        self._gold = gold
        if addgold:
            #判断首次充值
            if self._owner.level.getVipExp()<=90 and self._owner.baseInfo.getType()==0:
                self.doFirstRechargeBound()
            self.Recharge(int(addgold))
            
    def updateRecharge(self):
        '''更新角色的充值信息
        '''
        addgold = int(dbCharacter.getRepurchaseGold(self._owner.baseInfo.id))
        if addgold:
            #判断首次充值
            if self._owner.level.getVipExp()<=90 and self._owner.baseInfo.getType()==0:
                self.doFirstRechargeBound()
            self.Recharge(int(addgold))
    
    def setGold(self,gold):
        delta = self._gold - gold
        if delta>0:
            self._owner.quest.UseGold(delta)
        self._gold = gold
        
    def updateGold(self,gold,state=1):
        delta = self._gold - gold
        if not delta:
            return
        if delta<0:
            msg = Lg().g(314)%abs(delta)
        else:
            msg = Lg().g(315)%abs(delta)
        if delta>0:
            self._owner.quest.UseGold(delta)
        self._gold = gold
        dbaccess.updateCharacter(self._owner.baseInfo.id, 'gold', gold)
        pushObjectNetInterface.pushUpdatePlayerInfo(self._owner.getDynamicId())
        if state:
            if msg:
                pushPromptedMessage(msg, [self._owner.getDynamicId()])
        else:
            self._owner.msgbox.putFightMsg(msg)#将消息加入战后消息处理中
            
    def doFirstRechargeBound(self):
        '''首次充值奖励
        '''
        package = self._owner.pack._package.getPackageByType(1)
        nowsize = package.getSize()+1
        package.setSize(nowsize)
        dbaccess.updatePlayerInfo(self._owner.baseInfo.id, {'packageSize':nowsize})
        self._owner.pack.putNewItemsInPackage(20700071,1)#添加首充礼包
        
            
    def Recharge(self,gold):
        '''充值钻
        '''
        if gold==0:
            return
        self.addGold(gold)
        self._owner.level.addVipExp(gold)#添加VIP经验
        
    def consGold(self,consGold,consType,consDesc='',itemId=0):
        '''金币消耗
        @param consGold: int 消耗的金币的数量
        @param consType: int 消耗的行为类型
        @param consDesc: str 消耗的描述
        @param itemId: int 相关物品的ID
        1.祈祷
        2.在商城中购买
        3.竞技场消费
        4.宠物商店刷新
        5.铁矿洞中立即完成
        6.国升级军徽
        7.购买活力值
        8.宠物培养
        9.军营中立即完成
        10.军营中加急训练
        11.铁矿洞点石成金
        12.其他
        '''
        from app.scense.core.ConsMonitor import ConsMonitor
        characterId = self._owner.baseInfo.id
        ConsMonitor().addConsRecord(characterId, consType, consGold, consDesc,itemId)
        self.addGold(-consGold)
        
    def addGold(self,gold):
        if gold<0:
            self._owner.quest.UseGold(-gold)
        nowgold = self._gold +gold
        if nowgold<0:
            return False
        self.updateGold(nowgold)
        return True
#        dbaccess.updateCharacter(self._owner.baseInfo.id, 'gold', self._gold)
        
    #--------------------------coupon--------------
    def getCoupon(self):
        return self._coupon
    
    def setCoupon(self,coupon):
        self._coupon = coupon
        
    def updateCoupon(self,coupon):
        self._coupon = coupon
        msg = u'消耗礼券%d'%(coupon-self._coin)
        dbaccess.updateCharacter(self._owner.baseInfo.id, 'coupon', coupon)
        pushPromptedMessage(msg, [self._owner.getDynamicId()])
        

    def goldConsignment(self,goldNum,coinPrice):
        '''閲戝竵瀵勫崠
        @param goldNum: int 瀵勫崠鐨勬暟閲�
        @param coinPrice: int 瀵勫崠鐨勪环鏍硷紙鍗曚环锛�
        '''
        if self.getGold()<goldNum:
            return {'result':False,'message':u'閲戝竵浣欓涓嶈冻'}
        result = dbaccess.goldConsignment(self._owner.baseInfo.getId(), goldNum, coinPrice)
        if result:
            self.updateGold(self.getGold()-goldNum)
            return {'result':True,'message':u'瀵勫敭鎴愬姛'}
        return {'result':False,'message':u'瀵勫敭澶辫触'}
        