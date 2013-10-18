#coding:utf8
'''
Created on 2011-8-27
@author: SIOP_09
'''

from app.scense.utils import dbaccess
from MySQLdb.cursors import DictCursor
from twisted.python import log
instance_dAll={}

def getInstance_dByid(id):
    '''根据副本id获得组队副本中需要的副本信息
    @param id: int #组队副本信息
    '''
    if instance_dAll.has_key(id):
        i= instance_dAll.get(id)
        info={}
        info['context']=i['context']
        info['dropitem']=i['dropitem']
        info['id']=i['id']
        info['instanceid']=i['instanceid']
        info['instancename']=i['instancename']
        info['moster']=i['moster']
        return info
    
    
    log.err(u"tb_instance_d表中没有instanceid=%S"%id)
    return None
    
    
#    sql="select * from tb_instance_d where instanceid="+str(id)
#    cursor=dbaccess.dbpool.cursor(cursorclass=DictCursor)
#    cursor.execute(sql)
#    result = cursor.fetchone()
#    cursor.close()
#    if not result:
#        return None
#    if result:
#        itemlist=eval("["+result['dropitem']+"]")
#        mosterlist=eval("["+result['moster']+"]")
#        result['dropitem']=itemlist
#        result['moster']=mosterlist
#        if len(itemlist)>2:
#            result['dropitem']=itemlist[:10]
#        if len(mosterlist)>1:
#            result['dropitem']=itemlist[:1]
#    return result

def getInstance_dAll():
    '''获取所有副本掉落信息'''
    instance_dAll222={}
    sql="select * from tb_instance_d "
    cursor=dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    val = cursor.fetchall()
    cursor.close()
    if not val:
        return None
    for result in val:
        itemlist=eval("["+result['dropitem']+"]")
        mosterlist=eval("["+result['moster']+"]")
        result['dropitem']=itemlist
        result['moster']=mosterlist
        if len(itemlist)>2:
            result['dropitem']=itemlist[:10]
        if len(mosterlist)>1:
            result['dropitem']=itemlist[:1]
        instance_dAll222[result['instanceid']]=result
    return instance_dAll222