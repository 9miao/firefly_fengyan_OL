#coding:utf8
'''
Created on 2012-5-17
官爵
@author: jt
'''
from app.scense.applyInterface import nobility_app
from app.scense.serverconfig.node import nodeHandle
from app.scense.protoFile.nobility import guanjue3300_pb2
from app.scense.protoFile.nobility import getShengJue_pb2
from app.scense.protoFile.nobility import GetWeiWangInfo3303_pb2
from app.scense.protoFile.nobility import GetShangJiaoInfo3304_pb2
from app.scense.protoFile.nobility import GetZuan3306_pb2
from app.scense.core.language.Language import Lg

@nodeHandle
def getNobility_3300(dynamicId,request_proto):
    '''获取爵位面板所有信息'''
    arguments = guanjue3300_pb2.GetGuanJueInfoRequest()
    arguments.ParseFromString(request_proto)
    response = guanjue3300_pb2.GetGuanJueInfoResponse()
    
    pid=arguments.id#角色id
    page=arguments.curpage#当前页
    
    data=nobility_app.getAllInfo(pid, page)
    if data:
        response.result=True
        response.message=u''
        response.data.currentJuewei=data.get('currentJuewei')
        response.data.weiwang=data.get('weiwang')
        response.data.currentJinbi=data.get('currentJinbi')
        response.data.currentDouqi=data.get('currentDouqi')
        response.data.adddq.extend(data.get('adddq'))
        response.data.nextJuewei=data.get('nextJuewei')
        response.data.nextWeiwang=data.get('nextWeiwang')
        response.data.nextJinbi=data.get('nextJinbi')
        response.data.nextDouqi=data.get('nextDouqi')
        response.data.addxj.extend(data.get('addxj'))
        response.data.ftime.extend(data.get('ftime'))
        response.data.fcontext.extend(data.get('fcontext'))
        response.data.curpage=int(data.get('curpage'))
        response.data.totalpage=int(data.get('totalpage'))
        response.data.isjw=data.get('isjw')
        response.data.hasGetSalary=data.get('hasGetSalary')
        response.data.level=data.get('dengji')
        
    else:
        response.result=False
        response.message=Lg().g(614)
        response.data.adddq.extend(data.get('adddq'))
        response.data.addxj.extend(data.get('addxj'))
        response.data.ftime.extend(data.get('ftime'))
        response.data.fcontext.extend(data.get('fcontext'))
        response.data.curpage=page
        response.data.totalpage=0
    
    return response.SerializeToString()

@nodeHandle
def getNobility_3301(dynamicId,request_proto):
    '''领取俸禄'''
    arguments = getShengJue_pb2.GetShengJueRequest()
    arguments.ParseFromString(request_proto)
    response = getShengJue_pb2.GetShengJueResponse()
    
    pid=arguments.id#角色id
    result=nobility_app.drawSalary(pid)
    
    response.result=result
    response.message=u''
    return response.SerializeToString()

@nodeHandle
def getNobility_3302(dynamicId,request_proto):
    '''升级爵位'''
    arguments = getShengJue_pb2.GetShengJueRequest()
    arguments.ParseFromString(request_proto)
    response = getShengJue_pb2.GetShengJueResponse()
    
    pid=arguments.id#角色id
    result=nobility_app.drawPromote(pid)
    
    response.result=result
    response.message=u''
    return response.SerializeToString()

@nodeHandle
def getNobility_3303(dynamicId,request_proto):
    '''获取威望任务'''
    arguments = GetWeiWangInfo3303_pb2.GetWeiWangInfoRequest()
    arguments.ParseFromString(request_proto)
    response = GetWeiWangInfo3303_pb2.GetWeiWangInfoResponse()
    
    pid=arguments.id#角色id
    
    list=nobility_app.getItemList(pid)
    if len(list)>0:
        response.result=True
        response.message=u''
        for item in list:
            #item [0物品id,1物品名称,2物品数量，3获得贡献值数量，4是否可以上交，5唯一标识(字段你名称)]
            wp=response.data.wp.add()
            wp.id=item[0]#物品模板id
            
            try:
                wp.name=item[1]#物品名称
            except:
                wp.name=item[1].decode('utf8')#物品名称
            
            wp.count=item[2]#物品数量
            wp.weiwang=item[3]#奖励的威望值
            wp.adddq=item[4]#是否可以上交
            wp.wy=item[5]#唯一标识
            wp.addzuan=item[6]#魔钻是否足够
    else:
        response.result=False
        response.message=Lg().g(614)
        response.data.wp.extend([])
    return response.SerializeToString()
    
@nodeHandle
def getNobility_3304(dynamicId,request_proto):
    '''上交物品换取威望'''
    arguments = GetShangJiaoInfo3304_pb2.GetShangJiaoInfoRequest()
    arguments.ParseFromString(request_proto)
    response = GetShangJiaoInfo3304_pb2.GetShangJiaoInfoResponse()
    
    pid=arguments.id#角色id
    wy=arguments.wy#唯一标识
    
    rs=nobility_app.handin(pid, wy)
    if rs.get("result"):
        response.result=True
        response.message=u''
    else:
        response.result=False
        response.message=Lg().g(615)
    return response.SerializeToString()
    
@nodeHandle
def getNobility_3305(dynamicId,request_proto):
    '''上交钻换取威望'''
    arguments = GetShangJiaoInfo3304_pb2.GetShangJiaoInfoRequest()
    arguments.ParseFromString(request_proto)
    response = GetShangJiaoInfo3304_pb2.GetShangJiaoInfoResponse()
    
    pid=arguments.id#角色id
    wy=arguments.wy#唯一标识
    
    rs=nobility_app.drawDiamond(pid, wy)
    if rs.get("result"):
        response.result=True
        response.message=u''
    else:
        response.result=False
        response.message=Lg().g(615)
    return response.SerializeToString()

@nodeHandle
def getNobility_3306(dynamicId,request_proto):
    '''返回客户端这次点击贡献应该花费多少钻'''
    arguments = GetZuan3306_pb2.GetZuanInfoRequest()
    arguments.ParseFromString(request_proto)
    response = GetZuan3306_pb2.GetZuanInfoResponse()
    pid=arguments.id#角色id
    rs=nobility_app.getzuan(pid)
    if rs>0:
        response.result=True
        response.message=u''
        response.count=rs
    else:
        response.result=False
        response.message=Lg().g(614)
    return response.SerializeToString()
