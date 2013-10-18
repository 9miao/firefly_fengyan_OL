#coding:utf8
'''
Created on 2012-7-16
祈祷
@author: jt
'''
from app.scense.serverconfig.node import nodeHandle
from app.scense.core.pray.PrayManage import PrayManage

from app.scense.protoFile.pray import a4100_pb2

@nodeHandle
def pray_4100(dynamicId, request_proto):
    '''获取祈祷信息'''
    argument = a4100_pb2.GetPrayInfoRequest()
    argument.ParseFromString(request_proto)
    response = a4100_pb2.GetPrayInfoResponse()
    
    dynamicId = dynamicId
    pid = argument.id
    qd=argument.qd #true:祈祷   false:查看
    data=None
    if qd:#如果是点击祈祷
        if PrayManage().updateQd(pid):
            data = PrayManage().getQdInfo(pid)
    else:#查看祈祷面板信息
        data = PrayManage().getQdInfo(pid) #[mg,gold,counts,self.getGG()] str,int,int,[str,str,str,str]
    
    response.result = True
    response.message = u''
    if data:
        mg=data[0]#预测祷告的结果
        gold=data[1]#需要花费的钻石数量
        counts=data[2]#距离下次加钻石的剩余次数
        gg=data[3]#数组，有可能为[] ，存放n倍奖励信息 最多4条记录
        
        response.prayDes=mg
        response.needDiamond=gold
        response.remainTimes=counts
        if len(gg)<1:
            response.otherPrayMsg.extend([])
        else:
            response.otherPrayMsg.extend(gg)
#            for item in gg:
#                info=response.otherPrayMsg.add()
#                info=item
    else:
        response.otherPrayMsg.extend([])
    
    return response.SerializeToString()