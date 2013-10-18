#coding:utf8
'''
Created on 2011-9-17
行会类
@author: lan
'''
from app.scense.component.mail.Mail import Mail
from app.scense.utils.dbopera import dbGuild
import datetime
import math

from app.scense.core.PlayersManager import PlayersManager
from app.scense.netInterface.pushObjectNetInterface import pushOtherMessage,pushApplyMessage
from app.scense.netInterface.pushPrompted import pushPromptedMessage
from app.scense.serverconfig.chatnode import chatnoderemote
from app.scense.protoFile.guild import CorpsLevelUp_pb2
from app.scense.core.language.Language import Lg


ADDGUILDTASKTYPE = 105


def pushGuildLevelUpMessage(level,sendList):
    '''推送国升级的消息'''
    response = CorpsLevelUp_pb2.CorpsLevelUpNotify()
    response.level = level
    msg = response.SerializeToString()
    pushApplyMessage(1323,msg,sendList)

class Guild():
    
    MAXLEVEL = 10
    
    def __init__(self,name):
        '''初始化国对象
        '''
        #国的数据
        self.id = 0#国的ID
        self.name = ""#国的名称
        self.bugle = ""#国的军号
        self.camp = 0#国的阵营
        self.announcement = ""#国的公告
        self.level = 1#国的等级
        self.exp = 0#国的经验
        self.emblemLevel = 1#军徽等级
        self.description = ""#国的描述
        self.president = 0#国行会长的ID
        self.creator = 0#国创始人的ID
        self.veterans = ""#元老组成员ID（2位，id逗号分隔） 
        self.staffOfficers = ""#参谋组成员（6位，id逗号分隔） 
        self.senators = ""#议员组成员（10位，id逗号分隔）
        self.color = 13421721#代表颜色 
        self.levelrequired = 0#加入国最低等级限制
        self.presidentname = ""#国长名称
        self.createDate = None#创建时间
        self.fortune = 0#幸运值
        self.cliffordLog = []#祈福日志
        
    def initGuildData(self,data):
        '''初始化行会数据'''
        for keyname in self.__dict__.keys():
            if not keyname.startswith('_'):
                setattr(self,keyname,data.get(keyname))
        self.fortune = 0
        self.cliffordLog = []
        
    @property
    def guildinfo(self):
        '''国的所有信息
        '''
        info={"id":self.id,"name":self.name,"bugle":self.bugle,"camp":self.camp,"announcement":self.announcement,
              "level":self.level,"exp":self.exp,"emblemLevel":self.emblemLevel,"description":self.description,
              "president":self.president,"creator":self.creator,"veterans":self.veterans,"staffOfficers":self.staffOfficers,
              "senators":self.senators,"color":self.color,"levelrequired":self.levelrequired,"presidentname":self.presidentname,
              "createDate":self.createDate,"fortune":self.fortune,"cliffordLog":self.cliffordLog
              }
        return info
    
    def get(self,val):
        info=self.guildinfo
        data=info.get(val,None)
        return data
    
    def getClolor(self):
        '''获取行会的替代颜色'''
        corlor = self.get('corlor')
        if not corlor:
            return 0
        return corlor
    
    def getPresident(self):
        '''获取国长的ID
        '''
        president = self.get('president')
        if not president:
            return 0
        return president
    
    def getGuildName(self):
        '''获取行会的名称'''
        name = self.get('name')
        if not name:
            return ''
        return name
    
    def changeColor(self,operator,color):
        '''修改行会代表颜色'''
        if self.getPresident() != operator:
            return {'result':False,'message':Lg().g(515)}
        self.color=color
        return {'result':True,'message':Lg().g(175)}
    
    def getGuildMemberIdlist(self):
        '''获取行会成员的id列表'''
        result = dbGuild.getGuildMemberIdList(self.id)
        return result
    
    def getGuildLevel(self):
        '''获取国的等级'''
        level = self.get('level')
        if not level:
            return ''
        return level
    
    def getGuildInfo(self,characterId):
        '''获取行会的信息'''
        corpsInfo = dbGuild.getGuildInfoById(self.id)
        guildInfo = self.guildinfo
        corpsInfo['corpsImg'] = guildInfo['emblemLevel']
        corpsInfo['level'] = guildInfo['level']
        corpsInfo['memberCount'] = corpsInfo['memberCount'] + ((guildInfo['emblemLevel']-1)*30)
        corpsInfo['bugle'] = guildInfo['bugle']
        corpsInfo['nickname'] = guildInfo['presidentname']
        corpsInfo['levelrequired'] = guildInfo['levelrequired']
        return corpsInfo
    
    def getGuildMemberInfo(self,index,limit=10):
        '''获取行会成员信息
        @param index: int 页面数
        @param limit: int 每页显示数目限制
        '''
        MemberInfoList = {}
        infos = []
        maxPage = math.ceil(dbGuild.countGuildMenberNum(self.id)/float(limit))
        memberInfos = dbGuild.getGuildMemberInfo(self.id, index, limit)
        for member in memberInfos:
            data = {}
            data['memberliId'] = member['characterId']
            data['memberName'] = member['nickname']
            data['memberLevel'] = member['level']
            data['memberProfession'] = member['profession']
            data['memberRank'] = {0:Lg().g(516),1:Lg().g(517),2:Lg().g(518),3:Lg().g(519),4:Lg().g(520)}.get(member['post'])
            data['onlineState'] = self.getCharacterOnlineState(member['isOnline'],
                                                               member['outtime'])
            data['memberContribution'] = member['contribution']
            infos.append(data)
        MemberInfoList['MemberOrAppliListBaseInfo'] = infos
        MemberInfoList['maxPage'] = maxPage
        return MemberInfoList
    
    def searchGuildMemberInfo(self,searchCriteria,curPage,limit =10):
        '''搜索行会成员
        @param searchCriteria: str 成员的名称
        '''
        MemberInfoList = {}
        infos = []
        maxPage = math.ceil(dbGuild.countSearchMemberNum(self.id,searchCriteria)/float(limit))
        if maxPage==0:
            maxPage=1
        members = dbGuild.searchGuildMemberInfo(self.id,searchCriteria,curPage,limit)
        for member in members:
            data = {}
            data['memberliId'] = member['characterId']
            data['memberName'] = member['nickname']
            data['memberLevel'] = member['level']
            data['memberProfession'] = member['profession']
            #data['memberRank'] = Lg().g(516)#{0:Lg().g(516),1:Lg().g(517),2:Lg().g(518),3:Lg().g(519),4:Lg().g(520)}.get(member['post'])
            if data['memberliId']==self.president:
                data['memberRank'] = Lg().g(520)
            elif data['memberliId'] in eval("["+self.guildinfo['veterans']+"]"):
                data['memberRank'] = Lg().g(519)
            elif data['memberliId'] in eval("["+self.guildinfo['staffOfficers']+"]"):
                data['memberRank'] = Lg().g(518)
            elif data['memberliId'] in eval("["+self.guildinfo['senators']+"]"):
                data['memberRank'] = Lg().g(517)
            else:
                data['memberRank'] = Lg().g(516)
            data['onlineState'] = self.getCharacterOnlineState(member['isOnline'],
                                                               member['outtime'])
            data['memberContribution'] = member['contribution']
            infos.append(data)
        MemberInfoList['curPage'] = curPage
        MemberInfoList['MemberListBaseInfo'] = infos
        MemberInfoList['maxPage'] = maxPage
        return MemberInfoList
    
    def GetEmblemInfo(self):
        '''获取行会管理人员信息'''
        veteranList = eval('['+self.guildinfo['veterans']+']')
        staffList = eval('['+self.guildinfo['staffOfficers']+']')
        senatorsList = eval('['+self.guildinfo['senators']+']')
        info = {}
        info['corpsFounder'] = dbGuild.getCharacterNameByID(self.guildinfo['creator'])
        info['corpsId'] = self.id
        info['corpsImg'] = self.guildinfo['emblemLevel']
        info['createData'] = str(self.guildinfo['createDate'])
        info['corpsLevel'] = self.guildinfo['level']
        info['curProgress'] = self.guildinfo['exp']
        info['maxPorgress'] = self.guildinfo['level']**2*1000
        info['emblemLevel'] = self.guildinfo['emblemLevel']
        info['corpsChief'] = dbGuild.getCharacterNameByID(self.guildinfo['president'])
        info['veteranList'] = []
        info['staffInfo'] = []
        info['orderInfo'] = []
        info['bugleTxt'] = self.guildinfo['bugle']
        for veteran in veteranList:
            info['veteranList'].append(dbGuild.getCharacterNameByID(veteran))
        for staff in staffList:
            info['staffInfo'].append(dbGuild.getCharacterNameByID(staff))
        for senator in senatorsList:
            info['orderInfo'].append(dbGuild.getCharacterNameByID(senator))
        return info
        
    def getCharacterOnlineState(self,isOnline,outtime):
        '''获取角色的在线状态'''
        state = ''
        if isOnline:
            state = Lg().g(521)
        else:
            delta = datetime.datetime.now()-outtime
            state = Lg().g(522)%delta.days
        return state
    
    def getApplyList(self,index,limit=10):
        '''获取申请列表'''
        MemberInfoList = {}
        maxPage = math.ceil(dbGuild.countGuildApplyNum(self.id)/float(limit))
        infos = []
        applyList = dbGuild.getApplyJoinGuildList(self.id,index, limit)
        for member in applyList:
            data = {}
            data['memberliId'] = member['applicant']
            data['memberName'] = member['nickname']
            data['memberLevel'] = member['level']
            data['memberProfession'] = member['profession']
            data['memberRank'] = Lg().g(143)
            data['memberTime'] = str(member['appTime'])
            data['memberContribution'] = 0
            infos.append(data)
        MemberInfoList['MemberOrAppliListBaseInfo'] = infos
        MemberInfoList['maxPage'] = maxPage
        return MemberInfoList
    
    def searchApplyJoinGuildInfo(self,searchCriteria,curPage,limit = 10):
        '''搜索行会申请信息
        @param searchCriteria: str 搜索条件
        '''
        MemberInfoList = {}
        maxPage = math.ceil(dbGuild.countSearchMemberNum(self.id,searchCriteria)/float(limit))
        if maxPage==0:
            maxPage=1
        infos = []
        members = dbGuild.searchApplyJoinGuildInfo(self.id, searchCriteria,curPage,limit = limit)
        for member in members:
            data = {}
            data['memberliId'] = member['applicant']
            data['memberName'] = member['nickname']
            data['memberLevel'] = member['level']
            data['memberProfession'] = member['profession']
            data['memberRank'] = Lg().g(143)
            data['memberTime'] = str(member['appTime'])
            infos.append(data)
        MemberInfoList['levelrequired'] = self.guildinfo['levelrequired']
        MemberInfoList['curPage'] = curPage
        MemberInfoList['AppliListBaseInfo'] = infos
        MemberInfoList['maxPage'] = maxPage
        return MemberInfoList
    
    def getGuildAttrExt(self):
        '''获取国科技属性的加成'''
        info = {}
        guildLevel = self.getGuildLevel()
        techlimit = dbGuild.lEVEL_TECHNOLOGY.get(guildLevel)
        for techId,technology in dbGuild.All_TECHNOLOGY.items():
            level = techlimit.get('tech_%d'%techId)
            if level:
                formula = technology.get('technologyFormula','')
                exec(formula)
        return info
    
    def fireMember(self,operator,memberId):
        '''开除行会成员
        @param operator: 操作者的id
        @param memberID: int 成员的id 角色id
        '''
        from app.scense.core.instance.ColonizeManage import ColonizeManage
        president = self.getPresident()
        veteranList = eval('['+self.guildinfo['veterans']+']')
        staffList = eval('['+self.guildinfo['staffOfficers']+']')
        senatorsList = eval('['+self.guildinfo['senators']+']')
        #获取操作者的权限
        if operator==president:
            operatorpost =4
        elif operator in veteranList:
            operatorpost = 3
        elif operator in staffList:
            operatorpost = 2
        elif operator in senatorsList:
            operatorpost = 1
        else:
            operatorpost = 0
        #获取被操作者的权限
        if memberId==president:
            memberpost =4
        elif memberId in veteranList:
            memberpost = 3
        elif memberId in staffList:
            memberpost = 2
        elif memberId in senatorsList:
            memberpost = 1
        else:
            memberpost = 0
            
        if operator ==memberId:
            return {'result':False,'message':Lg().g(523)}#权限不够
        if operatorpost<= memberpost:
            return {'result':False,'message':Lg().g(515)}#权限不够
        if not dbGuild.checkCharacterInGuild(memberId, self.id):
            return {'result':False,'message':Lg().g(524)}
        result = dbGuild.deleteCharacterGuildRelation(memberId)
        if result:
            postdict = dbGuild.updateGuildPost(self.id)
            self.veterans=postdict.veterans
            self.staffOfficers=postdict.staffOfficers
            self.senators=postdict.senators
            content = Lg().g(525)%(self.guildinfo.get('nickname',''),\
                                      self.guildinfo.get('name',''))
            title = Lg().g(526)
            m = Mail( title=title,type =0, senderId =-1, receiverId=memberId,\
                            sender = Lg().g(128),content=content)
            m.mailIntoDB()
            player = PlayersManager().getPlayerByID(memberId)
            if player:
                player.guild.updateID(0)
                chatnoderemote.callRemote('updateGuild',memberId,self.id,0)#同步聊天角色中的行会
                playerList = dbGuild.getGuildCharacterIdList(self.id)
                msg = Lg().g(527)%(player.baseInfo.getName(),self.getGuildName())
                sendList = [PlayersManager().getPlayerByID(p[0]).getDynamicId()\
                         for p in playerList \
                        if PlayersManager().getPlayerByID(p[0]) and \
                        PlayersManager().getPlayerByID(p[0]).getDynamicId()]
                pushPromptedMessage(msg, sendList)
                player.updatePlayerInfo()
            ColonizeManage().updateGuild(memberId, 0, u'')
            return {'result':True,'message':Lg().g(528)}#开除成功
        return {'result':False,'message':Lg().g(529)}#开除失败
    
    def JointGuild(self,characterId):
        '''将角色加入国'''
        curMenberNum = dbGuild.countGuildMenberNum(self.id)
        info = self.guildinfo
        maxMemberCount = 20 + ((info['emblemLevel']-1)*30)
        if curMenberNum>=maxMemberCount:
            return {'result':False,'message':Lg().g(83)}
        result = dbGuild.insertCharacterGuildInfo(characterId, self.id)
        dbGuild.delCharacterAllApply(characterId)
        if result:
            player = PlayersManager().getPlayerByID(characterId)
            if player:
                player.quest.specialTaskHandle(ADDGUILDTASKTYPE)
                player.guild.updateID(self.id)
                chatnoderemote.callRemote('updateGuild',characterId,self.id,1)#同步聊天角色中的行会
                player.updatePlayerInfo()
            return {'result':True,'message':Lg().g(530)}#同意申请成功
        return {'result':True,'message':Lg().g(531)}#同意申请失败
    
    def acceptGuildApply(self,operator,characterId):
        '''同意角色的入会申请
        @param operator: 操作者的id
        @param characterId: int 申请人的id
        '''
        president = self.get('president')
        veteranList = eval('['+self.guildinfo['veterans']+']')
        staffList = eval('['+self.guildinfo['staffOfficers']+']')
        senatorsList = eval('['+self.guildinfo['senators']+']')
        #获取操作者的权限
        if operator==president:
            operatorpost =Lg().g(520)
        elif operator in veteranList:
            operatorpost = Lg().g(519)
        elif operator in staffList:
            operatorpost = Lg().g(518)
        elif operator in senatorsList:
            operatorpost = Lg().g(517)
        
        managementGroup = veteranList + staffList + senatorsList
        
        if not dbGuild.checkHasApply(self.id, characterId):
            return -4
        if operator!=self.president and operator not in managementGroup:
            return -1#权限不够
        if dbGuild.checkCharacterHasGuild(characterId):
            return -2#已经加入了行会
        curMenberNum = dbGuild.countGuildMenberNum(self.id)
        info = self.guildinfo
        maxMemberCount = 20 + ((info['emblemLevel']-1)*30)
        if curMenberNum>=maxMemberCount:
            return -3#成员数量达到上限
        result = dbGuild.insertCharacterGuildInfo(characterId, self.id)
        dbGuild.delCharacterAllApply(characterId)
        if result:
            player = PlayersManager().getPlayerByID(operator)
            content = Lg().g(532)\
            %(self.guildinfo.get('name',''),operatorpost,\
                player.baseInfo.getNickName(),self.guildinfo.get('name',''))
            title = Lg().g(526)
            m = Mail( title=title,type =0, senderId =-1, receiverId=characterId,\
                            sender = Lg().g(128),content=content)
            m.mailIntoDB()
            player = PlayersManager().getPlayerByID(characterId)
            if player:
                player.guild.updateID(self.id)
                chatnoderemote.callRemote('updateGuild',characterId,self.id,1)#同步聊天角色中的行会
                player.updatePlayerInfo()
            return 1#同意申请成功
        return 0#同意申请失败
    
    def refuseGuildApply(self,operator,characterId):
        '''拒绝角色的入会申请
        @param operator: 操作者的id
        @param characterId: int 申请人的id
        '''
        president = self.get('president')
        veteranList = eval('['+self.guildinfo['veterans']+']')
        staffList = eval('['+self.guildinfo['staffOfficers']+']')
        senatorsList = eval('['+self.guildinfo['senators']+']')
        #获取操作者的权限
        if operator==president:
            operatorpost =Lg().g(520)
        elif operator in veteranList:
            operatorpost = Lg().g(519)
        elif operator in staffList:
            operatorpost = Lg().g(518)
        elif operator in senatorsList:
            operatorpost = Lg().g(517)
        
        managementGroup = veteranList + staffList + senatorsList
        if not dbGuild.checkHasApply(self.id, characterId):
            return -4
        if operator!=self.president and operator not in managementGroup:
            return -1#权限不够
        result = dbGuild.delGuildApplyJoinRecord(self.id, characterId)
        if result:
            player = PlayersManager().getPlayerByID(operator)
            content = Lg().g(533)%(player.baseInfo.getName(),operatorpost,self.guildinfo.get('nickname',''))
            title = Lg().g(526)
            m = Mail( title=title,type =0, senderId =-1, receiverId=characterId,\
                            sender = Lg().g(128),content=content)
            m.mailIntoDB()
            tplayer = PlayersManager().getPlayerByID(characterId)
            if tplayer:
                tplayer.quest.specialTaskHandle(ADDGUILDTASKTYPE)
        return 1
    
    def TransferCorps(self,operator,memberId):
        '''移交国长
        @param operator: int 操作者的id
        @param memberId: int 被任命的角色的id
        '''
        managementGroup = eval("["+self.guildinfo['veterans']+"]")\
                                +eval("["+self.guildinfo['staffOfficers']+"]")\
                                +eval("["+self.guildinfo['senators']+"]")
        if memberId not in managementGroup:
            return {'result':False,'message':Lg().g(534)}
        if operator!=self.president:
            return {'result':False,'message':Lg().g(515)}
        if not dbGuild.checkCharacterInGuild(memberId, self.id):
            return {'result':False,'message':Lg().g(524)}
        result = dbGuild.TransferCorps(self.id, operator, memberId)
        if result:
            self.president = memberId
            player = PlayersManager().getPlayerByID(operator)
            player.updatePlayerInfo()
            member = PlayersManager().getPlayerByID(memberId)
            
            if member:
                member.updatePlayerInfo()
            dbGuild.updateCharacterGuildInfo(memberId, {'post':4})
            membername = dbGuild.getCharacterNameByID(memberId)
            content = Lg().g(535)%\
            (self.guildinfo.get('nickname',''),membername,self.guildinfo.get('name',''),)
            title = Lg().g(526)
            for characterId in dbGuild.getAllGuildCharacterId(self.id):
                m = Mail( title=title,type =0, senderId =-1, receiverId=characterId[0],\
                            sender = Lg().g(128),content=content)
                m.mailIntoDB()
            postdict = dbGuild.updateGuildPost(self.id)
            self.veterans=postdict.veterans
            self.staffOfficers=postdict.staffOfficers
            self.senators=postdict.senators
#            self.SynchGuildInfo()
            return {'result':True,'message':Lg().g(85)}
        return {'result':False,'message':Lg().g(536)}
    
    def modifyCorpsAnnoun(self,operator,announContent):
        '''修改国公告'''
        if self.getPresident() !=operator:
            return {'result':False,'message':Lg().g(515)}
        self.announcement=announContent
        return {'result':True,'message':Lg().g(537)}
    
    def ModifyBugle(self,operator,bugleTxt):
        '''修改军号
        @param operator: int 操作者的id
        @param bugleTxt: str 军号名称
        '''
        if len(bugleTxt)!=1:
            return {'result':False,'message':Lg().g(539)}
        if self.getPresident() !=operator:
            return {'result':False,'message':Lg().g(515)}
        self.bugle=bugleTxt
        return {'result':True,'message':Lg().g(540)}
    
    def LevelUpEmblem(self,operator):
        '''升级军徽
        @param operator: int 操作者的id
        '''
        if self.MAXLEVEL <= self.get('emblemLevel'):
            return {'result':False,'message':Lg().g(542)}
        player = PlayersManager().getPlayerByID(operator)
        self.emblemLevel+=1
        result = True
        if result:
            msg = Lg().g(543)%\
            (self.guildinfo['emblemLevel'])
            pushOtherMessage(905,msg,[player.getDynamicId()])
            if self.guildinfo['emblemLevel']==20:
                utype = {1:Lg().g(544),2:Lg().g(545)}.get(self.guildinfo['camp'],Lg().g(546))
                palyername = player.baseInfo.getName(0)
                gname = self.getGuildName()
                sendmsg = Lg().g(547)%(utype,
                                            palyername,gname)
                chatnoderemote.callRemote('pushSystemToInfo',sendmsg)
            return {'result':True,'message':Lg().g(548)%(self.guildinfo['emblemLevel'])}
        return {'result':False,'message':Lg().g(549)}
    
    def getTechnologyList(self,characterId,curPage):
        '''获取科技列表'''
        limit = 12
        all_technology = dbGuild.All_TECHNOLOGY
        maxPage = int(math.ceil(len(all_technology.items())/float(limit)))
        technologylist = all_technology.values()[(curPage-1)*limit:curPage*limit]
        infos = {}
        infos['curPage'] = curPage
        infos['maxPage'] = maxPage
        infos['technologyInfo'] = []
        guildLevel = self.guildinfo['level']
        techlimit = dbGuild.lEVEL_TECHNOLOGY.get(guildLevel)
        for technology in technologylist:
            info = {}
            limitLevel = techlimit.get('tech_%d'%technology['technology'],0)
            info['technologyId'] = technology['technology']
            info['technologyImg'] = technology['icon']
            info['technologyName'] = technology['technologyName']
            info['technologyLevel'] = limitLevel
            info['remainCondition'] = u""
            info['curSchedule'] = 0
            info['maxSchedule'] =0
            info['technologyDes'] = technology['technologyDes']
            info['defaultDonate'] = False
            if limitLevel > 0:
                info['isenable'] = True
            else:
                info['isenable'] = False
            infos['technologyInfo'].append(info)
        return infos
    
    def findNewPresident(self):
        '''寻找新的行会长'''
        if eval("["+self.guildinfo['veterans']+"]"):
            return eval("["+self.guildinfo['veterans']+"]")[0]
        if eval("["+self.guildinfo['staffOfficers']+"]"):
            return eval("["+self.guildinfo['staffOfficers']+"]")[0]
        if eval("["+self.guildinfo['senators']+"]"):
            return eval("["+self.guildinfo['senators']+"]")[0]
        result = dbGuild.findNewPresident(self.id, self.getPresident())
        return result
    
    def leaveGuild(self,operator):
        '''离开行会'''
        from app.scense.core.instance.ColonizeManage import ColonizeManage
        if self.getPresident() == operator:
            newPresident =  self.findNewPresident()
            if not newPresident:
                return {'result':False,'message':Lg().g(550)}
            else:
                dbGuild.updateCharacterGuildInfo(newPresident, {'post':4})
                self.president=newPresident
#        if operator in eval("["+self.guildinfo['veterans']+"]"):
#            newstaffOfficers = str(eval("["+self.guildinfo['veterans']+"]").remove(operator))[1:-1]
#            self.update('veterans', newstaffOfficers)
#        if operator in eval("["+self.guildinfo['staffOfficers']+"]"):
#            newveterans = str(eval("["+self.guildinfo['staffOfficers']+"]").remove(operator))[1:-1]
#            self.update('staffOfficers', newveterans)
#        if operator in eval("["+self.guildinfo['senators']+"]"):
#            newsenators = str(eval("["+self.guildinfo['senators']+"]").remove(operator))[1:-1]
#            self.update('senators', newsenators)
        result = dbGuild.deleteCharacterGuildRelation(operator)
        if result:
            postdict = dbGuild.updateGuildPost(self.id)
            self.veterans=postdict.veterans
            self.staffOfficers=postdict.staffOfficers
            self.senators=postdict.senators
            player = PlayersManager().getPlayerByID(operator)
            player.updatePlayerInfo()
            playerList = dbGuild.getGuildCharacterIdList(self.id)
            msg = Lg().g(551)%player.baseInfo.getName()
            sendList = [PlayersManager().getPlayerByID(p[0]).getDynamicId()\
                         for p in playerList \
                        if PlayersManager().getPlayerByID(p[0]) and \
                        PlayersManager().getPlayerByID(p[0]).getDynamicId()]
            pushPromptedMessage(msg, sendList)
            ColonizeManage().updateGuild(operator, 0, Lg().g(143))
            return {'result':True,'message':Lg().g(552)}#开除成功
        return {'result':False,'message':Lg().g(553)}#开除失败
    
    def takeCorpsChief(self,operator):
        '''接位'''
        if self.getPresident() ==operator:
            return {'result':False,'message':Lg().g(554)}
        managementGroup = eval("["+self.guildinfo['veterans']+"]")\
                                +eval("["+self.guildinfo['staffOfficers']+"]")\
                                +eval("["+self.guildinfo['senators']+"]")
        if operator not in managementGroup:
            return {'result':False,'message':Lg().g(555)}
        self.president=operator
        return {'result':True,'message':Lg().g(556)}
    
    def pushGuildLevelUp(self,level):
        '''推送国升级的消息'''
        memberList = dbGuild.getGuildMemberIdList(self.id)
        sendlist = []
        for memberId in memberList:
            player = PlayersManager().getPlayerByID(memberId)
            if player:
                sendlist.append(player.getDynamicId())
        pushGuildLevelUpMessage(level, sendlist)
        if level==20:
            utype = {1:Lg().g(544),2:Lg().g(545)}.get(self.guildinfo['camp'],Lg().g(546))
            gname = self.getGuildName()
            msg = Lg().g(558)%(utype,gname)
            chatnoderemote.callRemote('pushSystemToInfo',msg)
    
    def addExp(self,addexp):
        '''添加经验'''
        self.lock()
        try:
            oldlevelinfo = self.get_multi(['exp','level'])
            level = oldlevelinfo.get('level')
            exp = oldlevelinfo.get('exp')+addexp
            statu = 0
            while exp>= level**2*1000:
                exp -= level**2*1000
                level+=1
                statu = 1
            if statu:
                self.pushGuildLevelUp(level)
                resultlist =True
                self.level=level
                self.exp=exp
                if resultlist:
                    result = False
                else:
                    result = True
            else:
                result =True
                self.exp=exp
            return result
        except Exception,e:
            return False
        finally:
            self.release()
            
    def ModifyJoinLevel(self,operator,levelrequired):
        '''修改国加入等级'''
        guildinfo = self.guildinfo
        if operator!=guildinfo['president']:
            return -1#权限不够
        if guildinfo['levelrequired']== levelrequired:
            return 1
        guildinfo['levelrequired'] = levelrequired
        self.levelrequired=levelrequired
        return 1#成功
    
    def GetXuYuanInfo(self):
        '''获取幸运信息
        '''
        guildInfo = self.guildinfo
        info = {}
        info['xyValue'] = guildInfo.get('fortune',0)
        info['cliffordLog'] = guildInfo.get('cliffordLog',[])
        return info
    
    def UseXingYun(self,usetype,usename):
        '''祈祷
        @param usetype: int 0四叶草1郁金香2蝴蝶兰3紫罗兰4曼陀罗
        @param usename: str 使用的角色的名称
        '''
        XINGYUN_CONFIG = {0:5,1:10,2:15,3:20,4:30}
        xingyunadd = XINGYUN_CONFIG.get(usetype)
        props = {}
        guildInfo = self.guildinfo
#        self.fortune = guildInfo.get('fortune',0)+xingyunadd
        info = {'name':usename,'type':usetype}
        cliffordLog = guildInfo.get('cliffordLog',[])
        cliffordLog.append(info)
        self.cliffordLog = cliffordLog[-7:]
        return xingyunadd
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
    