#coding:utf8
'''
Created on 2011-8-19
@author: SIOP_09
'''

#from twisted.python import log
from app.scense.core.instance.WinManager import WinManager
from app.scense.core.instance.InstanceGroupManage import InstanceGroupManage
from app.scense.core.language.Language import Lg
count=10 #殖民消息最多多少条
listt=[]#存放殖民特权消息  #最多存储10条公共信息

instancemessage={} #key:副本组id  value:[ [时间，内容],[],[]] 


def updatethis(lists,instancemessages):
    global listt
    listt=lists
    global instancemessage
    instancemessage=instancemessages
    
def outGuild(pid,pname,gname):
    from app.scense.core.instance.ColonizeManage import ColonizeManage
    for info in ColonizeManage().getI().values():
                if info['pid']==pid:
                    mmg=Lg().g(208)%(info['name'],pname,gname)
                    addmessage(mmg,type=1,id=info['id'])

def addmessage(strs,type=0,id=0):
    '''添加殖民信息
    @param strs: string 内容
    @param type: int 1表是加入多副本信息中   0不是不加入副本信息中
    @param id: int 副本组id
    '''
    import datetime,time
#    from serverconfig.publicnode import publicnoderemote
    global listt
    global instancemessage
    if len(listt)>count:
        del listt[0]
    listt.append(strs)
    if type==1: 
        if instancemessage.has_key(id):
            instancemessage[id].append([str(datetime.datetime.fromtimestamp(time.time())),strs])
        else:
            instancemessage[id]=[]
            instancemessage[id].append([str(datetime.datetime.fromtimestamp(time.time())),strs])
#    publicnoderemote.callRemote('public_winning_appupate',listt, instancemessage)

def getpublicstr():
    '''获取殖民特权输出信息'''
    ss=u""
    global listt
    if len(listt)>0:
        for item in listt:
            try:
                ss+=item+u"<br/>"
            except:
                print listt
                print u"------------------------------------------"
                print item
                
    return ss
        

def getStr(instanceid):
    '''根据副本id获取字符串'''
    groupid=InstanceGroupManage().getFristInstanceBy(instanceid)#根据副本id获取副本组id
    ss=u''
    lists=[]
    global instancemessage
    if instancemessage.has_key(groupid):
        listte=instancemessage[groupid]
        for item in listte:
            lists.append(u'%s<br/>%s<br/>'%(item[0],item[1]))
        ss=ss.join(lists)

    return[ss,getCountByid(groupid)]

def set0():
    '''清空副本输出信息'''
#    from serverconfig.publicnode import publicnoderemote
    global instancemessage
    global listt
    instancemessage.clear()
    listt=[]
#    publicnoderemote.callRemote('public_winning_appupate',listt, instancemessage)
        
def getCountByid(id):
    '''根据副本组id获取此副本被攻打次数
    @param id: int 副本组id
    '''
    count=0
    global instancemessage
    if instancemessage.has_key(id):
        count=len(instancemessage[id])#记录数
    return count

def getmessage():
    '''获得消息信息'''
    return listt

def getWinning(pid):
    '''获取连胜次数'''
    return WinManager().getcount(pid)

def updateWinning(pid,flg):
    '''
    @param flg: boo 挑战成功或者失败
    '''
    
    if flg:#如果挑战成功
        WinManager().add(pid) #添加连胜
        
    else:#挑战失败
        WinManager().set0(pid)#设置连胜0
        
