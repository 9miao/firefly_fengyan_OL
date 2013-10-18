#coding:utf8
'''
Created on 2012-5-16

@author: jt
'''
from app.scense.component.Component import Component
from app.scense.utils.dbopera import dbNobility,dbNobilityHistory,dbNobilityAstrict
from app.scense.applyInterface import configure
from twisted.python import log
from app.scense.core.language.Language import Lg

class CharacterNobility(Component):
    '''角色官爵属性
    '''


    def __init__(self,owner):
        '''
        Constructor
        '''
        Component.__init__(self, owner)
        self._level=1 #角色当前爵位等级
        self.owner=owner
        self.isgx=True #当天是否可以上交**获取威望
        self.istrue=True #当天是否可以领取俸禄
        self.counts=1#当天上交钻石次数
        self.sjwp=set([])#记录当天上交的物品 ['f1','f3','f5']代表
        
        astrictList=dbNobilityAstrict.getInfoBypid(self.owner.baseInfo.id)
        if astrictList:
            self.istrue=configure.NumbToBool(astrictList['istrue']) #当天是否可以领取俸禄
            sjlist=eval(astrictList['isgx'])#上交的贡献物品或者是对应的贡献
            self.sjwp=set(sjlist)
            if len(sjlist)==6:
                self.isgx=False #当天是否可以上交**获取威望
            self.counts=astrictList['counts']#上交钻石次数
    
    
    def ishdsw(self):
        '''是否获得过威望'''
        if self.counts>0 or len(self.sjwp)>0:
            return True
        else:
            return False
        
    def clear(self):
        '''清除所有限制'''
        self.isgx=True
        self.istrue=True
        self.counts=0
        self.sjwp=set([])
        
    
    def addSjWp(self,ids):
        '''威望任务，添加上交物品
        @param ids: str f1 f2 f3...
        '''
        ids=int(ids[1:2])
        self.sjwp.add(ids)
        if len(self.sjwp)<6:#如果上交的物品不足6种
            self.isgx=True
        else:
            self.isgx=False
    
    def isSJWP(self,idd):
        '''判断是否可以上交该物品完成威望任务
        @param idd: str f1 f2 f3
        '''
        idd=int(idd[1:2])
        if idd in self.sjwp:
            return False  #如果这个物品已经上交 则返回不可上交
        return True
    
    def dbupdate(self):
        '''下线记录'''
        istrue=configure.BoolToNumb(self.istrue)#当天是否可以领取俸禄
        sj="["  #记录当天上交的物品 
        for item in self.sjwp:
            sj+=str(item)+","
        if len(self.sjwp)>0:
            sj= sj[:-1]
        sj+="]"
        if dbNobilityAstrict.getInfoBypid(self.owner.baseInfo.id):#如果有记录
            flg=dbNobilityAstrict.updateInfo(self.owner.baseInfo.id, istrue, sj, self.counts)
        else:#如果没有记录
            flg=dbNobilityAstrict.add(self.owner.baseInfo.id, istrue, sj, self.counts)
        return flg
        
    def drawZuanShi(self,idd):
        '''贡献钻石获取威望
        @param idd: str 威望任务物品标识  f1 ,f2 f3
        '''
        ids=int(idd[1:2])
        if list(self.sjwp).count(ids)>0:
            return {'result':False,'message':Lg().g(371)}

        if not self.isgx:
            return {'result':False,'message':Lg().g(372)}
        c1=self.owner.finance.getGold()#角色钻数量
        c2=configure.guanjueZuan(self.counts+1)#需要花费钻的数量
        if c1>=c2:
            self.owner.finance.updateGold(c1-c2)
        else:
            return {'result':False,'message':Lg().g(190)}
        info=self.getNowInfo()#当前爵位信息
        if not info:
            return {'result':False,'message':Lg().g(373)}
        li=eval(info[idd]) #{0物品id,1物品名称,2物品数量，3获得贡献值数量]}
        ww=li[3]#获得威望  
        self.owner.finance.updatePrestige(ww+self.owner.finance.getPrestige())#更改威望值
        self.addSjWp(idd)
        self.counts+=1
        return {'result':True,'message':Lg().g(166)}
    
    def handin(self,idd):
        '''贡献物品获取威望
        @param idd: str 威望任务物品标识
        '''
        try:
            ids=int(idd[1:2])
            if list(self.sjwp).count(ids)>0:
                return {'result':False,'message':Lg().g(371)}
            
            if not self.isgx:
                return {'result':False,'message':Lg().g(372)}
            info=self.getNowInfo()#当前爵位信息
            if not info:
                return {'result':False,'message':Lg().g(373)}
            lli=eval(info[idd]) #[0物品id,1物品名称，2物品数量，3获得贡献值数量]
            ct=self.owner.pack._package._PropsPagePack.countItemTemplateId(lli[0])#物品的数量
            if ct<lli[2]:
                return {'result':False,'message':Lg().g(374)}
            ctt=self.owner.pack.delItemByTemplateId(lli[0],lli[2])
            if ctt!=1:
                return {'result':False,'message':Lg().g(375)}
            self.owner.finance.updatePrestige(lli[3]+self.owner.finance.getPrestige())#更改威望值
            self.addSjWp(idd)
        except:
            log.err(idd+"上交物品货物威望")
        self.owner.quest.specialTaskHandle(127)
        return {'result':True,'message':u'上交物品成功'}
    
    
    
    def setLevel(self,val):
        '''设置官爵等级（仅限内存，初始化使用）'''
        self._level=val
    
    def getLevel(self):
        '''获取当前爵位等级'''
        return self._level
        
    def getName(self):
        '''获取爵位名称'''
        info=dbNobility.all[self._level]#当前爵位名称
        if info:
            return info['names']
        else:
            return u''
        
    def getNowInfo(self):
        '''获得当前爵位信息'''
        info=dbNobility.all[self._level]#当前爵位信息
        if info:
            return info
        else:
            log.err(str(self._level))
            return None
        
    def getAttribute(self):
        attrinfo= self.getNowInfo().get('attribute','{}')
        return eval(attrinfo)
        
    def getNextInfo(self):
        '''获得下一爵位信息'''
        if dbNobility.all.has_key(self._level+1):
            info=dbNobility.all[self._level+1]#下一级爵位信息
            if info:
                return info
            else:
                return None
        else:
            return None
        
    def promote(self):
        '''升级爵位
        return bool
        '''
        info=self.getNextInfo()#下级爵位信息
        if not info:
            return False
        ww=info['prestige']#升爵位所需威望值
        nowww=self.owner.finance.getPrestige()#角色当前威望值
        if nowww>=ww:
            self.owner.finance.updatePrestige(nowww-ww)#更新威望值
            self._level+=1#内存更改爵位等级
#            dbaccess.updateCharacter(self._owner.baseInfo.id, 'NobilityLevel', self._level)#数据库更改爵位等级
            me=Lg().g(376)%self.getName()
            self.clear()#清除所有限制
            me=me.replace("\\\\", "\\")
            dbNobilityHistory.add(self._owner.baseInfo.id, me, self._level)
            self._owner.daily.noticeDaily(18,0,self._level)
            self._owner.quest.specialTaskHandle(128)
            return True
        else:
            return False
        
    def ispromote(self):
        '''判断当前角色是否可以升级爵位'''
        info=self.getNextInfo()#下级爵位信息
        if not info:
            return False
        ww=info['prestige']#升爵位所需威望值
        dj=info['dengji']#升级爵位所需要的等级
        nowlevel=self.owner.level.getLevel()#角色当前等级
        nowww=self.owner.finance.getPrestige()#角色当前威望值
        if nowww>=ww and nowlevel>=dj:
            return True
        return False
        
        
        
    def isdraw(self):
        '''判断当前角色现在可否领取俸禄'''
        return self.istrue
    
    def isDdd(self):
        '''判断今天是是否领取过俸禄'''
        return not self.istrue
    
    def isisgx(self):
        '''判断当前角色是否可以上交*获取威望'''
        return self.isgx
        
    def draw(self):
        '''领取俸禄
        return bool
        '''
        flg=self.isdraw()
        if not flg:
            return False
        info=self.getNowInfo()#当前爵位信息
        if not info :
            return False
        self.owner.finance.updateCoin(self.owner.finance.getCoin()+info['coin'])#修改角色金币
        self.owner.finance.updateMorale(self.owner.finance.getMorale()+info['morale'])#修改角色斗气
        self.istrue=False#设置当天不能领取俸禄
        self.owner.quest.specialTaskHandle(114)#特殊任务处理
        self.owner.schedule.noticeSchedule(10,goal = 1)
        return True
        
        
    def getHistory(self,pid,page,count=4):
        '''获取封爵历史
        @param pid: int 角色id
        @param page: int 当前页数
        @param count: int 每页数量
        '''
        li=dbNobilityHistory.getBypid(pid, page, count)
        ctime=[]#时间
        context=[]#内容
        val=li[0]
        if val:
            for item in val:
                context.append(item['context'])
                ctime.append(str(item['ctime']))
            return {'time':ctime,'context':context,'zong':li[1]}
        else:
            return None
        
    def getzuans(self):
        '''返回客户端这次点击贡献应该花费多少钻'''
        count=configure.guanjueZuan(self.counts+1)
        return count 
    
        

        