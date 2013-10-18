#coding:utf8
'''
Created on 2013-1-8
战役的章节
@author: lan
'''

from app.scense.utils.dbopera import db_zhanyi,dbMonster

class ZhangJie:
    '''战役的章节'''
    
    def __init__(self,zid):
        '''初始化章节的信息
        '''
        self.zid = zid#章节的ID
        self.zname = ''#章节的名称
        self.desc = ''#章节的描述
        self.monsterId = ''#章节首领的ID
        self.initdata()
        
    def initdata(self):
        '''写入数据
        '''
        data = db_zhanyi.ALL_ZHANGJIE_INFO.get(self.zid)
        if not data:
            raise Exception(u'章节（%d）信息不存在'%self.yid)
        self.zname = data.get('name')
        self.desc = data.get('desc')
        self.monsterId = data.get('monsterID')
        
    def formatInfo(self,zj):
        '''格式化章节的数据
        '''
        info = {}
        info['zhangjieid'] = self.zid
        info['name'] = self.zname
        info['desc'] = self.desc
        if self.zid>zj:
            info['state'] = 1
        elif self.zid==zj:
            info['state'] = 2
        else:
            info['state'] = 3
        info['monster'] = dbMonster.All_MonsterInfo.get(self.monsterId)
        return info
    
    
    
    
    