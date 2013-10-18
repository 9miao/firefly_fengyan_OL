#coding:utf8
'''
Created on 2011-4-14

@author: sean_lan
'''
from app.scense.component.Component import Component
from app.scense.core.PlayersManager import PlayersManager
from app.scense.core.Card import Card
from twisted.internet import reactor
from app.scense.applyInterface import dropout
from app.scense.netInterface.pushObjectNetInterface import pushApplyMessage
from app.scense.applyInterface import instance_app

from app.scense.utils.dbopera import dbVIP
from app.scense.serverconfig.chatnode import chatnoderemote 
from app.scense.protoFile.fight import TurnOneCard_pb2,showAllCards_pb2,TurnAllCards_pb2
from app.scense.core.instance.InstanceGroupManage import InstanceGroupManage
from app.scense.core.language.Language import Lg


reactor = reactor
CARD_NUM =5#默认为10张
TURNCUS = 2 #翻牌子默认消耗
cuts=1000000 #掉落基数

def pushTurnOneCardMessage(characterId,nickname,cardId,sendList,topicID = 706):
    '''推送翻开一张卡牌的消息'''
    response = TurnOneCard_pb2.TurnOneCard()
    response.characterId = characterId
    response.cardId = cardId+1
    response.nickname = nickname
    msg = response.SerializeToString()
    pushApplyMessage(topicID, msg, sendList)
    
def pushTurnAllCardMessage(sendList,topicID = 708):
    '''推送翻开所有卡牌的消息'''
    response = TurnAllCards_pb2.TurnAllCards()
    response.signal = 1
    msg = response.SerializeToString()
    pushApplyMessage(topicID, msg, sendList)

def pushShowAllCards(sendList):
    '''推送显示所有牌子的信息'''
    response = showAllCards_pb2.showAllCards()
    response.signal = 1
    msg = response.SerializeToString()
    pushApplyMessage(709,msg,sendList)

class SceneCardComponent(Component):
    '''场景卡片组件'''
    def __init__(self,owner,cardNum = CARD_NUM):
        '''
        @param cardNum: 场景中卡片的数量
        '''
        Component.__init__(self, owner)
        self._cards = {}
        self._IsShowed = 0    #卡片是否已经展现
        self._AreAllTurned = 0 #卡牌是否已经全部翻过了
        self._AllShowed = 0 #卡片是否已经全部显示了
        self._showAllTimer = None
        self.playersTurned = [] #已经翻过牌子的角色的id list
        self.playersGet = [] #已经获取过牌子的角色的id list
        self._cardsNum = cardNum
        self.cardsTurned = []
        
    def initCards(self,instanceid,dropoutid,cardNum):
        '''初始化卡片组
        @param instanceid: int 副本id
        @param dropoutid: int 掉落id
        @param cardNum: int 卡片数量
        '''
        self._IsShowed = 0
        dropoutdata=dropout.getByDropOutByid(dropoutid)
        if not dropoutdata:
            raise u'没有掉落数据'
        for cardId in range(cardNum):
            dropInfo = dropoutdata[cardId]
            card = Card(id=cardId, coin= dropInfo.get('coin',0),\
                         coupon= dropInfo.get('coupon',0),itemBound=dropInfo.get('item'))
            self._cards[card.getID()] = card
    
    def changeIsShowed(self):
        '''更改是否展现的状态'''
        self._IsShowed = 1
        
    def changeAreAllTurned(self):
        '''更改是否全部翻转的状态'''
        self._AreAllTurned = 1
        
    def IsShowed(self):
        '''是否已经展现'''
        return self._IsShowed
    
    def pushShow(self):
        ''''''
        if self._AreAllTurned:
            return
        self.changeAreAllTurned()
        sendList = []
        playersList = []
        for scence in self._owner._Scenes.values():
            playersList.extend(scence._playerlist)
        playersList = set(playersList)
        for characterId in playersList:
            if characterId in self.playersGet:
                pl = PlayersManager().getPlayerByID(characterId)
                #副本通关任务的处理
                if pl:
                    pl.quest.clearance(self._owner._id)
                    sendList.append(pl.dynamicId)
            else:
                pass
#        reactor.callLater(15,self.TurnAllCard)
        if not self._AllShowed:
            pushShowAllCards(sendList)
            self._AllShowed = 1
            
    def TurnAllCard(self):
        '''将所有的牌翻转'''
        playersList = []
        sendList = []
        for scence in self._owner._Scenes.values():
            playersList.extend(scence._playerlist)
        playersList = set(playersList)
        for characterId in playersList:
            if characterId in self.playersGet:
                pl = PlayersManager().getPlayerByID(characterId)
                #副本通关任务的处理
                if pl:
                    pl.quest.clearance(self._owner._id)
                if pl:
                    sendList.append(pl.dynamicId)
            else:
                pass
        for key in self._cards.keys():
            self._cards[key].changeIsTurned()
        pushTurnAllCardMessage(sendList)
            
    def getAllCardInfo(self,characterId):
        '''获取所有卡片的信息'''
        from app.scense.applyInterface import defencelog_app
        data = []
        for card in self._cards.values():
            data.append(card.formatCardInfo())
        if not self._showAllTimer:
            self._showAllTimer = reactor.callLater(10,self.pushShow)
        
        self.changeIsShowed()
        self.playersGet.append(characterId)
        playersList = []
        for scence in self._owner._Scenes.values():
            playersList.extend(scence._playerlist)
        playersList = list(set(playersList))
        if self.playersGet == playersList:
            try:
                self._showAllTimer.cancel()
            except Exception,e:
                pass
            reactor.callLater(1,self.pushShow)
        player=PlayersManager().getPlayerByID(characterId)
        instanceid=player.baseInfo.getInstanceid()
        groupid=InstanceGroupManage().getFristInstanceBy(instanceid)
        instance_app.addInstance_record(characterId, groupid)#副本组通关记录
        instance_app.addInstance_record_id(characterId, instanceid) #副本通关记录
#        defencelog_app.ClearanceOperate(instanceid, characterId, True)#给殖民领主添加通关记录
        return {'result':True,'data':data}
    
    def turnCard(self,characterId,nickname,cardId):
        '''副本结束翻牌
        @param characterId: int 角色的id
        @param cardId: int 卡牌的id
        '''
        player = PlayersManager().getPlayerByID(characterId)
        pushcnt = self.playersTurned.count(characterId)
        nowpushcnt = pushcnt + 1
        viplevel = player.baseInfo.getType()
#        dbVIP.vipCertification('cardnum', viplevel,nowtimes = pushcnt)
        if not dbVIP.vipCertification('cardnum', viplevel,nowtimes = nowpushcnt):
            reactor.callLater(0.5,self.TurnAllCard)
        if nowpushcnt>=2:
            cus = pushcnt*TURNCUS
            reGold = player.finance.getGold()- cus
            if reGold<0:
                return {'reslt':False,'message':Lg().g(190)}
            player.finance.updateGold(reGold)
            
        card = self._cards[cardId]
        if card.IsTurned():
            return {'result':False,'message':Lg().g(279)}
        card.changeIsTurned()
        sendList = []
        playersList = []
        for scence in self._owner._Scenes.values():
            playersList.extend(scence._playerlist)
        playersList = set(playersList)
        for characterId in playersList:
            pl = PlayersManager().getPlayerByID(characterId)
            if pl:
                sendList.append(pl.dynamicId)
        dropItem = card.itemBound
        coin = card.coin
        if dropItem:
            player.pack.putNewItemInPackage(dropItem)
            self.pushJipinInfo(player,dropItem)
        else:
            player.finance.addCoin(coin)
        self.playersTurned.append(characterId)
        pushTurnOneCardMessage(characterId,nickname,cardId, sendList)
        
        return {'result':True,'message':Lg().g(280)}
            
    
    def pushJipinInfo(self,player,dropItem):
        '''推送获取极品物品的消息'''
        itemlist = [20030049,20030050,20030062,20030064]
        tempid = dropItem.baseInfo.getItemTemplateId()
        quality = dropItem.baseInfo.getBaseQuality()
        if tempid not in itemlist or quality < 6:
            return
        UnionTypeStr = player.guild.getUnionTypeStr()+Lg().g(129)
        palyername = player.baseInfo.getName()
        hardinfo = {1:Lg().g(281),2:Lg().g(282),3:Lg().g(283)}.get(self._owner._hard)
        instansname = self._owner._name +"-"+ hardinfo
        itemrichname = dropItem.baseInfo.getRichName()
        msg = Lg().g(284)%(UnionTypeStr,palyername,
                                          instansname,itemrichname)
        chatnoderemote.callRemote('pushSystemToInfo',msg)
            
    
    
            