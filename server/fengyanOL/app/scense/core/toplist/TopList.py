#coding:utf8
'''
Created on 2011-9-15

@author: SIOP_09
'''
from app.scense.core.singleton import Singleton
from app.scense.utils.dbopera import dbCharacter
from app.scense.utils.dbopera import dbTopitem
from app.scense.utils.dbopera import dbGuild
from app.scense.utils.dbopera import dbCharacterTop
from app.scense.core.PlayersManager import PlayersManager
import  datetime,time
from app.scense.core.language.Language import Lg

class TopList:
    '''排行榜单列模式'''
    __metaclass__ = Singleton

    def __init__(self):
        self.plevel=[] #角色等级排行榜
#        self.pfinance=[] #财富排行榜
#        self.pcredit=[] #声望排行榜
        self.pbattle=[] #战斗力排行榜
        
        self.glevel=[] #行会等级排行榜
        self.gstrength=[] #行会实力排行榜
        self.updatetime="" #最后更新时间
        
#        self.iarm=[] #武器排行榜
#        self.iaccouter=[] #装备排行榜
#        self.iadorn=[] #饰品排行榜
        self.onlypl={} #个人当前等级排名
        self.onlypb={} #个人当前战力排名
        self.onlygl={} #个人当前行会等级排名
        self.onlygs={} #个人当前行会实例排名
        self.into()
        
    def into(self):
        '''初始化数据'''
#        self.updateiaitem(0)
#        self.updateiaitem(1)
#        self.updateiaitem(2)
        self.updateAll()#更新所有排行
        #print '等级的排行数量：'+str(len(self.plevel))
    
    
    
    def updateAll(self):
        '''更新所有排行'''
#        self.updateiaitem(0)
#        self.updateiaitem(1)
#        self.updateiaitem(2)
        self.updatepcharacter(0)
        self.updatepcharacter(3)
        self.updateGuild(1)
        self.updateGuild(2)
        self.updatetime=str(time.strftime(Lg().g(585),time.localtime(time.time()))) #系统当前时间
        flg=0
        for it in dbGuild.getTopAll(1): #国等级排名
            flg+=1
            self.onlygl[it[0]]=flg
        flg=0
        for it in dbGuild.getTopAll(2):#国实力排名
            flg+=1
            self.onlygs[it[0]]=flg
        flg=0
        for it in dbCharacterTop.getTopListAll(): #角色武力排名
            flg+=1
            self.onlypb[it[0]]=flg
        flg=0
        for it in dbCharacter.getTopAll(0): #角色等级排名
            flg+=1
            self.onlypl[it[0]]=flg
            
    
    def updateGuild(self,typeid):
        '''更新行会排行数据
        @param typeid: int 1国等级 2国实力
        '''
        resu=dbGuild.getTop100(typeid)
        if not resu or len(resu)<1:
                return{'result':False,'message':Lg().g(586),'data:':None}
        if typeid==1:
            self.glevel=resu
        elif typeid==2:
            self.gstrength=resu
    def updateiaitem(self,typeid):
        '''更新物品排行数据
        @param typeid: 物品类型   0武器 1装备 2饰品
        @param page: 当前页数
        @param counts: 每页记录数
        '''
        resu=dbTopitem.getTop(typeid) #flist=['itemid','marks','profession','name','guildname']
        if not resu or len(resu)<1:
            return{'result':False,'message':Lg().g(587),'data:':None}
        if typeid==0:
            self.iarm=resu
        elif typeid==1:
            self.iaccouter=resu
        elif typeid==2:
            self.iadorn=resu
            
    def upateAddzl(self):
        ''''''
        dbCharacterTop.delTop()#删除所有排行信息成功
        battleList=dbCharacter.getCharacterBattleAll() #获取所有角色战斗力
        if not dbCharacterTop.addTopList(battleList):#添加角色战力到战力排行榜表
            #print '添加角色战力到战力表排行时失败！'
            return
    
    def updatepcharacter(self,typeid):
        '''更新角色排行数据
        @param typeid: int 0玩家等级排行  1游戏币排行  2声望排行   3综合战斗力排行
        '''
        if typeid==3: #更新角色战力排行榜数据
#            dbCharacterTop.delTop()#删除所有排行信息成功
#            battleList=dbCharacter.getCharacterBattleAll() #获取所有角色战斗力
#            if not dbCharacterTop.addTopList(battleList):#添加角色战力到战力排行榜表
#                #print '添加角色战力到战力表排行时失败！'
#                return
            self.pbattle=dbCharacterTop.getTopList()
            return
        resu=dbCharacter.getTop100(typeid)
        if len(resu)<1:
            return{'result':False,'message':Lg().g(588),'data:':None}
        if typeid==0:
            self.plevel=resu
        elif typeid==1:
            self.pfinance=resu
        elif typeid==2:
            self.pcredit=resu
        
        
    def getTop(self,id,ranking):
        '''获取排行榜数据
        @param id: int 当前角色id
        @param ranking: int 排行分类类型  1角色等级排行  2个人战力排行  3国等级排行  4国战力排行
        '''
        data=[] #排行榜中显示的排行
        date={} #当前角色的排行
#        player=PlayersManager().getPlayerByID(id)
#        nickname=player.baseInfo.getNickName()
            
        if ranking==1:#等级榜
            data=self.plevel
            date=self.onlypl.get(id)#  dbCharacter.getOneTopByNname(nickname, 0)
        elif ranking==2:#武力排行榜
            data=self.pbattle
            date=self.onlypb.get(id)#dbCharacterTop.getMysely(nickname)
        elif ranking==3: #国等级
            data=self.glevel
            date=self.onlygl.get(id)#dbGuild.getTop100ByName(nickname, 1)
        elif ranking==4: #国实力
            data=self.gstrength
            date=self.onlygs.get(id)#dbGuild.getTop100ByName(nickname, 2)
        return data,date,self.updatetime