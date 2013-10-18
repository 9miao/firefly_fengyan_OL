#coding:utf8
'''
Created on 2012-8-7
团队战斗战力管理类
@author: jt
'''
from app.scense.core.singleton import Singleton
from twisted.python import log
from app.scense.core.teamfight.TeamInfo import TeamInfo
import math
from app.scense.netInterface import pushObjectNetInterface
from app.scense.applyInterface import configure
from app.scense.utils import dbaccess
from app.scense.core.language.Language import Lg

class TeamFight(object):
    '''团队战斗战力管理类'''
    __metaclass__ = Singleton

    def __init__(self):
        '''初始化'''
        self.info={}#key:队伍id,value:队伍信息
        self.tag=1
        self.pi={}#key:角色id,value:所在队伍id
        self.ct={}#key：角色id,value:{多人副本类型:挑战次数，多人副本类型:挑战次数}
        
        self.mc = dbaccess.memclient#
        ncxx=self.mc.get("TeamInstanceFight#pi")
        self.CXpi=list(ncxx) #set([])或None
        
    def addfightcount(self,pid,tyid):
        '''添加战斗次数限制
        @param pid: int 角色id
        @param tyid: int 多人副本类型id
        '''
        if not self.ct.has_key(pid):#如果没有这个角色的记录
            self.ct[pid]={tyid:1}
        else:
            info=self.ct.get(pid)
            if not info.get(tyid):
                info[tyid]=1
            else:
                info[tyid]+=1
    
    def iscsxz(self,pid,tyid):
        '''判断能否进入多人副本战斗
        @param pid: int 角色id
        @param tyid: int 多人副本类型id
        '''
        if not self.ct.has_key(pid):
            return True
        else:
            info=self.ct.get(pid)
            if not info.has_key(tyid):
                return True
            else:
                count=info.get(tyid)#挑战次数
                if count>=3:
                    return False
                return True
    
    def getCXpi(self):
        '''获取共享内存中的伍信息'''
        self.CXpi=list(self.mc.get("TeamInstanceFight#pi")) #set([])或None
        return self.CXpi
    
    def addCXpi(self,pid):
        '''想共享内存中添加有队伍的角色id'''
        self.getCXpi()
        self.CXpi.append(pid)
        pilist=set(self.CXpi)
        self.mc.set("TeamInstanceFight#pi",pilist)
        
    def delCXpi(self,pid):
        '''删除共享内存中的队伍角色'''
        if self.getCXpi().count(pid)>0:
            self.CXpi.remove(pid)
            pilist=set(self.CXpi)
            self.mc.set("TeamInstanceFight#pi",pilist)
            
            
        
    
    def getTeamidByPid(self,pid):
        return self.pi.get(pid,0)
    
    def getteaminfoByteamid(self,teamid):
        '''根据队伍id获取队伍信息'''
        return self.info.get(teamid,None)
        
    def ishaveteam(self,teamid):
        '''判断是否有此队伍
        @param teamid: int 队伍id
        '''
        if self.info.has_key(teamid):
            return True
        return False
        
    def GetByPage(self,page,count=7):
        '''获取组队列表
        @param page: int 当前页数
        '''
        toplist= self.info.keys()#队伍id排序[1,2,3,4,5,6,7]
        if page<1:
            page=1
        i=(page-1)*count#起始key
        result=[]
        for n in range(count):
            if len(toplist)>i+n:
                xinxi={}#当前页队伍列表信息
                ke=toplist[i+n]#self.info中的key值(队伍id)
                teaminfo=self.info[ke]#队伍信息
                xinxi['dwId']=ke#队伍id
                xinxi['leaderName']=teaminfo.pname
                xinxi['curNum']=teaminfo.count
                xinxi['dwType']=teaminfo.type
                result.append(xinxi)
                
        return result,int(math.ceil(len(toplist)/7.0))
    
    def CreateTeam(self,player,typeid,wz):
        '''创建队伍
        @param player: obj 角色实例 
        @param typeid: int 副本类型
        @param wz: int 角色所在阵法的位置
        '''
        if not configure.isteamInstanceTime(player.level.getLevel()):
            return 0
        pid=player.baseInfo.getId()#队长id
        if not self.iscsxz(pid, typeid):
            pushObjectNetInterface.pushOtherMessageByCharacterId(Lg().g(645), [pid])
            return 0            
        self.tag+=1
        pid=player.baseInfo.getId()#队长id
        if self.pi.has_key(pid):
            return 0
        self.info[self.tag]=TeamInfo(self.tag,player,typeid,wz)#组队挑战副本类
        self.pi[pid]=self.tag#记录角色所在队伍id
        self.addCXpi(pid)
        return self.tag
        
    def TeamAddPlayer(self,player,tid,wz):
        '''角色加入队伍
        @param player: obj 角色实例
        @param tid: int 要加入队伍的id
        @param wz: int 阵法位置
        '''
        #队伍有变动后需要推送队伍信息给所有的成员
        if not configure.isteamInstanceTime(player.level.getLevel()):
            return {'result':False,'message':Lg().g(580),'tid':0}
        pid=player.baseInfo.getId()#角色id
        teid= self.pi.get(pid,None)#原始队伍id
        teaminfo=self.info.get(tid,None)#队伍信息
        if not teaminfo:#如果没有队伍信息
            pushObjectNetInterface.pushOtherMessageByCharacterId(Lg().g(624), [pid])
            return {'result':False,'message':Lg().g(479),'tid':tid}
        typeid=teaminfo.type
        if not self.iscsxz(pid, typeid):
            pushObjectNetInterface.pushOtherMessageByCharacterId(Lg().g(645), [pid])
            return {'result':False,'message':Lg().g(645),'tid':tid}
        
        if teaminfo.zf[wz]>0: 
            return{'result':False,'message':Lg().g(577),'tid':tid}
        if teaminfo.count>=5:
            return{'result':False,'message':Lg().g(578),'tid':tid}
        if teid:
            if tid==teid:
                return{'result':False,'message':Lg().g(579),'tid':tid}
            else:
                self.TeamDelPlayer(pid)#退出原始队伍
        teaminfo.addTeamPlayer(player, wz)
        plist=teaminfo.players.keys()#队伍成员id列表
        plist.remove(pid)
        pushObjectNetInterface.team4304(tid, plist)
        self.pi[pid]=tid
        self.addCXpi(pid)
        return {'result':True,'message':Lg().g(166),'tid':tid}
    
    def TeamDelPlayer(self,pid):
        '''成员主动退出队伍
        @param pid: int 角色id
        '''
        #队伍有变动后需要推送队伍信息给所有的成员
        tid= self.pi.get(pid,None)#队伍id
        if not tid:
            return
            log.err(u'TeamFight->TeamDelPlayer(%s) self.pid=%s'%(pid,self.pi))
        teaminfo=self.info.get(tid,None)
        if not teaminfo:
            log.err(u'TeamFight->TeamDelPlayer(%s) tid=%s  self.info=%s'%(pid,tid,self.info))
            return
        if teaminfo.pid==pid:#如果队长退出队伍
            plist=teaminfo.players.keys()#队伍成员id列表
            for k in teaminfo.players.keys():
                del self.pi[k]#删除角色所在队伍信息
                self.delCXpi(k)
                #通知该角色队伍已经解散
            del self.info[tid]#删除队伍
            pushObjectNetInterface.team4304(Lg().g(581), plist)
        else:
            teaminfo.delTeamPlayer(pid)
            del self.pi[pid]
            self.delCXpi(pid)
            
        plist=teaminfo.players.keys()#队伍成员id列表
        
        pushObjectNetInterface.team4304(tid, plist)
        
        
    def TCTeamPlayer(self,pid,cid):
        '''队长将成员踢出队伍
        @param pid: int 队长角色id
        @param cid: int 成员角色id
        '''
        tid= self.pi.get(cid,None)#成员队伍id
        if not tid:
            log.err(u'TeamFight->TCTeamPlayer(%s,%s) self.pid=%s'%(pid,cid,self.pi))
        teaminfo=self.info.get(tid,None)
        if not teaminfo:
            log.err(u'TeamFight->TCTeamPlayer(%s,%s) tid=%s  self.info=%s'%(pid,cid,tid,self.info))
            return {'result':False,'message':Lg().g(479)}
        if not teaminfo.pid==pid:
            return{'result':False,'message':Lg().g(582)}
        if cid==pid:
            return{'result':False,'message':Lg().g(583)}
        
        teaminfo.delTeamPlayer(cid)
        del self.pi[cid]
        self.delCXpi(cid)
        pushObjectNetInterface.pushOtherMessageByCharacterId(Lg().g(584),[cid])
        plist=teaminfo.players.keys()#队伍成员id列表
        pushObjectNetInterface.team4304(tid, plist)#推送其他队伍成员队伍信息
        pushObjectNetInterface.teamClean4304(tid, [cid])
        return{'result':True,'message':u'成功'}
    def getTeamInfoByPlayerId(self,pid,dwid):
        '''获取队伍信息
        @param pid: int 角色id
        '''
        tid= self.pi.get(pid,None)#成员的队伍id
        if not tid:
            log.err(u'TeamFight->getTeamInfoByPlayerId(%s,%s) self.pid=%s'%(pid,dwid,self.pi))
        if not dwid==tid:
            log.err("getTeamInfoByPlayerId(%s,%s) tid=%s"%(pid,dwid,tid))
        teaminfo=self.info.get(tid,None)
        if not teaminfo:
            pushObjectNetInterface.pushOtherMessageByCharacterId(Lg().g(624), [pid])
            return []
            log.err(u'TeamFight->getTeamInfoByPlayerId(%s,%s) tid=%s  self.info=%s'%(pid,dwid,tid,self.info))
        zf=teaminfo.zf #{1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0}#阵法信息 key阵法信息，value:>0表示角色在此位置
        rs=[]#队伍信息（右侧）
        for key,value in zf.items():#key:表示阵法位置，value：表示阵法上面的角色
            if value>0:
                zfinfo={}
                player=teaminfo.players.get(value)#角色实例
                zfinfo['roleId']=player.baseInfo.getId()
                zfinfo['level']=player.level.getLevel()#角色等级
                zfinfo['roleType']=player.profession.getFigure()#角色职业
                zfinfo['roleName']=player.baseInfo.getNickName()#角色名称
                zfinfo['pos']=key#角色位置
                rs.append(zfinfo)
        return rs
    
    def getTeamInfoByPlayerId1(self,dwid):
        '''获取队角色选择的阵法信息
        @param dwid: int 队伍id
        '''
        teaminfo=self.info.get(dwid,None)
        if not teaminfo:
            return[]
            log.err(u'TeamFight->getTeamInfoByPlayerId1(%s) dwid=%s  self.info=%s'%(dwid,dwid,self.info))
        zf=teaminfo.zf #{1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0}#阵法信息 key阵法信息，value:>0表示角色在此位置
        rs=[]#队伍信息（右侧）
        for key,value in zf.items():#key:表示阵法位置，value：表示阵法上面的角色
            if value>0:
                zfinfo={}
                player=teaminfo.players.get(value)#角色实例
                zfinfo['roleId']=player.baseInfo.getId()
                zfinfo['level']=player.level.getLevel()#角色等级
                zfinfo['roleType']=player.profession.getFigure()#角色职业
                zfinfo['roleName']=player.baseInfo.getNickName()#角色名称
                zfinfo['pos']=key#角色位置
                rs.append(zfinfo)
        return rs
    
    def dismissTeam(self,tid):
        '''解散队伍
        @param teamid: int 队伍id
        '''
        teaminfo=self.info.get(tid,None)#获取队伍类
        if not teaminfo:
            return 
        if teaminfo:
            plist=teaminfo.players.keys()#队伍所有成员列表
            for pcid in plist:
                del self.pi[pcid]
                self.delCXpi(pcid)
            del self.info[tid]
            plist=teaminfo.players.keys()#队伍成员id列表
            pushObjectNetInterface.team4304(tid, plist)
    #        pushObjectNetInterface.pushOtherMessageByCharacterId(Lg().g(581), plist)
        else:
            log.err(u'dismissTeam(%s)'%tid)

