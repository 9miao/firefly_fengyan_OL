#coding:utf8
'''
Created on 2012-2-21
殖民管理器
@author: jt
'''
from app.scense.core.singleton import Singleton
from app.scense.utils.dbopera import dbPublicscene,dbInstanceColonize,dbPortals
from app.scense.core.instance.InstanceGroupManage import InstanceGroupManage
from twisted.python import log
from app.scense.utils import dbaccess
from app.scense.core.language.Language import Lg


class ColonizeManage:
    '''殖民管理器'''
    __metaclass__ = Singleton

    def __init__(self):
        '''初始化'''

        #name(副本、城市、传送阵名称)  camp(所属阵营 0中立  1光明  2黑暗)  reward(奖励数量) fo={'id':0,'name':u'','pid':0,'pname':Lg().g(143),'gid':0,'gname':Lg().g(143),'camp':0,'reward':0}
        self.i={}#key:殖民副本组id,value:{}副本组信息  #副本被占领信息
        self.p={}#key:传送阵id,value:{}传送阵信息             #传送门被占领信息
        self.c={}#key:城市id，value:{}城市信息                     #城市被占领信息
        

        self.cityi={}#key:城市id,value:[]副本组id
        self.protali={}#key:传送阵id，value:[]副本组id
        self.ic={} #key:副本组id，value:城市id
        self.ip={} #key:副本组id，value:传送阵id
        self.wm={} #key:副本组id，value:卫冕次数
        
        #--------------------------------------------------------
        self.CXi={}#存储ColonizeManage().i在共享内存中的全部key
        self.CXc={}#存储ColonizeManage().c在共享内存中的全部key
        self.CXp={}#存储ColonizeManage().p在共享内存中的全部key
        self.CXwm={}#key:副本组id,value:内存中的key  
#        self.mc = dbaccess.memclient#memcache.Client(['127.0.0.1:11211',])
        #--------------------------------------------------------
        
        self.initSetDefaultValue() #初始化所有城市副本
#        self.CXi=self.mc.get("ColonzeGxAllKey#i")
#        self.CXc=self.mc.get("ColonzeGxAllKey#c")
#        self.CXp=self.mc.get("ColonzeGxAllKey#p")
#        self.CXwm=self.mc.get("ColonzeGxAllKey#wm")
#        self.AllUpdate()


    def getI(self):
        '''获取所有副本殖民信息'''
        self.updateI()
        return self.i
    
    def getC(self):
        '''获取所有副本城市殖民信息'''
        self.updateC()
        return self.c
    
    
    def initSetDefaultValue(self):
        '''填充城镇与副本，并设置默认值'''
        from app.scense.core.guild.GuildManager import GuildManager
        dataList=dbPublicscene.Allinfo.values()#获取所有城镇的信息
        for item in dataList: #迭代所有城镇信息    item['id']城市id ####################################城市
            cityid=item['id']#城市id
            self.cityi[cityid]=[]
            cfo={'cityid':cityid,'cityname':item['name'],'pid':0,'pname':u'无','gid':0,'gname':u'无','camp':0}
            self.c[cityid]=cfo
            dbInstanceColonize.addCityColonize(cityid, item['name'], 0, u'无', 0, u'无', 0, 0)
            pList=eval("["+str(item['portals'])+"]")
            if len(pList)<1: #如果城镇里面没有副本
                continue
            for it in pList: #迭代所有传送门id             ########################################传送阵
                itpname=dbPortals.ALL_PORTALS[it]['name']#传送阵名称
                pfo={'id':it,'name':itpname,'pid':0,'pname':u'无','gid':0,'gname':u'无','camp':0}
                self.p[it]=pfo
                self.protali[it]=[]
                groupList=InstanceGroupManage().getInstanceGroupBycszid(it) #获得传送门通往的所有副本组信息
                for i in groupList: #遍历所有副本组信息  i['id']:副本组id #########################副本组
                    instanceid=i['id']#副本组id
                    self.cityi[item['id']].append(instanceid) #向城市中添加副本组id
                    self.protali[it].append(instanceid)#向传送阵中添加副本组id
                    self.ic[instanceid]=cityid
                    self.ip[instanceid]=it
                    self.wm[instanceid]=0
                    ifo={'id':i['id'],'name':u'','pid':0,'pname':u'无','gid':0,'gname':u'无','camp':0,'wm':0}
                    defence=dbInstanceColonize.getInstanceColonizeByid(i['id']) #根据副本组id获取保卫信息
                    if defence:#如果此副本已经被玩家占领
                        ifo['pid']=defence['pid']
                        ifo['pname']=defence['pname']
                        ifo['gid']=defence['gid']
                        ifo['camp']=0
                        if defence['gid']>0:
                            ifo['camp']=GuildManager().getGuildById(defence['gid']).guildinfo['camp'] #所属阵营 0中立  1光明  2黑暗
                        ifo['gname']=defence['gname']
                        ifo['name']=defence['instancename']
                    self.i[i['id']]=ifo
#                    self.setProperty0()
        self.initCityColonize()
        self.initportal()
        
#    def setProperty0(self,instanceidinfo):
#        instanceidinfo['property']={}
#        #1力量、2敏捷 、3智力、4精神、5耐力、6所有
#        instanceidinfo['property'][1]=[False,None,None,None]#是否启用状态，datetime,定时器，是否小于30分钟（True：表示小于30分钟 or False）
#        instanceidinfo['property'][2]=[False,None,None,None]
#        instanceidinfo['property'][3]=[False,None,None,None]
#        instanceidinfo['property'][4]=[False,None,None,None]
#        instanceidinfo['property'][5]=[False,None,None,None]
                    
    
    
    
#    def updateResist(self,instancegroupid):
#        '''更新卫冕次数
#        @param instancegroupid: int 副本组id
#        @param pid: int 角色id
#        '''
#        
#        
#        if self.i.has_key(instancegroupid):
#            self.updateIByid(instancegroupid)#从共享内存更新数据
#            self.i[instancegroupid]['wm']+=1
#            self.setI(instancegroupid, self.i[instancegroupid])#提交更新后的数据
#            return self.i[instancegroupid]['wm']
        
        
    def updateGuild(self,pid,gid=0,gname=u''):
        from app.scense.core.guild.GuildManager import GuildManager
        
        '''角色更改国
        @param pid: int 角色id
        @param gid: int 国id 默认值0：表示没有国
        @param gname: int  国名称 默认值'',表示没有国
        '''
        from app.scense.applyInterface import winning_app
        if gname==u'':
            gname=Lg().g(143)
        self.updateC()
        for cityid in self.c.keys():#城市id
            cityinfo=self.c.get(cityid)
            if cityinfo['pid']==pid:#如果城镇殖民者id和修改国的角色是同一个玩家
                if gid==0:#如果角色退出国
                    cityinfo['pid']=0
                    cityinfo['gid']=0
                    winning_app.outGuild(pid, cityinfo['pname'], cityinfo['gname'])
                else:
                    cityinfo['gid']=gid #更新行会id
                    if gid>0:
                        cityinfo['camp']=GuildManager().getGuildById(gid).guildinfo['camp'] #所属阵营 0中立  1光明  2黑暗
                    else:
                        cityinfo['camp']=0
                    cityinfo['gname']=gname #更新行会名称
                self.setC(cityid, cityinfo)
                
        self.updateI()
        for instanceid in self.i.keys(): #副本组id
            info=self.i.get(instanceid)#副本殖民信息
            if info['pid']==pid: #如果此副本被该角色殖民了
                if gid==0:#如果角色退出国
                    info['pid']=0
                    info['gid']=0
                    info['wm']=0
                    winning_app.outGuild(pid, info['pname'], info['gname'])
                else:
                    info['gid']=gid
                    if gid>0:
                        info['camp']=GuildManager().getGuildById(gid).guildinfo['camp'] #所属阵营 0中立  1光明  2黑暗
                    else:
                        info['camp']=0
                    info['gname']=gname
                self.setI(instanceid, info)
        
        self.updateP()
        for cszid in self.p.keys():#传送阵id
            cinfo=self.p.get(cszid)#传送阵信息
            if cinfo['pid']==pid:
                if gid==0:#如果角色退出国
                    cinfo['pid']=0
                    cinfo['gid']=0
                else:
                    cinfo['gid']=gid
                    cinfo['gname']=gname
                    if gid>0:
                        cinfo['camp']=GuildManager().getGuildById(gid).guildinfo['camp'] #所属阵营 0中立  1光明  2黑暗
                    else:
                        cinfo['camp']=0
                self.setP(cszid, cinfo)
        
#        publicnoderemote.callRemote('updateColonizeManage',self.citys,self.instancetocity,self.Portals,self.instancetoprotal)
    
    
    
    def updateInstancePid(self,groupid,pid,pname,gid,gname,instancename):
        '''更改(或添加)副本领主
        @param groupid: int 副本组id
        @param pid: int 角色id
        @param pname: str 角色名称
        @param gid: int 国id
        @param gname: str 国名称
        @instancename:str 副本名称
        '''
        from app.scense.core.guild.GuildManager import GuildManager
        
        self.updateIByid(groupid)
        info=self.i[groupid]#副本殖民信息
        if info['pid']==0:#如果这个副本没有被殖民
            dbInstanceColonize.addInstanceColonize(groupid,instancename, pid, pname, gid, gname, 0, 0)#添加到数据库中

        info['pid']=pid #设置此副本的领主角色id
        info['pname']=pname #设置副本领主的角色名称
        info['gid']=gid #设置领主行会id
        info['camp']=0
        if gid>0:
            info['camp']=GuildManager().getGuildById(gid).guildinfo['camp'] #所属阵营 0中立  1光明  2黑暗
        info['gname']=gname #设置领主行会名称
        info['name']=instancename #设置副本名称
        self.setI(groupid,info)
        cityid=self.ic.get(groupid)#根据副本组id获取所属城市id
        result,instanceinfo=self.cityColonize(cityid) #根据城市id判断城市是否已经被玩家占领 
        if result:
            pid=instanceinfo['pid']
            cinfo=self.c[cityid]
            cinfo['pid']=pid
            cinfo['pname']=instanceinfo['pname']
            cinfo['gid']=instanceinfo['gid']
            cinfo['gname']=instanceinfo['gname']
            cinfo['camp']=instanceinfo['camp']
            self.setC(cityid, cinfo)
            
        cszid=self.ip.get(groupid)#根据副本组id获取所属传送阵id
        rs1,cs1=self.Portal(cszid)#根据传送阵id判断传送阵是否被主宰
        if rs1:
            pid=cs1['pid'] #设置城市占领者id
            pname=cs1['pname'] #设置城市占领者名称
            gid=cs1['gid'] #设置城市占领者行会id
            gname=cs1['gname']
            camp=cs1['camp']#所属阵营 0中立  1光明  2黑暗
            pinfo=self.p[cszid]#传送阵殖民信息
            pinfo['pid']=pid
            pinfo['pname']=pname
            pinfo['gid']=gid
            pinfo['gname']=gname
            pinfo['camp']=camp
            self.setP(cszid, pinfo)
        
#        publicnoderemote.callRemote('updateColonizeManage',self.citys,self.instancetocity,self.Portals,self.instancetoprotal)

    def cityColonizeinint(self,cityid):
        '''初始化是使用判断此城镇是否已经被殖民,return bool'''
        flg=0
        ilist=self.cityi.get(cityid)#城市所有副本组id
        for ids in ilist:#副本组id
            ppid=self.i[ids].get('pid')#此副本领主id  没有占领默认为0
            if ppid==0: #如果副本id为0
                return False,None
            if flg==0:
                flg=ppid #flg=副本占领者角色id
            else:
                if flg!=ppid: #如果同一个城市的副本的占领者角色id不同
                    return False,None
        instanceid=self.cityi[cityid][0]#副本组信息
        instanceinfo=self.i[instanceid]#副本殖民信息
        return True,instanceinfo

    def cityColonize(self,cityid):
        '''判断此城镇是否已经被殖民,return bool'''
        self.updateC()
        flg=0
        ilist=self.cityi.get(cityid)#城市所有副本组id
        for ids in ilist:#副本组id
            ppid=self.i[ids].get('pid')#此副本领主id  没有占领默认为0
            if ppid==0: #如果副本id为0
                return False,None
            if flg==0:
                flg=ppid #flg=副本占领者角色id
            else:
                if flg!=ppid: #如果同一个城市的副本的占领者角色id不同
                    return False,None
        instanceid=self.cityi[cityid][0]#副本组信息
        self.updateIByid(instanceid)
        instanceinfo=self.i[instanceid]#副本殖民信息
        return True,instanceinfo
    
    def initCityColonize(self):
        '''初始化城市占领信息'''
        for city in self.cityi.keys(): #city ： 城市id
            flg,instance=self.cityColonizeinint(city)
            if flg:
                pid=instance['pid']
                info=self.c[city]#城市殖民信息
                info['pid']=pid
                info['pname']=instance['pname']
                info['gid']=instance['gid']
                info['gname']=instance['gname']
                info['camp']=instance['camp']
    
    def Portal(self,csz):
        '''判断此传送阵是否已经被殖民,return bool'''
        
        self.updateP()
        flg=0
        for ids in self.protali.get(csz):#ids 副本组id
            ppid=self.i[ids].get('pid')#此副本领主id  没有占领默认为0
            if ppid==0: #如果副本id为0
                return False,None
            if flg==0:
                flg=ppid #flg=副本占领者角色id
            else:
                if flg!=ppid: #如果同一个城市的副本的占领者角色id不同
                    return False,None
        instanceid=self.protali[csz][0]#副本组信息
        self.updateIByid(instanceid)
        instanceinfo=self.i[instanceid]#副本殖民信息
        return True,instanceinfo
    
    def Portalinit(self,csz):
        '''判断此传送阵是否已经被殖民,return bool'''
        flg=0
        for ids in self.protali.get(csz):#ids 副本组id
            ppid=self.i[ids].get('pid')#此副本领主id  没有占领默认为0
            if ppid==0: #如果副本id为0
                return False,None
            if flg==0:
                flg=ppid #flg=副本占领者角色id
            else:
                if flg!=ppid: #如果同一个城市的副本的占领者角色id不同
                    return False,None
        instanceid=self.protali[csz][0]#副本组信息
        instanceinfo=self.i[instanceid]#副本殖民信息
        return True,instanceinfo
    
    def initportal(self):
        '''初始化传送阵占领信息'''
        for csz in self.protali.keys():
            flg,cszs=self.Portalinit(csz)
            if flg:
                pid=cszs['pid'] #设置城市占领者id
                pname=cszs['pname'] #设置城市占领者名称
                gid=cszs['gid'] #设置城市占领者行会id
                gname=cszs['gname']
                camp=cszs['camp']#所属阵营 0中立  1光明  2黑暗
                info=self.p[csz]#传送阵殖民信息
                info['pid']=pid
                info['pname']=pname
                info['gid']=gid
                info['gname']=gname
                info['camp']=camp

    
    def getCityList(self):
        '''获得所有城市被占领的信息'''
        
        cityList=[] #存放占领角色
        self.updateC()
        for info in self.c.values(): ##城市占领信息
            if info['pid']>0: #如果此城镇已经被玩家占领
                cityList.append(info)
        return cityList
        
    def getprotalBypid(self,pid):
        '''根据角色id获取主宰的传送门'''
        list=[]
        
        self.updateP()
        for info in self.p.values():#info 传送阵信息
            if info['pid']==pid:
                list.append(info['name'])
        return list

    def getInstanceListByCityid(self,cityid):
        '''通过城市id获得该城市所有副本信息'''
        #{副本id,副本信息}
        
        self.updateI()
        value={}
        instancelist= self.cityi.get(cityid)#副本组id集合
        for idd in instancelist:
            info=self.i.get(idd)#获取副本组信息
            value[idd]=info
        return value
    
    def getInstanceInfoByinstanceid(self,id):
        '''根据副本id，获取副本信息
        @param id: 副本id
        '''
        
        instancegroupid=InstanceGroupManage().getFristInstanceBy(id) #根据副本id获取副本组id
        self.updateIByid(instancegroupid)
        info=self.i.get(instancegroupid)
        return info
    
    def getInstanceInfoByid(self,id):
        '''根据副本组id，获取副本信息
        @param id: int 副本组id
        '''
        try:
            self.updateIByid(id)
            info=self.i.get(id)
            return info
        except:
            log.err(u'ClonizeManage().getInstanceInfoByid(id=%s)'%id)


#    def setAllCount0(self):
#        '''设置所有通关次数为0'''
#        for city in self.cityi.keys(): #city ： 城市id
#            for instance in self.cityi[city]: #instance #副本id
#                self.i[instance]['reward']=0
##        publicnoderemote.callRemote('updateColonizeManage',self.citys,self.instancetocity,self.Portals,self.instancetoprotal)
        
    def getCityByCityid(self,cityid):
        '''通过城镇id获得相应数据，没有返回None'''
        
        self.updateC()
        if self.c.has_key(cityid):
            info=self.c[cityid]
            if info['pid']>0: #如果此城镇已经被玩家占领
                    return {'cityid':cityid,'cityname':info['name'],'gid':info['gid'],'gname':info['gname'],'pname':info['pname'],'pid':info['pid']}
        else:
            return None
    
    def getpidByinstanceid(self,instanceid):
        '''通过副本组id获得副本殖民者id'''
        
        self.updateIByid(instanceid)
        info = self.i.get(instanceid)
        return info['pid']
    
#    def getPInfofoByid(self,id):
#        '''根据副本组id获取副本殖民信息'''
#        cityid=self.instancetocity[id] #通过副本组id获得城市id
#        return self.citys[cityid]['instances'][id]

    def ishavestrengthen(self,pid):
        '''判断这个角色是否有殖民地
        @param pid: int 角色id
        '''
#        self.updateI()
        for info in self.i.values():
            if info.get('pid')==pid:
                    return True
        return False
    
######################################################start##########################################################
    def sc(self,name,saveK,llist):
        '''生成并保存key以及把llist保存在共享内存中
        @param name: str  共享内存中key前缀
        @param saveK: {} 保存在本类中的共享内存的key
        @param llist: {} 要保存的数据
        '''
        pass
#        for key,value in llist.items():
#            xk="GxColonize_%s_%s"%(name,key)
#            saveK[key]=xk
#            self.mc.set(xk,value)
            
    def hq(self,saveK,data):
        '''获取共享内存中的值
        @param saveK: {} 本类中保存的共享内存key
        @param data: {} 存放共享内存的数据
        '''
        pass
#        for key,value in saveK.items():
#            data[key]=self.mc.get(value)
#------------------------------------------------------ColonizeManage().i-----------------#
    def saveAllI(self):
        '''保存所有副本组殖民信息'''
        pass
#        self.sc("I", self.CXi, self.i)
        
    def updateI(self):
        '''从共享内存中获取最新副本组殖民数据'''
#        self.hq(self.CXi, self.i)
        pass
            
    def setI(self,instanceid,value):
        '''更新或者添加副本组殖民信息'''
        pass
#        self.mc.set(self.CXi.get(instanceid),value)
        
    def updateIByid(self,instanceid):
        pass
#        value= self.mc.get(self.CXi.get(instanceid))
#        self.i[instanceid]=value
#        return value
        
#------------------------------------------------------ColonizeManage().c-----------------#
    def saveAllC(self):
        '''保存所有城市殖民信息'''
        pass
#        self.sc("C", self.CXc, self.c)
    
    def updateC(self):
        '''从共享内存中获取最新城市殖民数据'''
        pass
#        self.CXc=self.mc.get("ColonzeGxAllKey#c")
#        self.hq(self.CXc, self.c)

    
    def setC(self,cityid,value):
        '''更新或者添加城市殖民信息'''
        pass
#        self.mc.set(self.CXc.get(cityid),value)
        
#------------------------------------------------------ColonizeManage().p-----------------#        
        
    def saveAllP(self):
        '''保存所有城市殖民信息'''
        pass
#        self.sc("P", self.CXp, self.p)
    
    def updateP(self):
        pass
#        self.hq(self.CXp, self.p)
    
    def setP(self,portalid,value):
        '''更新或者添加城市殖民信息'''
        pass
#        self.mc.set(self.CXp.get(portalid),value)
        
    def saveAllWm(self):
        '''保存所有卫冕信息'''
        pass
#        self.sc("Wm", self.CXwm, self.wm)
    
    def AddWm(self,groupid):
        '''增加卫冕记录'''
        pass
#        counts=self.mc.get(self.CXwm.get(groupid))
#        self.mc.set(self.CXwm.get(groupid), counts+1)
#        return counts+1
    def getWm(self,groupid):
        '''获取卫冕记录'''
        pass
#        counts=self.mc.get(self.CXwm.get(groupid))
#        return counts
    def updateWm0(self,groupid):
        '''修改卫冕次数'''
        pass
#        self.mc.set(self.CXwm.get(groupid), 0)
        
#------------------------------------------------------ColonizeManage() i c p-----------------#
    def AllSave(self):
        '''保存所有殖民信息'''
        pass
#        self.saveAllWm()
#        self.saveAllI()
#        self.saveAllC()
#        self.saveAllP()
    
    def AllUpdate(self):
        '''从内存获取并更新到本地数据'''
        pass
#        self.updateI()
#        self.updateC()
#        self.updateP()
########################################################end########################################################

    
                
                
        