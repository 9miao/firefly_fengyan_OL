'''
Created on 2012-7-10

@author: jt
'''

class HlManage(object):
    '''角色领取活力值记录'''


    def __init__(self):
        ''''''
        self.info={}
        
    def add(self,pid,count=1):
        '''添加活力值领取次数'''
        if self.info.has_key(pid):
            self.info[pid]+=1
        else:
            self.info[pid]=1
            
    def clean(self):
        '''清除所有角色活力值领取限制'''
        self.info={}
        
    def getCount(self,pid):
        '''获取角色领取的次数'''
        if self.info.has_key(pid):
            return self.info[pid]
        return 0
        