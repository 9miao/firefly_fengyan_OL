#coding:utf8
'''
Created on 2011-9-21
排行榜
@author: SIOP_09
'''
from app.scense.core.toplist.TopList import TopList
from app.scense.applyInterface import pingfen
from app.scense.serverconfig.node import nodeHandle
from app.scense.protoFile.top import GetRankingListInfo2001_pb2
from app.scense.protoFile.top import GetMyScoreInfo2002_pb2
from app.scense.core.language.Language import Lg

@nodeHandle
def getTopList_2001(dynamicId, request_proto):
    argument=GetRankingListInfo2001_pb2.GetRankingListInfoRequest()
    argument.ParseFromString(request_proto)
    response=GetRankingListInfo2001_pb2.GetRankingListInfoResponse()
    
    id=argument.id#角色id
    rankingType=argument.rankingType #排行分类类型 1角色等级排行2个人战力排行3国等级排行4国战力排行
    
    data,date,times=TopList().getTop(id, rankingType)
    if not data:
        response.result=False
        response.message=u"getTopList"+Lg().g(621)
        response.data.rankingInfo.extend([])
        return response.SerializeToString()
    
    response.result=True
    response.message=Lg().g(166)
    if date:
        response.data.myRanking=str(date)
        try:
            response.data.refreshTime=times
        except Exception:
            response.data.refreshTime=times.decode('utf8')
    else:
        response.data.myRanking=Lg().g(339)
        try:
            response.data.refreshTime=times
        except Exception:
            response.data.refreshTime=times.decode('utf8')
        
#    tag=(curPage-1)*10+1
    tag=1#排名 (int)
    for item in data:
        val=response.data.rankingInfo.add()
        val.param1=str(tag)
        if item.get('topnum',0)>0:
            val.param1=str(item.get('topnum',0))
        if rankingType>=1 and rankingType<=2: #角色类
            val.id=id
            try:
                val.param2 = item.get('name','')
            except Exception:
                val.param2=item.get('name').decode('utf8')
            try:
                val.param3=item.get('guildname')
            except Exception:
                val.param3=item.get('guildname').decode('utf8')
            val.param4=__FS(item.get('profession'))
            val.param5=str(item.get('orther'))
        elif rankingType==3 or rankingType==4: #行会类
            val.id=int(item.get('id'))
            val.param2=item.get('name')
            val.param3=item.get('nickname')
            val.param4=str(item.get('level'))
            val.param5=str(item.get('other'))
        tag=tag+1
    return response.SerializeToString()



def __FS(typeid):
    if typeid==1:
        return Lg().g(390)
    elif typeid==2:
        return Lg().g(391)
    elif typeid==3:
        return Lg().g(392)
    elif typeid==4:
        return Lg().g(393)

@nodeHandle
def pingFen_2002(dynamicId, request_proto):
    argument=GetMyScoreInfo2002_pb2.GetMyScoreInfoRequest()
    argument.ParseFromString(request_proto)
    response=GetMyScoreInfo2002_pb2.GetMyScoreInfoResponse()
    

    characterid=argument.id #角色id
    data=pingfen.getPFenByCharacterId(characterid)
    if not data or len(data)<1:
        response.result=False
        response.message=Lg().g(622)
        return response.SerializeToString()
    response.result=True
    response.message=Lg().g(166)
    
    for item in data:
        it=response.data.add()
        it.score=item.get('pf')#评分
        itemm=item.get('item')
        itemm.SerializationItemInfo(it.itemsInfo)
    return response.SerializeToString()
    