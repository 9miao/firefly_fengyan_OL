#coding:utf8
'''
Created on 2011-8-29
@author: SIOP_09
'''
from app.scense.utils import dbaccess
tb_hook_Column_name=[]

def getHookByid(id):
    '''根据角色id获取挂机信息
    @param id: int 角色id
    '''
    sql="select * from tb_hook where characterid="+str(id)
    data={}
    cursor = dbaccess.dbpool.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    if result:
        for i in range(len(tb_hook_Column_name)):
            data[tb_hook_Column_name[i]]=result[i]
        return data
    return None

def addHook(characterid,multiple,hours,money,experience,miaojingyan):
    '''添加一个挂机信息
    @param characterid: int 挂机角色的id
    @param multiple: int 挂机的倍数  （用户选的+vip等级）
    @param hours: int 挂机的小时数
    @param money: int 总共花费多少游戏币
    @param experience: int 总共多少经验
    @param miaojingyan: int 每秒产生的经验值
    '''
    sql="insert  into `tb_hook`(`characterid`,`multiple`,`hours`,`money`,`experience`,`miaojingyan`) values (%d,%d,%d,%d,%d,%d)"%(characterid,multiple,hours,money,experience,miaojingyan)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False

def delHookByid(id):
    '''根据角色id删除挂机信息
    @param id: int 角色信息
    '''
    sql="delete from tb_hook where characterid="+str(id)
    cursor = dbaccess.dbpool.cursor()
    count = cursor.execute(sql)
    dbaccess.dbpool.commit()
    cursor.close()
    if count>=1:
        return True
    return False
    
    