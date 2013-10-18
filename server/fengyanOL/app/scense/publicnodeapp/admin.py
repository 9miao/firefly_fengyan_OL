#coding:utf8
'''
Created on 2012-4-17
游戏管理功能接口
@author: Administrator
'''
#from serverconfig.publicnode import publicnodeHandle
#from app.scense.core.PlayersManager import PlayersManager
#from app.scense.core.character.PlayerCharacter import PlayerCharacter
#
#@publicnodeHandle
#def recharge(playerId):
#    '''充值消息通知
#    '''
#    player = PlayersManager().getPlayerByID(playerId)
#    player.finance.updateRecharge()
#    player.pushInfoChanged()
#
#@publicnodeHandle
#def pushSystemMSG(strInfo):
#    from serverconfig.chatnode import pushSystemInfo
#    '''推送系统公告'''
#    pushSystemInfo(strInfo)
#    
#@publicnodeHandle
#def updatePlayerInfo(playerId,opearstr):
#    '''更新角色信息
#    @param playerId: int 角色的id
#    @param opearType: str 操作的脚本
#    '''
#    player = PlayersManager().getPlayerByID(playerId)
#    try:
#        if player:
#            exec(opearstr)
#        else:
#            player = PlayerCharacter(playerId)
#            exec(opearstr)
#    except:
#        return False
#    player.pushInfoChanged()
#    return True
#
#@publicnodeHandle
#def reloadModule():
#    '''重新加载模块
#    '''
#    try:
#        import restart
#        reload(restart)
#        restart.ModuleLoader()
#    except Exception,e:
#        pass
    
    
