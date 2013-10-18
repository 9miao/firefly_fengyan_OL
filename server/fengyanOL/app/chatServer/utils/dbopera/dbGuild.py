#coding:utf8
'''
Created on 2011-9-13
行会（国）数据库处理
@author: lan
'''
from app.chatServer.utils import dbaccess
from MySQLdb.cursors import DictCursor
from app.chatServer.core.GuildManager import GuildManager

def getGuildidBypid(pid):
    ''' 获取行会id
    @param pid: int 角色id
    '''
    sql = "SELECT guildId FROM tb_guild_character  WHERE characterId=%s"%pid
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    if not result:
        return None
    return result['guildId']
    
def setAllGuild():
    '''把角色添加到行会中'''
    sql="SELECT characterId,guildId FROM tb_guild_character"
    cursor = dbaccess.dbpool.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    if not result:
        return
    for item in result:
        GuildManager().add(item['characterId'], item['guildId'])
    
