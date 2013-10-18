#coding:utf8
'''
Created on 2011-12-20

@author: SIOP_09
'''
from app.scense.core.language.Language import Lg


class InstanceColonize():
    '''副本殖民'''
    

    def __init__(self,id):
        '''
        Constructor
        '''
        self.pid=0 #角色id
        self.pname=u"" #角色名称
        self.gid=0 #行会id
        self.gname=Lg().g(143) #行会名称
        self.resist=0 #成功卫冕次数
        self.inintInstanceColonize(id)

    def inintInstanceColonize(self,id):
        '''初始化副本殖民类'''
#        instancegroupid=InstanceGroupManage().getFristInstanceBy(id)
#        info=ColonizeManage().getInstanceInfoByid(instancegroupid)#根据副本组id获取副本信息
#        if info['pid']<1: #如果副本占领者角色小于1 说明副本没有被占领
#            return
#        self.pid=info['pid'] #角色id
#        self.pname=info['pname'] #角色名称
#        self.gid=info['gid'] #行会id
#        self.gname=info['gname'] #行会名称
#        self.resist=info['resist'] #成功卫冕次数
#        self.clearancecount=info['clearancecount'] #通关次数