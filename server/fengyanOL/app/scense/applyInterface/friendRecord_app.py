#coding:utf8
'''
Created on 2011-11-24
祝福记录操作
@author: SIOP_09
'''
count=10 #每个角色最高祝福次数上限
zf={}  #key: pid    value: 祝福次数


def addZF(pid):
    '''添加角色祝福次数
    @param pid: int 角色id
    '''
    global zf
    
    if zf.has_key(pid):
        zf[pid]=zf[pid]+1
    else:
        zf[pid]=1

def getRecord(pid):
    '''获取角色祝福次数
    @param id: int 当前角色id
    '''
    global zf
    if zf.has_key(pid):
        return zf[pid] #如果这个好友祝福次数有记录返回记录数量
    return 0 #如果这个好友祝福次数没有记录，那么返回好友记录数量为

def clean():
    '''清空所有祝福记录次数'''
    global zf
    zf={}