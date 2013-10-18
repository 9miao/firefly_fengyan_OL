#coding:utf8
'''
Created on 2011-9-29
物品合成
@author: SIOP_09
'''
from app.scense.utils import dbaccess
tb_compose_name=None

def getBytemplateid(itemtemplateid):
    '''根据物品模板id获取合成所需信息
    @param itemtemplateid: int 物品模板id
    '''
    sql="select * from tb_compose where goal="+str(itemtemplateid)
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result=cursor.fetchone() #当前页的信息
    data={} #存放一条数据
    cursor.close()
    if not result:
        return None
    for i in range(len(tb_compose_name)):
        data[tb_compose_name[i]]=result[i]
    if not data:
        return None
    return data