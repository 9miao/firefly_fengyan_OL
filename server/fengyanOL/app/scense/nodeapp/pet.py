#coding:utf8
'''
Created on 2011-12-19
角色宠物信息
@author: lan
'''
from app.scense.applyInterface import pet
from app.scense.serverconfig.node import nodeHandle

from app.scense.protoFile.pet import GetPetListInfo2300_pb2
from app.scense.protoFile.pet import ActivationPetSkill2301_pb2
from app.scense.protoFile.pet import LevelUpPetSkill2302_pb2
from app.scense.protoFile.pet import ModifyPetName2303_pb2
from app.scense.protoFile.pet import TrainingPet2304_pb2
from app.scense.protoFile.pet import DropPet2305_pb2
from app.scense.protoFile.pet import GetPetMatrixList2306_pb2
from app.scense.protoFile.pet import SettingMatrix2307_pb2
from app.scense.protoFile.pet import ActivationMatrix2308_pb2
from app.scense.protoFile.pet import ModifySlogan2309_pb2
from app.scense.protoFile.pet import ResurPet2701_pb2
from app.scense.protoFile.pet import ModifyPetStatus2310_pb2
from app.scense.protoFile.pet import GetOnePetInfo2311_pb2
from app.scense.protoFile.pet import WeiChiAndTiHuan2312_pb2
from app.scense.protoFile.pet import PetChuanCheng2314_pb2
from app.scense.protoFile.pet import GetTuJianPetList2315_pb2
from app.scense.protoFile.pet import GetOnePetTuJianInfo2316_pb2
from app.scense.protoFile.pet import ZhaoHuan2317_pb2
from app.scense.protoFile.pet import Pet3500_pb2
from app.scense.protoFile.pet import Pet3501_pb2
from app.scense.protoFile.pet import Pet3503_pb2
from app.scense.protoFile.pet import Pet3502_pb2
from app.scense.protoFile.pet import Pet3504_pb2
from app.scense.core.language.Language import Lg

@nodeHandle
def GetPetListInfo_2300(dynamicId,request_proto):
    '''获取宠物列表信息'''
    argument = GetPetListInfo2300_pb2.GetPetListInfoRequest()
    argument.ParseFromString(request_proto)
    response = GetPetListInfo2300_pb2.GetPetListInfoResponse()
    characterId = argument.id
    result = pet.GetPetListInfo(dynamicId, characterId)
    response.result = result.get('result',False)
    response.message = result.get('message','')
    if result.get('data',None):
        petListInfo = result.get('data')
        response.curPetNum = petListInfo.get('curPetNum',0)
        response.maxPetNum = petListInfo.get('maxPetNum',0)
        petInfolist = response.petInfo
        for _pet in petListInfo.get('petInfo',[]):
            petInfo = petInfolist.add()
            petInfo.petId = _pet['petId']
            petInfo.resPetId = _pet['resPetId']
            petInfo.petName = _pet['petName']
            petInfo.petLevel = _pet['petLevel']
            petInfo.icon = _pet['icon']
            petInfo.type = _pet['type']
    return response.SerializeToString()

@nodeHandle
def ActivationPetSkill_2301(dynamicId,request_proto):
    '''激活宠物技能'''
    argument = ActivationPetSkill2301_pb2.ActivationSkillPosRequest()
    argument.ParseFromString(request_proto)
    response = ActivationPetSkill2301_pb2.ActivationSkillPosResponse()
    characterId = argument.id
    petId = argument.petId
    result = pet.ActivationPetSkill(dynamicId, characterId, petId)
    response.result = result.get('result',False)
    response.message = result.get('message','')
    return response.SerializeToString()

@nodeHandle
def LevelUpPetSkill_2302(dynamicId,request_proto):
    '''升级宠物技能'''
    argument = LevelUpPetSkill2302_pb2.LevelUpPetSkillRequest()
    argument.ParseFromString(request_proto)
    response = LevelUpPetSkill2302_pb2.LevelUpPetSkillResponse()
    characterId = argument.id
    petId = argument.petId
    skillPos = argument.skillPos
    result = pet.LevelUpPetSkill(dynamicId, characterId, petId, skillPos)
    response.result = result.get('result',False)
    response.message = result.get('message','')
    return response.SerializeToString()

@nodeHandle
def ModifyPetName_2303(dynamicId,request_proto):
    '''修改宠物名称'''
    argument = ModifyPetName2303_pb2.ModifyPetNameRequest()
    argument.ParseFromString(request_proto)
    response = ModifyPetName2303_pb2.ModifyPetNameResponse()
    characterId = argument.id
    petId = argument.petId
    petName = argument.petName
    result = pet.ModifyPetName(dynamicId, characterId, petId, petName)
    response.result = result.get('result',False)
    response.message = result.get('message','')
    return response.SerializeToString()

@nodeHandle
def TrainingPet_2304(dynamicId,request_proto):
    '''宠物培养'''
    argument = TrainingPet2304_pb2.TrainingPetRequest()
    argument.ParseFromString(request_proto)
    response = TrainingPet2304_pb2.TrainingPetResponse()
    dynamicId = dynamicId
    characterId = argument.id
    petId = argument.petId
    trainingType = argument.trainingType
    result = pet.TrainingPet(dynamicId, characterId, petId, trainingType)
    response.result = result.get('result',False)
    response.message = result.get('message','')
    if result.get('data',None):
        trainData = result.get('data')
        trainInfo = response.trainInfo
        for keyname,values in trainData.items():
            setattr(trainInfo,keyname,values)
    return response.SerializeToString()

@nodeHandle
def DropPet_2305(dynamicId,request_proto):
    '''丢弃宠物'''
    argument = DropPet2305_pb2.DropPetRequest()
    argument.ParseFromString(request_proto)
    response = DropPet2305_pb2.DropPetResponse()
    characterId = argument.id
    petId = argument.petId
    result = pet.DropPet(dynamicId, characterId, petId)
    response.result = result.get('result',False)
    response.message = result.get('message','')
    return response.SerializeToString()

@nodeHandle
def GetPetMatrixList_2306(dynamicId,request_proto):
    '''获取阵法信息'''
    argument = GetPetMatrixList2306_pb2.GetPetMatrixListRequest()
    argument.ParseFromString(request_proto)
    response = GetPetMatrixList2306_pb2.GetPetMatrixListResponse()
    characterId = argument.id
    result = pet.GetPetMatrixList(dynamicId, characterId)
    response.result = result.get('result',False)
    response.message = result.get('message','')
    if result.get('data',None):
        _matrix = result.get('data')
        matrixInfo = response.matrixInfo
        matrixInfo.jwDes = _matrix.get('jwDes')
        matrixInfo.curNum = _matrix.get('curNum')
        matrixInfo.maxNum = _matrix.get('maxNum')
        for _eye in _matrix.get('matrixTitleInfo'):
            eyeInfo = matrixInfo.matrixTitleInfo.add()
            eyeInfo.titlePos = _eye.get('titlePos')
            eyeInfo.hasPet = _eye.get('hasPet')
            eyeInfo.petId = _eye.get('petId',-1)
            eyeInfo.type = _eye.get('type',0)
            eyeInfo.icon = _eye.get('icon',0)
    return response.SerializeToString()
    
@nodeHandle
def SettingMatrix_2307(dynamicId,request_proto):
    '''阵法设置'''
    argument = SettingMatrix2307_pb2.SettingMatrixRequest()
    argument.ParseFromString(request_proto)
    response = SettingMatrix2307_pb2.SettingMatrixResponse()
    characterId = argument.id
    matrixId = argument.matrixId
    petId = argument.petId
    operationType = argument.operationType
    fromPos = argument.fromPos
    toPos = argument.toPos
    result = pet.SettingMatrix(dynamicId, characterId, matrixId,\
                                petId, operationType, fromPos, toPos)
    response.result = result.get('result',False)
    response.message = result.get('message','')
    response.petId = petId
    response.operationType = operationType
    response.fromPos = fromPos
    response.toPos = toPos
    response.matrixId = matrixId
    return response.SerializeToString()
    

@nodeHandle
def ActivationMatrix_2308(dynamicId,request_proto):
    '''激活阵法设置'''
    argument = ActivationMatrix2308_pb2.ActivationMatrixRequest()
    argument.ParseFromString(request_proto)
    response = ActivationMatrix2308_pb2.ActivationMatrixResponse()
    characterId = argument.id
    matrixId = argument.matrixId
    result = pet.ActivationMatrix(dynamicId, characterId, matrixId)
    response.result = result.get('result',False)
    response.message = result.get('message','')
    return response.SerializeToString()
@nodeHandle
def ModifySlogan_2309(dynamicId,request_proto):
    '''修改宠物战斗宣言'''
    argument = ModifySlogan2309_pb2.ModifySloganRequest()
    argument.ParseFromString(request_proto)
    response = ModifySlogan2309_pb2.ModifySloganResponse()
    characterId = argument.id
    petId = argument.petId
    sloganStr = argument.sloganStr
    result = pet.ModifySlogan(dynamicId, characterId, petId, sloganStr)
    response.result = result.get('result',False)
    response.message = result.get('message','')
    return response.SerializeToString()

@nodeHandle
def ResurPet_2701(dynamicId,request_proto):
    '''复活宠物'''
    argument = ResurPet2701_pb2.ResurPetRequest()
    argument.ParseFromString(request_proto)
    response = ResurPet2701_pb2.ResurPetResponse()
    characterId = argument.id
    petId = argument.petId
    result = pet.ResurPet(dynamicId, characterId, petId)
    response.result = result.get('result',False)
    msg = result.get('message','')
    response.message = msg
    if result.get('data',None):
        data = result.get('data')
        response.failType = data.get('failType')
    return response.SerializeToString()

@nodeHandle
def ModifyPetStatus_2310(dynamicId,request_proto):
    '''更新宠物的携带状态'''
    argument = ModifyPetStatus2310_pb2.ModifyPetStatusRequest()
    argument.ParseFromString(request_proto)
    response = ModifyPetStatus2310_pb2.ModifyPetStatusResponse()
    characterId = argument.id
    petId = argument.petId
    result = pet.ModifyPetStatus(dynamicId, characterId, petId)
    response.result = result.get('result',False)
    msg = result.get('message','')
    response.message = msg
    return response.SerializeToString()
    
@nodeHandle
def GetOnePetInfo_2311(dynamicId,request_proto):
    '''获取单个宠物的信息'''
    argument = GetOnePetInfo2311_pb2.GetOnePetInfoRequest()
    argument.ParseFromString(request_proto)
    response = GetOnePetInfo2311_pb2.GetOnePetInfoResponse()
    characterId = argument.id
    petId = argument.petId
    masterId = argument.masterId
    result = pet.GetOnePetInfo(dynamicId, characterId, petId,masterId)
    response.result = result.get('result',False)
    response.message = result.get('message','')
    if result.get('data',None):
        petInfo = result.get('data')
        growth = petInfo.attribute.getMaxGrowth()
        petInfo.SerializationPetInfo(response.info)
        response.extendsExp = petInfo.level.getAllExp()
        response.ziZhiInfo.cur_zi_li = petInfo.attribute.StrGrowth
        response.ziZhiInfo.max_zi_li = growth.get('StrGrowth',1000)
        response.ziZhiInfo.cur_zi_zhi = petInfo.attribute.WisGrowth
        response.ziZhiInfo.max_zi_zhi = growth.get('WisGrowth',1000)
        response.ziZhiInfo.cur_zi_nai = petInfo.attribute.VitGrowth
        response.ziZhiInfo.max_zi_nai = growth.get('VitGrowth',1000)
        response.ziZhiInfo.cur_zi_min = petInfo.attribute.DexGrowth
        response.ziZhiInfo.max_zi_min = growth.get('DexGrowth',1000)
    return response.SerializeToString()

@nodeHandle
def WeiChiAndTiHuan_2312(dynamicId,request_proto):
    '''维持或者替换属性
    '''
    argument = WeiChiAndTiHuan2312_pb2.WeiChiAndTiHuanRequest()
    argument.ParseFromString(request_proto)
    response = WeiChiAndTiHuan2312_pb2.WeiChiAndTiHuanResponse()
    characterId = argument.id
    petId = argument.petId
    ttype = argument.type
    result = pet.WeiChiAndTiHuan(dynamicId, characterId, petId,ttype)
    response.result = result.get('result',False)
    response.message = result.get('message','')
    return response.SerializeToString()

@nodeHandle
def GetBeiJiChengList_2313(dynamicId,request_proto):
    '''获取可以被传承的宠物列表
    '''
    from app.scense.protoFile.pet import GetBeiJiChengList2313_pb2
    argument = GetBeiJiChengList2313_pb2.GetBeiJiChengListRequest()
    argument.ParseFromString(request_proto)
    response = GetBeiJiChengList2313_pb2.GetBeiJiChengListResponse()
    characterId = argument.id
    petId = argument.petId
    result = pet.GetBeiJiChengList(dynamicId, characterId, petId)
    response.result = result.get('result',False)
    response.message = result.get('message','')
    if result.get('data',None):
        BeiJiChengList = result.get('data')
        petInfoList = response.petInfoList
        for _petInfo in BeiJiChengList:
            petInfo = petInfoList.add()
            petbearer = petInfo.info
            _petInfo['pet'].SerializationPetInfo(petbearer)
            petInfo.reqCoin = _petInfo['reqCoin']
    return response.SerializeToString()
    
    
@nodeHandle
def PetChuanCheng_2314(dynamicId,request_proto):
    '''宠物传承
    '''
    argument = PetChuanCheng2314_pb2.PetChuanChengRequest()
    argument.ParseFromString(request_proto)
    response = PetChuanCheng2314_pb2.PetChuanChengResponse()
    characterId = argument.id
    petFrom = argument.petId
    petTo = argument.bjcPetId
    result = pet.PetChuanCheng(dynamicId, characterId, petFrom, petTo)
    response.result = result.get('result',False)
    response.message = result.get('message','')
    return response.SerializeToString()
    
@nodeHandle
def GetTuJianPetList_2315(dynamicId,request_proto):
    '''获取宠物图鉴信息
    '''
    argument = GetTuJianPetList2315_pb2.GetTuJianPetListRequest()
    argument.ParseFromString(request_proto)
    response = GetTuJianPetList2315_pb2.GetTuJianPetListResponse()
    characterId = argument.id
    ttype = argument.type
    page = argument.page
    result = pet.GetTuJianPetList(dynamicId, characterId, ttype, page)
    response.result = result.get('result',False)
    response.message = result.get('message','')
    if result.get('data',None):
        TujianInfo = result.get('data')
        response.slInfo.sjPro = TujianInfo.get('sjPro')
        response.slInfo.curPage = TujianInfo.get('curPage')
        response.slInfo.maxPage = TujianInfo.get('maxPage')
        SjListPet = TujianInfo.get('sjListPet')
        sjListPet = response.slInfo.sjListPet
        for _petinfo in SjListPet:
            petInfo = sjListPet.add()
            petInfo.petName = _petinfo.get('petName')
            petInfo.petLevel = _petinfo.get('petLevel')
            petInfo.petId = _petinfo.get('petId')
            petInfo.viewFlag = _petinfo.get('viewFlag')
            petInfo.quality = _petinfo.get('quality')
    return response.SerializeToString()


@nodeHandle
def GetOnePetTuJianInfo_2316(dynamicId,request_proto):
    '''获取宠物图鉴中宠物的收集信息
    '''
    argument = GetOnePetTuJianInfo2316_pb2.GetOnePetTuJianInfoRequest()
    argument.ParseFromString(request_proto)
    response = GetOnePetTuJianInfo2316_pb2.GetOnePetTuJianInfoResponse()
    characterId = argument.id
    petId = argument.petId
    result = pet.GetOnePetTuJianInfo(dynamicId, characterId, petId)
    response.result = result.get('result',False)
    response.message = result.get('message','')
    if result.get('data',None):
        petTujianInfo = result.get('data')
        petTujianInfo['pet'].SerializationPetInfo(response.info)
        response.curHun = petTujianInfo.get('curHun')
        response.maxHun = petTujianInfo.get('maxHun')
        response.reqCoin = petTujianInfo.get('reqCoin')
    return response.SerializeToString()

@nodeHandle
def ZhaoHuan_2317(dynamicId,request_proto):
    '''召唤宠物'''
    argument = ZhaoHuan2317_pb2.ZhaoHuanRequest()
    argument.ParseFromString(request_proto)
    response = ZhaoHuan2317_pb2.ZhaoHuanResponse()
    characterId = argument.id
    petId = argument.petId
    result = pet.ZhaoHuan(dynamicId, characterId, petId)
    response.result = result.get('result',False)
    response.message = result.get('message','')
    return response.SerializeToString()

@nodeHandle
def Pet_3500(dynamicId,request_proto):
    '''获取宠物商店所有信息'''
    argument = Pet3500_pb2.GetTavernListInfoRequest()
    argument.ParseFromString(request_proto)
    r = Pet3500_pb2.GetTavernTaskInfoResponse()
    pid = argument.id#角色id
    npcid = argument.npcId#npcid
    istrue=argument.istrue#是否是立即刷新
    

    data = pet.getPetShopInfo(pid, npcid,istrue)
    r.result=True
    r.message=Lg().g(166)
    if not data['result']:#如果返回错误
        r.result=False
        r.message=data['message']
        r.data.wowInfo.extend([])
        r.data.fashiPet.extend([])
        r.data.zhanshiPet.extend([])
        r.data.youxiaPet.extend([])
        r.data.xingyunzhi=0
        r.data.refreshTime=0
        r.data.isClose=False
        r.data.shengYuCiShu=0
        
    else:
        for item in data['wowInfo']:#item 宠物模板id
            wi=r.data.wowInfo.add()
            wi.id=item['id']
            wi.wSkill=item['wSkill']
            wi.wTexing=item['wTexing']
            wi.wLiliang=int(item['wLiliang'])
            wi.wZhili=int(item['wZhili'])
            wi.wNaili=int(item['wNaili'])
            wi.wMinjie=int(item['wMinjie'])
            wi.wWugong=int(item['wWugong'])
            wi.wMogong=int(item['wMogong'])
            wi.wGongsu=int(item['wGongsu'])
            wi.wBaoji=int(item['wBaoji'])
            wi.wWufang=int(item['wWufang'])
            wi.wMofang=int(item['wMofang'])
            wi.wMingzhong=int(item['wMingzhong'])
            wi.wShanbi=int(item['wShanbi'])
            wi.wKaobao=int(item['wKaobao'])
            wi.wGuyongzhi=int(item['wGuyongzhi'])
            wi.wName=item['wName']
            wi.wGuYongJinBi=item['wGuYongJinBi']
            wi.wGuYongXingYunZhi=item['wGuYongXingYunZhi']
            wi.color=item['color']
            wi.type=item['type']
            wi.icon=item['icon']
            wi.level=item['level']
        for item in data['fashiPet']:
            f=r.data.fashiPet.add()
            f.type=item['type']
            f.icon=item['icon']
            f.Skill=item['skillname']
            f.Texing=item['texing']
            f.Liliang=item['Str']
            f.Zhili=item['Wis']
            f.Naili=item['Vit']
            f.Minjie=item['Dex']
            f.Dengji=item['level']
            f.Hp=item['hp']
            f.Name=item['name']
        for item in data['zhanshiPet']:
            f=r.data.zhanshiPet.add()
            f.type=item['type']
            f.icon=item['icon']
            f.Skill=item['skillname']
            f.Texing=item['texing']
            f.Liliang=item['Str']
            f.Zhili=item['Wis']
            f.Naili=item['Vit']
            f.Minjie=item['Dex']
            f.Dengji=item['level']
            f.Hp=item['hp']
            f.Name=item['name']
        for item in data['youxiaPet']:
            f=r.data.youxiaPet.add()
            f.type=item['type']
            f.icon=item['icon']
            f.Skill=item['skillname']
            f.Texing=item['texing']
            f.Liliang=item['Str']
            f.Zhili=item['Wis']
            f.Naili=item['Vit']
            f.Minjie=item['Dex']
            f.Dengji=item['level']
            f.Hp=item['hp']
            f.Name=item['name']
        r.data.xingyunzhi=data['xingyunzhi']
        r.data.refreshTime=data['refreshTime']
        r.data.isClose=data['isClose']
        r.data.shengYuCiShu=int(data['shengYuCiShu'])
    return r.SerializeToString()



@nodeHandle
def Pet_3501(dynamicId,request_proto):
    '''雇佣宠物'''
    argument = Pet3501_pb2.Get3501Request()
    argument.ParseFromString(request_proto)
    r = Pet3501_pb2.Get3501Response()
    pid = argument.id#角色id
    petid = argument.petid#宠物模板id
    typeid=argument.typeid#1表示金币兑换的宠物  2表示幸运值兑换
    data = pet.guyongpet(pid, petid,typeid)
    r.result=data['result']
    r.message=data['message']
    return r.SerializeToString()

@nodeHandle
def Pet_3503(dynamicId,request_proto):
    '''获取幸运宠物'''
    argument = Pet3503_pb2.GetTavernListInfoRequest()
    argument.ParseFromString(request_proto)
    r = Pet3503_pb2.GetTavernTaskInfoResponse()
    pid = argument.id#角色id
    npcid = argument.npcId#NPCid
    page=argument.page#当前页数
    data = pet.getXYlist(pid, npcid, page)
    r.result=True
    r.message=Lg().g(166)
    r.data.zong=int(data['zong'])
    r.data.page=page
    if len(data['data'])<1:
        r.data.wowInfo.extend([])
    else:
        for item in data['data']:#item 宠物模板信息
            wi=r.data.xingYunwowInfo.add()
            wi.id=item['id']
            wi.wSkill=item['wSkill']
            wi.wTexing=item['wTexing']
            wi.wLiliang=int(item['wLiliang'])
            wi.wZhili=int(item['wZhili'])
            wi.wNaili=int(item['wNaili'])
            wi.wMinjie=int(item['wMinjie'])
            wi.wWugong=int(item['wWugong'])
            wi.wMogong=int(item['wMogong'])
            wi.wGongsu=int(item['wGongsu'])
            wi.wBaoji=int(item['wBaoji'])
            wi.wWufang=int(item['wWufang'])
            wi.wMofang=int(item['wMofang'])
            wi.wMingzhong=int(item['wMingzhong'])
            wi.wShanbi=int(item['wShanbi'])
            wi.wKaobao=int(item['wKaobao'])
            wi.wGuyongzhi=int(item['wGuyongzhi'])
            wi.wName=item['wName']
            wi.wGuYongXingYunZhi=item['wGuYongXingYunZhi']
            wi.color=item['color']
            wi.type=item['type']
            wi.icon=item['icon']
            wi.level=item['level']
    return r.SerializeToString()
    
@nodeHandle
def Pet_3502(dynamicId,request_proto):
    '''返回刷新需要的货币数量'''
    argument = Pet3502_pb2.Get3502Request()
    argument.ParseFromString(request_proto)
    r = Pet3502_pb2.Get3502Response()
    pid = argument.id#角色id
    npcid = argument.npcId#NPCid
    count = pet.getlijishuaxin(pid, npcid)
    r.result=True
    r.message=u''
    r.gold=count
    return r.SerializeToString()

@nodeHandle
def Pet_3504(dynamicId,request_proto):
    '''消费提示设置'''
    argument = Pet3504_pb2.Get3504Request()
    argument.ParseFromString(request_proto)
    r = Pet3504_pb2.Get3504Response()
    pid = argument.id#角色id
    close=argument.close #1没有打对勾    -1选中，已经打上对勾      (1开启消费提示 -1 关闭消费提示)
    data = pet.xiaofeitishi(pid,close)
    r.result=data['result']
    r.message=data['message']
    return r.SerializeToString()


