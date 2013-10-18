#coding:utf8
'''
Created on 2012-4-15
VIP 功能开启记录
@author: Administrator
'''
from app.scense.utils import dbaccess
from MySQLdb.cursors import DictCursor
from app.scense.core.language.Language import Lg

VIPPERM = {}#vip权限
ALLLIBAO = {}#所有的礼包类型
VIPEXP = {}#VIP经验配置表
VIPINFO = []#VIP信息


def initVIPInfo(data):
    '''初始化VIP信息
    '''
    global VIPINFO
    VIPINFO = []
    info = {'name':Lg().g(625),'Vip1':data[1]['cardnum'],
                  'Vip2':data[2]['cardnum'],'Vip3':data[3]['cardnum'],
                  'Vip4':data[4]['cardnum'],'Vip5':data[5]['cardnum'],
                  'Vip6':data[6]['cardnum'],'Vip7':data[7]['cardnum'],
                  'Vip8':data[8]['cardnum'],'Vip9':data[9]['cardnum'],
                  'Vip10':data[10]['cardnum']}
    VIPINFO.append(info)
    info = {'name':Lg().g(626),'Vip1':data[1]['turncointimes'],
                  'Vip2':data[2]['turncointimes'],'Vip3':data[3]['turncointimes'],
                  'Vip4':data[4]['turncointimes'],'Vip5':data[5]['turncointimes'],
                  'Vip6':data[6]['turncointimes'],'Vip7':data[7]['turncointimes'],
                  'Vip8':data[8]['turncointimes'],'Vip9':data[9]['turncointimes'],
                  'Vip10':data[10]['turncointimes']}
    VIPINFO.append(info)
    info = {'name':Lg().g(627),'Vip1':data[1]['turnexptimes'],
                  'Vip2':data[2]['turnexptimes'],'Vip3':data[3]['turnexptimes'],
                  'Vip4':data[4]['turnexptimes'],'Vip5':data[5]['turnexptimes'],
                  'Vip6':data[6]['turnexptimes'],'Vip7':data[7]['turnexptimes'],
                  'Vip8':data[8]['turnexptimes'],'Vip9':data[9]['turnexptimes'],
                  'Vip10':data[10]['turnexptimes']}
    VIPINFO.append(info)
    info = {'name':Lg().g(628),'Vip1':data[1]['turnenergytimes'],
                  'Vip2':data[2]['turnenergytimes'],'Vip3':data[3]['turnenergytimes'],
                  'Vip4':data[4]['turnenergytimes'],'Vip5':data[5]['turnenergytimes'],
                  'Vip6':data[6]['turnenergytimes'],'Vip7':data[7]['turnenergytimes'],
                  'Vip8':data[8]['turnenergytimes'],'Vip9':data[9]['turnenergytimes'],
                  'Vip10':data[10]['turnenergytimes']}
    VIPINFO.append(info)
    info = {'name':Lg().g(629),'Vip1':2,
                  'Vip2':3,'Vip3':3,
                  'Vip4':4,'Vip5':4,
                  'Vip6':4,'Vip7':4,
                  'Vip8':4,'Vip9':4,
                  'Vip10':4}
    VIPINFO.append(info)
    info = {'name':Lg().g(630),'Vip1':data[1]['arenatimes'],
                  'Vip2':data[2]['arenatimes'],'Vip3':data[3]['arenatimes'],
                  'Vip4':data[4]['arenatimes'],'Vip5':data[5]['arenatimes'],
                  'Vip6':data[6]['arenatimes'],'Vip7':data[7]['arenatimes'],
                  'Vip8':data[8]['arenatimes'],'Vip9':data[9]['arenatimes'],
                  'Vip10':data[10]['arenatimes']}
    VIPINFO.append(info)
    info = {'name':Lg().g(631),'Vip1':data[1]['finishedMining'],
                  'Vip2':data[2]['finishedMining'],'Vip3':data[3]['finishedMining'],
                  'Vip4':data[4]['finishedMining'],'Vip5':data[5]['finishedMining'],
                  'Vip6':data[6]['finishedMining'],'Vip7':data[7]['finishedMining'],
                  'Vip8':data[8]['finishedMining'],'Vip9':data[9]['finishedMining'],
                  'Vip10':data[10]['finishedMining']}
    VIPINFO.append(info)
    info = {'name':Lg().g(632),'Vip1':data[1]['finishedTrain'],
                  'Vip2':data[2]['finishedTrain'],'Vip3':data[3]['finishedTrain'],
                  'Vip4':data[4]['finishedTrain'],'Vip5':data[5]['finishedTrain'],
                  'Vip6':data[6]['finishedTrain'],'Vip7':data[7]['finishedTrain'],
                  'Vip8':data[8]['finishedTrain'],'Vip9':data[9]['finishedTrain'],
                  'Vip10':data[10]['finishedTrain']}
    VIPINFO.append(info)
    info = {'name':Lg().g(633),'Vip1':'10%',
                  'Vip2':'20%','Vip3':'30%',
                  'Vip4':'40%','Vip5':'50%',
                  'Vip6':'60%','Vip7':'70%',
                  'Vip8':'80%','Vip9':'90%',
                  'Vip10':'100%'}
    VIPINFO.append(info)
    info = {'name':Lg().g(634),'Vip1':'10%',
                  'Vip2':'20%','Vip3':'30%',
                  'Vip4':'40%','Vip5':'50%',
                  'Vip6':'60%','Vip7':'70%',
                  'Vip8':'80%','Vip9':'90%',
                  'Vip10':'100%'}
    VIPINFO.append(info)
    info = {'name':Lg().g(635),'Vip1':'10%',
                  'Vip2':'20%','Vip3':'30%',
                  'Vip4':'40%','Vip5':'50%',
                  'Vip6':'60%','Vip7':'70%',
                  'Vip8':'80%','Vip9':'90%',
                  'Vip10':'100%'}
    VIPINFO.append(info)
    info = {'name':Lg().g(636),'Vip1':'10%',
                  'Vip2':'20%','Vip3':'30%',
                  'Vip4':'40%','Vip5':'50%',
                  'Vip6':'60%','Vip7':'70%',
                  'Vip8':'80%','Vip9':'90%',
                  'Vip10':'100%'}
    VIPINFO.append(info)
    info = {'name':Lg().g(637),'Vip1':'10%',
                  'Vip2':'20%','Vip3':'30%',
                  'Vip4':'40%','Vip5':'50%',
                  'Vip6':'60%','Vip7':'70%',
                  'Vip8':'80%','Vip9':'90%',
                  'Vip10':'100%'}
    VIPINFO.append(info)

def getVIPExp():
    global VIPEXP
    sql = "SELECT * FROM tb_vipexp"
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result=cursor.fetchall()
    cursor.close()
    for vipp in result:
        VIPEXP[vipp['viplevel']] = vipp['maxexp']

def getAllVIPPer():
    '''获取所有VIP权限配置'''
    global VIPPERM
    sql = "SELECT * FROM tb_vippermissions"
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result=cursor.fetchall()
    cursor.close()
    for vipp in result:
        VIPPERM[vipp['viplevel']] = vipp
    initVIPInfo(VIPPERM)
        
def getAllLibao():
    '''获取所有技能的信息'''
    global ALLLIBAO
    sql = "SELECT * FROM tb_libao"
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result=cursor.fetchall()
    cursor.close()
    for libao in result:
        ALLLIBAO[libao['id']] = libao

def vipCertification(permkey,viplevel,**kw):
    '''vip权限认证
    @param permkey: str 权限名称
    '''
    vipperm = VIPPERM.get(viplevel)
    if not vipperm:
        return False
    if permkey == 'cardnum':#翻牌子的数量
        nowtimes = kw.get('nowtimes')
        if nowtimes >= vipperm.get('cardnum'):
            return False
    elif permkey == 'turncointimes':
        nowtimes = kw.get('nowtimes')
        if nowtimes > vipperm.get('turncointimes'):
            return False
    elif permkey == 'turnexptimes':
        nowtimes = kw.get('nowtimes')
        if nowtimes > vipperm.get('turnexptimes'):
            return False
    elif permkey == 'turnexptimes':
        nowtimes = kw.get('nowtimes')
        if nowtimes > vipperm.get('turnexptimes'):
            return False
    elif permkey == 'petflow':
        if not vipperm.get('petflow'):
            return False
    elif permkey == 'turnenergytimes':
        nowtimes = kw.get('nowtimes')
        if nowtimes > vipperm.get('turnenergytimes'):
            return False
    elif permkey == 'arenatimes':
        nowtimes = kw.get('nowtimes')
        if nowtimes >= vipperm.get('arenatimes'):
            return False
    elif permkey == 'finishedMining':
        nowtimes = kw.get('nowtimes')
        if nowtimes >= vipperm.get('finishedMining'):
            return False
    elif permkey == 'finishedTrain':
        nowtimes = kw.get('nowtimes')
        if nowtimes >= vipperm.get('finishedTrain'):
            return False
    elif permkey == 'climbtimes':
        nowtimes = kw.get('nowtimes')
        if nowtimes >= vipperm.get('climbtimes'):
            return False
    elif permkey == 'wish_0_times':
        nowtimes = kw.get('nowtimes')
        if nowtimes >= vipperm.get('wish_0_times'):
            return False
    elif permkey == 'wish_1_times':
        nowtimes = kw.get('nowtimes')
        if nowtimes >= vipperm.get('wish_1_times'):
            return False
    elif permkey == 'wish_2_times':
        nowtimes = kw.get('nowtimes')
        if nowtimes >= vipperm.get('wish_2_times'):
            return False
    elif permkey == 'wish_3_times':
        nowtimes = kw.get('nowtimes')
        if nowtimes >= vipperm.get('wish_3_times'):
            return False
    elif permkey == 'wish_4_times':
        nowtimes = kw.get('nowtimes')
        if nowtimes >= vipperm.get('wish_4_times'):
            return False
    return True

def getVipZhekou(viplevel):
    vipperm = VIPPERM.get(viplevel)
    if not vipperm:
        return 100
    return vipperm.get('zhekou')

def getViplibaod(viplevel,lingquguo):
    '''获取当前vip等级可领取礼包的ID
    @param viplevel: int 当前vip等级
    @param lingquguo: int 领取过礼包的vip等级
    '''
    if lingquguo >= viplevel:
        return 0,viplevel
    for vl in range(lingquguo+1,viplevel+1):
        vipperm = VIPPERM.get(vl)
        if vipperm and vipperm.get('libaoId'):
            return vipperm.get('libaoId'),vl
    return 0,viplevel

    




