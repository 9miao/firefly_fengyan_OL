#coding:utf8
'''
Created on 2011-8-29

@author: SIOP_09
'''
from app.scense.utils import dbaccess

flist=['level','ExpRequired','ExpSecProduce']
def getExpSecProduceBylevel(level):
    '''根据角色等级获取秒产经验
    @param level: int  角色的等级
    '''
    sql="select * from tb_experience where level="+level+" "
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result=cursor.fetchone()
    cursor.close()
    data={}#存放查询出来的信息
    if result:
        for i in range(len(flist)):
            data[flist[i]]=result[i]
        return data
    return None
        
            
            
    