#coding:utf8
'''
Created on 2012-5-30

@author: jt
'''
from app.scense.component.Component import Component
from app.scense.applyInterface import configure
from app.scense.utils.dbopera import dbCharacterPet,dbPetShop, dbPetShopConfigure
import random,datetime,math
from app.scense.core.character.Pet import Pet

class PetWineshop(Component):
    '''宠物酒店
    '''


    def __init__(self,owner):
        '''初始化宠物酒店
        '''
        Component.__init__(self,owner)
        self.owner=owner
        self.pid=owner.baseInfo.id#角色id
        self.ctime=None#记录时间
        self.counts=0#秒数间隔（剩余秒数）
        self.shop1=[]#宠物商店 (存储4个宠物模板)#[[宠物模板id,宠物等级],[宠物模板id,宠物等级]]
        self.isoption=1#消费提示打开状态 1开启消费提示 -1 关闭消费提示
        self.cs=1#每天剩余免费次数
        self.xy=0#幸运值
        info=dbPetShop.getByid(self.pid)#剩余时间记录
        if info:
            self.ctime=info['ctime']
            self.counts=info['counts'] 
            self.xy=info['xy']
            self.isoption=info['ioption']
            self.cs=info['cs']
        self.getShop()
        
    def getsycs(self):
        '''获取每天剩余免费次数'''    
        if self.cs<0:
            self.cs=0
        return self.cs
    def addXy(self,count):
        '''增加幸运值
        @param count: int 增加的数量
        '''
        self.xy+=count
        
    def getShop(self):
        '''获取商店中的商品'''
        info=dbPetShop.getByid(self.pid)#获取宠物商店信息
        if info:#如果有这个角色
            petinfo=dbCharacterPet.PET_TEMPLATE
            shop1=eval(info['shop1'])#[[宠物模板id,宠物等级],[宠物模板id,宠物等级]]
            if len(shop1)>0:
                sho1list=[]
                for i in shop1:
                    sho1list.append([petinfo[i[0]],i[1]])
                self.shop1=sho1list#[宠物信息，宠物等级]
        else:
            self.suiji(10001)
            
    def getXyShopBylv(self,lv,page,count=4):
        '''根据npcid获取Xy兑换的宠物
        @param lv: int npcid
        @param page: int 当前页数
        @param count: int 每页记录数
        '''
        date=[]#返回的数据信息
        xy=dbCharacterPet.shopXy
        zongcount=float(len(xy))#总条数
        zong = math.ceil(zongcount/float(count))#总页数
        ic=(page-1)*count
        for i in range(4):
            if ic+i<zongcount:
                date.append(xy[ic+i])
        return {'zong':zong,'date':date}
    
    def getShopInfo(self,lv):
        '''根据npcid获取商店宠物信息'''
        return self.shop1
    
    def getPetConfigByLv(self,lv):
        '''根据npcid获取宠物推荐组合'''
        dd=dbPetShopConfigure.lists
        val=dd.get(1)
        return self.getconfigto(val)
       
            
            
    def getconfigto(self,val):
        '''工具相关'''
        data={}
        data['fashi']=[]
        data['zhanshi']=[]
        data['youxia']=[]
        fashil=eval(val['fashi'])
        for fs in fashil:
            pi=Pet(templateId=fs,level=1)#宠物信息
            data['fashi'].append(pi.formatPetInfo())#添加法师推荐的宠物信息
        zhanshil=eval(val['zhanshi'])
        for zs in zhanshil:
            pi=Pet(templateId=zs,level=1)#宠物信息
            data['zhanshi'].append(pi.formatPetInfo())#添加战士推荐的宠物信息
        youxial=eval(val['youxia'])
        for zs in youxial:
            pi=Pet(templateId=zs,level=1)#宠物信息
            data['youxia'].append(pi.formatPetInfo())#添加战士推荐的宠物信息
        return data
    
    def ishaveMb(self,id):
        '''商店里面是否有这个宠物的模板id'''
        for item in self.shop1:
            if item[0]['id']==id:
                return True
        return False
    
    
    def s42(self,dj,shopall,shopx):
        '''随机宠物内层1算法
            @param dj: int  #宠物等级  #1高级宠物  2中级宠物  3低级宠物
            @param shopall: {} 宠物商店
            @param shopx: [] 角色存储商店  self.shop1 
            @param result: bool  如果宠物商店中有宠物返回true  如果宠物商店中没有宠物返回false
        '''
        shop=shopall.get(dj) #宠物模板信息列表
        count=len(shop)
        if count>0:
            abs=random.randint(0,count-1)
            le=1#random.randint(1,5)   #宠物等级
            if self.ishaveMb(shop[abs]['id']):#如果商店中有这个宠物了
                if count>=4:
                    while(self.ishaveMb(shop[abs]['id'])):
                        abs=random.randint(0,count-1)
                else:
                    return False
            shopx.append([shop[abs],le])
            return True
        else:
            return False
            
    
    def s4(self,shopall,shopx):
        '''随机宠物内层1算法
            @param shopall: {} 宠物商店
            @param shopx: [] 角色存储商店  self.shop1
        '''
        l={1:[2,3],2:[3,1],3:[2,1]}
        del shopx[:len(self.shop1)]#清除原来的
        for i in range(4):
            dj=configure.getpetshopsuiji()#宠物等级  #1高级宠物  2中级宠物  3低级宠物
            result=self.s42(dj, shopall, shopx)
            if not result:#如果这个商店中没有宠物
                clist=l.get(dj)#[dj,dj]
                pdj=clist[0]#宠物等级    #1高级宠物  2中级宠物  3低级宠物
                r1=self.s42(pdj, shopall, shopx)
                if not r1:#如果这个商店中没有宠物
                    self.s42(clist[1], shopall, shopx)
                    
        
    def suiji(self,lv,istrue=False):
        '''随机四个宠物
        @param lv: int npcid
        @param istrue: bool  默认False True：表示刷新时间
        '''
        shopall=dbCharacterPet.shopAll
        self.s4(shopall, self.shop1)

        if istrue:
            self.ctime=datetime.datetime.now() #系统当前时间
            self.counts=configure.m(30)
        
    def isdraw(self):
        '''是否刷新宠物
        @param counts: int 距离秒数
        ''' 
        s=configure.getchaTime(self.ctime,self.counts)#与当前时间相差秒数
        if s==0:
            return True
        return False
    
    def getTime(self):
        '''获取商店剩余冷却时间'''
        if self.ctime:
            s=configure.getchaTime(self.ctime,self.counts)#与当前时间相差秒数
            return s
        else:
            return 0
        
        
    def add(self):
        '''添加或者修改商店冷去时间，返回剩余秒数
        @param counts: int 冷却秒数
        '''
        if self.ctime:
            tlist=configure.getchatimeTime(self.ctime,self.counts)
            ctime=tlist[1]#系统当前时间
            ss=tlist[0]#冷却持续时间
            if ss<1:
                self.counts=ss+configure.m(30)
                self.ctime=ctime
            return self.counts
        else:
            self.counts=configure.m(30)
            self.ctime=datetime.datetime.now()
            return self.counts
        
    def get3ShopToString(self):
        '''把商店列表信息装换成字符串信息,返回列表'''
        shop1='['
        shop2='['
        shop3='['
        
        for i in range(4):
            if len(self.shop1)==4:
                shop1+="[%s,%s]"%(self.shop1[i][0]['id'],self.shop1[i][1])
                if i!=3:
                    shop1+=","
#            if len(self.shop2)==4:
#                shop2+="[%s,%s]"%(self.shop2[i][0]['id'],self.shop2[i][1])
#                if i!=3:
#                    shop2+=","
#            if len(self.shop3)==4:
#                shop3+="[%s,%s]"%(self.shop3[i][0]['id'],self.shop3[i][1])
#                if i!=3:
#                    shop3+=","
        shop1+=']'
        shop2+=']'
        shop3+=']'
        return [shop1,shop2,shop3]
    
    def dbupdate(self):
        '''下线处理中，将信息记录到数据库中'''
        
        li=self.get3ShopToString()
        tlist=configure.getchatimeTime(self.ctime,self.counts)
        ctime=tlist[1]
        counts=tlist[0]
        if dbPetShop.getByid(self.pid):#如果有记录了
            dbPetShop.updateInfo(self.pid, li[0], li[1], li[2],ctime,counts,self.isoption,self.xy,self.cs)
        else:
            dbPetShop.addInfo(self.pid, li[0], li[1], li[2],ctime,counts,self.isoption,self.xy,self.cs)
        