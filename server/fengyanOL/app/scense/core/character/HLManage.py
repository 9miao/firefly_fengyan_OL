'''
Created on 2012-7-10

@author: jt
'''

class HlManage(object):
    '''��ɫ��ȡ����ֵ��¼'''


    def __init__(self):
        ''''''
        self.info={}
        
    def add(self,pid,count=1):
        '''��ӻ���ֵ��ȡ����'''
        if self.info.has_key(pid):
            self.info[pid]+=1
        else:
            self.info[pid]=1
            
    def clean(self):
        '''������н�ɫ����ֵ��ȡ����'''
        self.info={}
        
    def getCount(self,pid):
        '''��ȡ��ɫ��ȡ�Ĵ���'''
        if self.info.has_key(pid):
            return self.info[pid]
        return 0
        