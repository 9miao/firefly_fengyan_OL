#coding:utf8
'''
Created on 2012-7-3
VIP信息
@author: Administrator
'''
from app.scense.serverconfig.node import nodeHandle

from app.scense.applyInterface import vipinfo
from app.scense.protoFile.vip import GetVIPInfo_3800_pb2

@nodeHandle
def GetVIPInfo_3800(dynamicId, request_proto):
    '''获取VIP信息
    '''
    argument = GetVIPInfo_3800_pb2.GetVIPInfoRequest()
    argument.ParseFromString(request_proto)
    response = GetVIPInfo_3800_pb2.GetVIPInfoResponse()
    
    dynamicId = dynamicId
    characterId = argument.id
    result = vipinfo.GetVipInfo_3800(dynamicId, characterId)
    response.result = result.get('result',False)
    response.message = result.get('message','')
    if result.get('data',None):
        data = result.get('data')
        response.data.viplevel = data.get('level',0)
        response.data.exp = int(data.get('exp',0))
        response.data.maxexp = data.get('maxexp',0)
        response.data.msg = data.get('msg','')
        vipresponse = response.data.vipinfo
        vipinfolist = data.get('vipinfo',[])
        for _vipinfo in vipinfolist:
            viprp = vipresponse.add()
            viprp.funcname = _vipinfo['name']
            viprp.vip1cnt = str(_vipinfo['Vip1'])
            viprp.vip2cnt = str(_vipinfo['Vip2'])
            viprp.vip3cnt = str(_vipinfo['Vip3'])
            viprp.vip4cnt = str(_vipinfo['Vip4'])
            viprp.vip5cnt = str(_vipinfo['Vip5'])
            viprp.vip6cnt = str(_vipinfo['Vip6'])
            viprp.vip7cnt = str(_vipinfo['Vip7'])
            viprp.vip8cnt = str(_vipinfo['Vip8'])
            viprp.vip9cnt = str(_vipinfo['Vip9'])
            viprp.vip10cnt = str(_vipinfo['Vip10'])
    return response.SerializeToString() 
        
        
        
        
        
        
