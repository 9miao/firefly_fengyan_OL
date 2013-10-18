#coding:utf8
'''
Created on 2013-1-8
战役类
@author: lan
'''
from zhangjie import ZhangJie
from app.scense.utils.dbopera import db_zhanyi,dbMonster

class ZhanYi:
    '''战役类
    '''
    
    def __init__(self,yid):
        '''初始化
        @param yid: int 战役的ID
        '''
        self.yid = yid
        self.yname = ''#战役的名称
        self.desc = ''#战役的描述
        self.monsterId = ''#战役的首领的ID
        self.zhangjieSet = {}#战役中所有章节的信息
        self.initdata()
        
    def initdata(self):
        '''写入战役的数据
        '''
        data = db_zhanyi.ALL_ZHANYI_INFO.get(self.yid)
        zhangjielist = db_zhanyi.ALL_ZHANGJIE_GROP.get(self.yid)
        if not data:
            raise Exception(u'战役（%d）信息不存在'%self.yid)
        for zid in zhangjielist:
            self.zhangjieSet[zid] = ZhangJie(zid)
        self.yname = data.get('name')
        self.desc = data.get('desc')
        self.monsterId = data.get('monsterID')
        
        
    def formatInfo(self,zy,zj):
        '''格式化战役的数据
        '''
        info = {}
        info['id'] = self.yid
        info['name'] = self.yname
        info['desc'] = self.desc
        if self.yid>zy:
            info['state'] = 1
        elif self.yid==zy:
            info['state'] = 2
        else:
            info['state'] = 3
        info['monster'] = dbMonster.All_MonsterInfo.get(self.monsterId)
        info['zhangjielist'] = [zjobj.formatInfo(zj) for zjobj in self.zhangjieSet.values()]
        return info
    
    