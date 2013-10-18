#coding:utf8
'''
Created on 2011-12-19
角色宠物信息
@author: lan
'''

from app.scense.core.PlayersManager import PlayersManager
from app.scense.core.character.Pet import Pet
from app.scense.netInterface.pushObjectNetInterface import pushOtherMessage
from app.scense.netInterface import pushObjectNetInterface
from app.scense.core.language.Language import Lg


def GetPetListInfo(dynamicId,characterId):
    '''获取角色的宠物列表信息'''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    petList = player.pet.getCharacterPetListInfo()
    return {'result':True,'data':petList}

def ActivationPetSkill(dynamicId,characterId,petId):
    '''激活宠物技能'''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
#    errotmap = {-5:Lg().g(159),-4:u'缺少技能水晶Lv1',-1:u'技能槽已满',0:u'数据库写入错误'}
    result = player.pet.activationPetSkill(petId)
    if result==1:
        return {'result':True}
    return {'result':True}

def LevelUpPetSkill(dynamicId,characterId,petId,skillPos):
    '''升级宠物技能'''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
#    errotmap = {-5:Lg().g(159),-2:u'缺少技能水晶',
#                -1:u'技能信息不存在', 0:u'技能达到最高等级',
#                -3:u'技能已到最高等级',-4:u'技能信息不存在'}
    result = player.pet.LevelUpPetSkill(petId,skillPos)
    if result==1:
        return {'result':True}
#    msg = errotmap.get(result)
#    pushOtherMessage(905, msg, [dynamicId])
    return {'result':True}

def TrainingPet(dynamicId,characterId,petId,trainingType):
    '''宠物培养'''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    result = player.pet.Training(petId,trainingType)
    msg = result.get('message','')
    if msg:
        pushOtherMessage(905, msg, [dynamicId])
    return result

def WeiChiAndTiHuan(dynamicId, characterId, petId,ttype):
    '''维持或者替换成长'''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    result = player.pet.Tihuan(petId,ttype)
    msg = result.get('message','')
    if msg:
        pushOtherMessage(905, msg, [dynamicId])
    return result
    
def DropPet(dynamicId,characterId,petId):
    '''宠物丢弃'''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    errotmap = {-5:Lg().g(159),0:u'数据库写入出错'}
    result = player.pet.DropPet(petId)
    if result==1:
        return {'result':True}
    return {'result':False,'message':errotmap.get(result)}

def ModifyPetName(dynamicId, characterId, petId, petName):
    '''修改宠物名称'''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    errotmap = {0:Lg().g(159),-1:u'宠物等级不足3级，不能改名'}
    result = player.pet.updateName(petId,petName)
    if result==1:
        msg = Lg().g(160)
        pushOtherMessage(905, msg, [dynamicId])
        return {'result':True}
    return {'result':False,'message':errotmap.get(result)}

def ModifySlogan(dynamicId, characterId, petId, slogan):
    '''修改宠物战斗语言
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    errotmap = {0:u'数据库写入出错'}
    result = player.pet.modifySlogan(petId,slogan)
    if result==1:
        msg = Lg().g(161)
        pushOtherMessage(905, msg, [dynamicId])
        return {'result':True}
    return {'result':False,'message':errotmap.get(result)}

def GetPetMatrixList(dynamicId,characterId):
    '''获取阵法设置'''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    data = player.matrix.getMatrixListSetting()
    return {'result':True,'data':data}

def SettingMatrix(dynamicId,characterId,matrixID,petId,operationType,fromPos,toPos):
    '''阵法设置'''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    result = player.matrix.updateMatrix(petId,operationType,fromPos,toPos)
    if not result.get('result'):
        msg = result.get('message','')
        pushOtherMessage(905, msg, [dynamicId])
    return result

def ActivationMatrix(dynamicId,characterId,matrixId):
    '''激活阵法'''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    errotmap = {-1:Lg().g(162),0:u'数据库写入出错',-2:Lg().g(163)}
    result = player.matrix.updateNowMatrix(matrixId)
    if result==1:
        msg = Lg().g(164)
        pushOtherMessage(905, msg, [dynamicId])
        return {'result':True}
    return {'result':False,'message':errotmap.get(result)}
    
def ResurPet(dynamicId, characterId, petId):
    '''复活宠物'''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    result = player.pet.ResurPet(petId)
    msg = result.get('message','')
    if msg:
        pushOtherMessage(905,msg,[dynamicId])
    return result

def ModifyPetStatus(dynamicId,characterId, petId):
    '''更新宠物的携带状态'''
    from app.scense.core.map.MapManager import MapManager
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    result = player.pet.updateShow(petId)
    msg = result.get('message','')
    if result.get('result'):
        if result.get('data'):
            if player.baseInfo.getState()==0:  #如果角色在场景中
                sceneId = player.baseInfo.getTown()
                scene = MapManager().getMapId(sceneId)
                scene.dropPet(petId)
    if msg:
        pushOtherMessage(905,msg,[dynamicId])
    return result

def GetOnePetInfo(dynamicId,characterId, petId,masterId):
    '''获取单个宠物的信息'''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    toplayer = PlayersManager().getPlayerByID(masterId)
    if not toplayer:
        return {'result':False,'message':Lg().g(159)}
    else:
        pet = toplayer.pet.getPet(petId)
    return {'result':True,'data':pet}
    
def GetBeiJiChengList(dynamicId,characterId, petId):
    '''获取可以被传承的宠物列表'''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    data = player.pet.getTransferPetList(petId)
    return {'result':True,'data':data}


def getPetShopInfo(pid,npcid,istrue):
    '''获取宠物商店信息
    @param pid: int 角色信息
    @param npcid: int NPCid
    @param istrue: int 是否是立即刷新
    '''
    player = PlayersManager().getPlayerByID(pid)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    
    if istrue:
        if player.petShop.cs>=0 and player.petShop.getTime()<=0:#免费刷新
            player.petShop.cs-=1#每天免费刷新次数-1
        else:#使用钻石刷新
            gold=player.finance.getGold()
            if gold>=10:
#                player.finance.updateGold(gold-10)
                player.finance.consGold(10,4)
                player.petShop.xy+=1
            else:
                pushOtherMessage(905, Lg().g(165), [player.dynamicId])
                return {'result':False,'message':Lg().g(165)}
        player.petShop.suiji(npcid,True)#刷新
        player.quest.specialTaskHandle(116)#特殊任务处理
    data={}
    data['result']=True
    data['message']=Lg().g(166)
    op={-1:True,1:False}
    ps= player.petShop#宠物商店类
    data['xingyunzhi']=ps.xy#幸运
    data['refreshTime']=ps.getTime() #剩余时间\
    data['isClose']=op.get(ps.isoption)#是否打开 1开启消费提示 -1 关闭消费提示
    data['shengYuCiShu']=ps.getsycs()#剩余次数
    tj=ps.getPetConfigByLv(npcid)#推荐组合   data={} data['fashi']=[]
    data['fashiPet']=tj['fashi']#[宠物模板信息]
    data['zhanshiPet']=tj['zhanshi']#[宠物模板信息]
    data['youxiaPet']=tj['youxia']#[宠物模板信息]
    petlist=ps.getShopInfo(npcid)#获取四个宠物信息 petlist[宠物模板信息,宠物模板信息,宠物模板信息,宠物模板信息]
    data['wowInfo']=[]
    if len(petlist)>0:
        ttlist=player.pet.getHasPetTemplatelist()#获取已经获取的宠物的模版列表
        for items in petlist:#item 宠物模板信息
            item=items[0]
            pi=Pet(templateId=item['id'],level=items[1])#宠物信息
            info = pi.formatPetInfo()#宠物属性
            val={}
            val['id']=item['id']
            val['wSkill']=info['skillname']
            val['wTexing']=info['texing']
            val['wLiliang']=int(info['Str'])
            val['wZhili']=int(info['Wis'])
            val['wNaili']=int(info['Vit'])
            val['wMinjie']=int(info['Dex'])
            val['wWugong']=int(info['PhyAtt'])
            val['wMogong']=int(info['MigAtt'])
            val['wGongsu']=int(info['Speed'])
            val['wBaoji']=int(info['CriRate'])
            val['wWufang']=int(info['PhyDef'])
            val['wMofang']=int(info['MigDef'])
            val['wMingzhong']=int(info['HitRate'])
            val['wShanbi']=int(info['Dodge'])
            val['wKaobao']=int(info['Block'])
            val['color']=int(info['quality'])
            if item['id'] in ttlist:
                val['wGuyongzhi']=1#是否标记已拥有  1标记  -1不标记
            else:
                val['wGuyongzhi']=-1#是否标记已拥有  1标记  -1不标记
            val['wName']=item['nickname']
            val['wGuYongJinBi']=item['coin']
            val['wGuYongXingYunZhi']=item['xy']
            val['type']=item['type']
            val['icon']=item['icon']
            val['level']=items[1]
            data['wowInfo'].append(val)
    return data
    
    

def guyongpet(pid,petid,typeid):
    '''雇用宠物
    @param pid: int 角色id
    @param petid: int 宠物模板id
    @param typeid: int #1表示金币兑换的宠物  2表示幸运值兑换
    '''
    from app.scense.utils.dbopera import dbCharacterPet
    player = PlayersManager().getPlayerByID(pid)
    if not player:
        return {'result':False,'message':Lg().g(18)}
        
    alls=dbCharacterPet.PET_TEMPLATE
    if alls.has_key(petid):
        pet=alls.get(petid)
        coin=pet['coin']
        xy=pet['xy']
        if typeid==1:#扣除金币
            pcoin=player.finance.getCoin()
            if pcoin>=coin:
                petlevel=1#宠物等级
                for i in  player.petShop.shop1:# i[宠物模板id,宠物等级]
                    if i[0]['id']==petid:
                        petlevel=i[1]
                
                flg=player.pet.addPet(petid,level=petlevel)#添加宠物并返回
                if flg==-1:
                    pushObjectNetInterface.pushOtherMessage(905,Lg().g(167), [player.getDynamicId()])
                    return {'result':True,'message':Lg().g(167)}
                elif flg==-2:
                    pushObjectNetInterface.pushOtherMessage(905,Lg().g(168), [player.getDynamicId()])
                    return {'result':True,'message':Lg().g(168)}
                
                player.finance.updateCoin(pcoin-coin)
                player.quest.specialTaskHandle(115)#特殊任务处理
                player.schedule.noticeSchedule(16,goal = 1)
                return {'result':True,'message':Lg().g(166)}
            else:
                return {'result':False,'message':Lg().g(88)}
        else:#扣除幸运值
            pxy=player.petShop.xy
            if pxy<xy:
                pushObjectNetInterface.pushOtherMessage(905,Lg().g(169), [player.getDynamicId()])
                return {'result':True,'message':Lg().g(169)}
            if pxy>=xy:
                flg=player.pet.addPet(petid)
                if flg==-1:
                    pushObjectNetInterface.pushOtherMessage(905,Lg().g(167), [player.getDynamicId()])
                    return {'result':False,'message':Lg().g(167)}
                elif flg==-2:
                        pushObjectNetInterface.pushOtherMessage(905,Lg().g(168), [player.getDynamicId()])
                        return {'result':True,'message':Lg().g(168)}
                player.petShop.xy=pxy-xy
                player.quest.specialTaskHandle(115)#特殊任务处理
                player.schedule.noticeSchedule(16,goal = 1)
                return {'result':True,'message':Lg().g(166)}
            else:
                return {'result':False,'message':Lg().g(169)}
    else:
        return {'result':False,'message':Lg().g(170)}
            
def getXYlist(pid,lv,page):
    '''获取幸运值兑换的宠物列表
    return  {'zong':zong,'date':date}
    '''
    player = PlayersManager().getPlayerByID(pid)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    data=player.petShop.getXyShopBylv(lv,page)
    ttlist=player.pet.getHasPetTemplatelist()#获取已经获取的宠物的模版列表
    li=[]

    for item in data['date']:
#        le=random.randint(1,5)
        pi=Pet(templateId=item['id'],level=1)#宠物信息
        info = pi.formatPetInfo()#宠物属性
        val={}
        val['id']=item['id']
        val['wSkill']=info['skillname']
        val['wTexing']=info['texing']
        val['wLiliang']=info['Str']
        val['wZhili']=info['Wis']
        val['wNaili']=info['Vit']
        val['wMinjie']=info['Dex']
        val['wWugong']=info['PhyAtt']
        val['wMogong']=info['MigAtt']
        val['wGongsu']=info['Speed']
        val['wBaoji']=info['CriRate']
        val['wWufang']=info['PhyDef']
        val['wMofang']=info['MigDef']
        val['wMingzhong']=info['HitRate']
        val['wShanbi']=info['Dodge']
        val['wKaobao']=info['Block']
        val['color']=int(info['quality'])
        if item['id'] in ttlist:
            val['wGuyongzhi']=1#是否标记已拥有  1标记  -1不标记
        else:
            val['wGuyongzhi']=-1#是否标记已拥有  1标记  -1不标记
        val['wName']=item['nickname']
        val['wGuYongXingYunZhi']=item['xy']
        val['type']=item['type']
        val['icon']=item['icon']
        val['level']=1
        li.append(val)
    data['data']=li
    return data

def getlijishuaxin(pid,lv):
    '''立即刷新'''
    player = PlayersManager().getPlayerByID(pid)
    if player.petShop.cs>=0 and player.petShop.getTime()<=0:#免费刷新
        return 0
    return 10
    
def xiaofeitishi(pid,close):
    '''消费提示'''
    player = PlayersManager().getPlayerByID(pid)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    player.petShop.isoption=close
    return {'result':True,'message':Lg().g(166)}

def PetChuanCheng(dynamicId,characterId, petFrom,petTo):
    '''宠物传承
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    data = player.pet.TransferExp(petFrom,petTo)
    msg = data.get('message',0)
    if msg:
        pushOtherMessage(905, msg, [dynamicId])
    return data

def GetTuJianPetList(dynamicId,characterId, ttype,page):
    '''获取图鉴信息
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    data = player.pet.GetTuJianPetList(ttype,page)
    return {'result':True,'data':data}

def GetOnePetTuJianInfo(dynamicId,characterId, petId):
    '''获取图鉴中某个宠物的收集信息
    '''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    data = player.pet.GetOnePetTuJianInfo(petId)
    return {'result':True,'data':data}
    
def ZhaoHuan(dynamicId, characterId, petId):
    '''宠物召唤'''
    player = PlayersManager().getPlayerByID(characterId)
    if not player:
        return {'result':False,'message':Lg().g(18)}
    result = player.pet.ZhaoHuan(petId)
    msg = result.get('message',0)
    if msg:
        pushOtherMessage(905, msg, [dynamicId])
    return result

