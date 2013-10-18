#coding:utf8
'''
Created on 2012-7-16
祷告管理
@author: jt
'''
from app.scense.core.singleton import Singleton
from app.scense.utils import dbaccess
from app.scense.applyInterface import configure
from app.scense.netInterface import pushObjectNetInterface
import time
import datetime
from app.scense.core.language.Language import Lg



class PrayManage():
    '''祷告管理'''

    __metaclass__ = Singleton

    def __init__(self):
        ''''''
        self.mc = dbaccess.memclient
        self.CXk=set([])#存储内存中的key 
        #  value{'gold':数量,'counts':次数}
        self.key="PrayManage#zs" #值是self.CXk
        
        
        self.gg=[] #n倍奖励信息  最多4条记录 [str,str]
        self.ggkey='prayGGkey' #存储self.gg
        
    def clean0(self):
        '''清空内存数据'''
        self.mc.delete_multi(list(self.CXk))
        
    def getGG(self):
        '''获取n倍奖励信息'''
        info=self.mc.get(self.ggkey)
        if not info:
            info=[]
        infolist=[]
        self.gg=[]
        for item in info:
            timestr=item[0] #2012-07-18 15:54:02
            str=item[1]
            
            st=time.strptime(timestr,"%Y-%m-%d %X")
            date=datetime.datetime( *st[:6] ) 
            ss=datetime.datetime.now()
            a4=ss-date
            count=int(a4.days)
            if count==0:
                str=Lg().g(560)%date.strftime(Lg().g(561))+str
            elif count==1:
                str=Lg().g(562)+str
            else:
                str=Lg().g(563)+str
            infolist.append(str)
            self.gg.append(item)
        return infolist
    
    def uploadGG(self,info):
        '''将信息保存在共享内存中'''
        self.mc.set(self.ggkey,info)
        
    def getkey(self,pid):
        '''生成内存key'''
        str="PrayManage#zs#key%s"%pid
        return str
        
    def updateQd(self,pid):
        '''角色点击祈祷
        @param pid: int 角色名称
        '''
        gold=0
        counts=0
        str=self.getkey(pid)
        info=self.mc.get(str)#获取角色祈祷信息
        if info:
            gold=info['gold']
            counts=info['counts']
            if not self.runingQd(pid, gold):#执行祈祷操作
                return False
            if counts==1:
                gold=gold+1
                counts=gold
                info={'gold':gold,'counts':counts}
            else:
                info={'gold':gold,'counts':counts-1}
            
            
        else:
            if not self.runingQd(pid, 0):#执行祈祷操作
                return False
            info={'gold':1,'counts':1}
            
            
        self.mc.set(str,info)#更新到内存
        self.CXk.add(str)
        self.mc.set(self.key,self.CXk)
        return True
        
        
        
    def runingQd(self,pid,gold):
        '''祈祷逻辑
        @param gold: int 钻石数量
        '''
        from app.scense.serverconfig.chatnode import chatnoderemote
        from app.scense.core.PlayersManager import PlayersManager
        v={1:Lg().g(564),2:Lg().g(499),3:Lg().g(565),4:Lg().g(566),0:Lg().g(564)}
        player=PlayersManager().getPlayerByID(pid)
        mygold=player.finance.getGold()
        if mygold<gold:
            pushObjectNetInterface.pushOtherMessage(905, Lg().g(567), [player.getDynamicId()])
            return False
        result=configure.qd(gold)
        lx=result[0]#奖励类型    1金币奖励    2经验奖励   3声望奖励    4活力
        sl=result[1]#奖励数量
        bs=result[2]#奖励倍数
        if lx==1:
            player.finance.addCoin(sl)
            ss=Lg().g(568)%(v.get(lx),sl)
        elif lx==2:
            player.level.addExp(sl)
            ss=Lg().g(568)%(v.get(lx),sl)
        elif lx==3:
            player.finance.addPrestige(sl)
            ss=Lg().g(568)%(v.get(lx),sl)
        elif lx==4:
            player.attribute.addEnergy(sl)
            ss=Lg().g(568)%(v.get(lx),sl)
        else:
            player.finance.addCoin(sl)
        if bs>1:
            ss+=Lg().g(569)%bs
        pushObjectNetInterface.pushOtherMessage(905, ss, [player.getDynamicId()])
#        player.finance.updateGold(mygold-gold)
        player.finance.consGold(gold,1)
        
        bbs=1#大于这个倍数的才会广播
        sj=time.strftime("%w%H")
        sj=int(sj)
        if sj>=310 and sj<=314:
            bbs=2
        
        if bs>bbs:
            pname=player.baseInfo.getName()
            tm=time.strftime("%Y-%m-%d %X")
            mg=Lg().g(570)%(pname,bs,v.get(lx),sl)
            chatnoderemote.callRemote('pushSystemToInfo',mg)
            
            if len(self.getGG())==4:
                del self.gg[0]
            self.gg.append([tm,mg])
            self.uploadGG(self.gg)
        return True
        
    def getQdInfo(self,pid):
        '''获取祈祷页面信息'''
        v={1:Lg().g(564),2:Lg().g(499),3:Lg().g(565),4:Lg().g(566),0:Lg().g(564)}
        sl=0#祈祷后获得奖励数量
        str=self.getkey(pid)
        info=self.mc.get(str)#获取角色祈祷信息
        gold=0#花费钻石的数量
        counts=1#剩余次数
        if info:
            gold=info['gold']
            counts=info['counts']
            
        mg=u''
        qsl=gold
        for item in range(3):
            if item>0:
                item+=2
            else:
                item+=1
            if gold==0:
                qsl=1
            else:
                qsl=gold
            sl=configure.qdShuliang(item, qsl)#获取祈祷之后的数量
            if item==4:
                mg=mg+u'%s%s'%(v.get(item),sl)
            else:
                mg=mg+Lg().g(571)%(v.get(item),sl)
        mg+=u'.'
        return[mg,gold,counts,self.getGG()]
        