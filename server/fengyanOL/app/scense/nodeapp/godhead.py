#coding:utf8
'''
Created on 2012-5-15

@author: Administrator
'''
from app.scense.applyInterface import godhead
from app.scense.serverconfig.node import nodeHandle
from app.scense.protoFile.godhead import GetShenChiInfo3400_pb2
from app.scense.protoFile.godhead import ActiveShenGe3401_pb2

@nodeHandle
def GetShenChiInfo_3400(dynamicId,request_proto):
    '''获取神格信息
    '''
    argument = GetShenChiInfo3400_pb2.GetShenChiInfoRequest()
    argument.ParseFromString(request_proto)
    response = GetShenChiInfo3400_pb2.GetShenChiInfoResponse()
    characterId = argument.id
    headtype = argument.page
    
    data = godhead.getGodheadInfo(dynamicId,characterId, headtype)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    if data.get('data',None):
        godheadlistinfos = data.get('data')
        response.shenChiInfo.douqi = godheadlistinfos.get('douqi')
        try:
            response.shenChiInfo.des = godheadlistinfos.get('des')
        except:
            response.shenChiInfo.des = godheadlistinfos.get('des').decode('utf8')
        response.shenChiInfo.curPage = godheadlistinfos.get('curPage')
        response.shenChiInfo.maxPage = godheadlistinfos.get('maxPage')
        response.shenChiInfo.nextBtnFlag = godheadlistinfos.get('nextBtnFlag')
        shenGeInfolist = response.shenChiInfo.shenGeList
        for godheadinfo in godheadlistinfos.get('shenGeList',[]):
            shenGeInfo = shenGeInfolist.add()
            for key,value in godheadinfo.items():
                try:
                    setattr(shenGeInfo,key,value)
                except:
                    setattr(shenGeInfo,key,value.decode('utf8'))
    return response.SerializeToString()


@nodeHandle
def ActiveShenGe_3401(dynamicId,request_proto):
    '''激活神格'''
    argument = ActiveShenGe3401_pb2.ActiveShenGeRequest()
    argument.ParseFromString(request_proto)
    response = ActiveShenGe3401_pb2.ActiveShenGeResponse()
    characterId = argument.id
    godheadid = argument.sgID
    data = godhead.ActiveGodhead(dynamicId,characterId, godheadid)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    return response.SerializeToString()
        
        
        
        