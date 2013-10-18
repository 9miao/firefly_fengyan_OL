#coding:utf8
'''
Created on 2012-5-31
宠物商店
@author: jt
'''
from app.scense.utils import dbaccess
from MySQLdb.cursors import DictCursor
dbpool=dbaccess.dbpool

def getByid(pid):
    '''根据角色id获取宠物商店信息'''
    sql = "SELECT * FROM tb_pet_shop where pid=%s"%pid
    cursor = dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result=cursor.fetchone()
    if result:
        return result
    return None


def addInfo(pid,shop1,shop2,shop3,ctime,counts,ioption,xy,cs):
    '''添加记录
    @param shop1: str 商店1信息
    @param shop2: str 商店2信息
    @param shop3: str 商店3信息
    @param cs: int 剩余免费次数
    '''
    sql="insert  into `tb_pet_shop`(`pid`,`shop1`,`shop2`,`shop3`,`ctime`,`counts`,`ioption`,`xy`,`cs`) values (%s,'%s','%s','%s','%s',%s,%s,%s,%s)"%(pid,shop1,shop2,shop3,ctime,counts,ioption,xy,cs)
    cursor = dbpool.cursor()
    count = cursor.execute(sql)
    dbpool.commit()
    cursor.close()
    if count >= 1:
        return True
    else:
        return False

    
def updateInfo(pid,shop1,shop2,shop3,ctime,counts,ioption,xy,cs):
    '''更改宠物商店记录
    @param pid: int 角色id
    @param ctime: str 冷却开始时间
    @param counts: int 冷却持续时间
    @param ioption: int 消费提示打开状态  1开启消费提示  -1 关闭消费提示 
    @param cs: int 剩余免费次数
    '''
    sql="UPDATE tb_pet_shop SET shop1='%s',shop2='%s',shop3='%s',ctime='%s',counts=%s,ioption=%s,xy=%s,cs=%s WHERE pid=%s"%(shop1,shop2,shop3,ctime,counts,ioption,xy,cs,pid)
    cursor = dbpool.cursor()
    count = cursor.execute(sql)
    dbpool.commit()
    cursor.close()
    if count >= 1:
        return True
    else:
        return False
    