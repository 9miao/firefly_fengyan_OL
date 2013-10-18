#coding:utf8
'''
Created on 2011-5-26

@author: sean_lan
'''
from app.scense.applyInterface import mail
from app.scense.serverconfig.node import nodeHandle
from app.scense.protoFile.mail import GetMailList_pb2
from app.scense.protoFile.mail import GetMailInfo_pb2
from app.scense.protoFile.mail import SendMail_pb2
from app.scense.protoFile.mail import SaveAndDeleteMail_pb2

@nodeHandle
def getMailList_501(dynamicId, request_proto):
    '''获取邮件列表'''
    argument = GetMailList_pb2.getMailListRequest()
    argument.ParseFromString(request_proto)
    response = GetMailList_pb2.getMailListResponse()
    
    dynamicId = dynamicId
    characterId = argument.id
    mailType = argument.mailType
    pageCount = argument.pageCount
    data = mail.getMailList(dynamicId, characterId, mailType, pageCount)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    if data.get('data',None):
        data = data.get('data')
        response.data.curPage = data['curPage']
        response.data.maxPage = data['pageCnd']
        response.data.responseMailType = data['responseMailType']
        mailListInfo = data['mailListInfo']
        for mailInfo in mailListInfo:
            mail_info = response.data.mailinfo.add()
            mail_info.mailId = mailInfo['id']
            mail_info.mailState = mailInfo['isReaded']
            mail_info.mailFromType = mailInfo['type']
            mail_info.mailTitle = mailInfo['title']
            mail_info.mialSendTime = str(mailInfo['sendTime'].date())
            mail_info.outline = mailInfo['content'][:20]
    return response.SerializeToString()

@nodeHandle
def getMailInfo_505(dynamicId, request_proto):
    '''获取邮件内容'''
    argument = GetMailInfo_pb2.getMailInfoRequest()
    argument.ParseFromString(request_proto)
    response = GetMailInfo_pb2.getMailInfoResponse()
    
    dynamicId = dynamicId
    characterId = argument.id
    mailID = argument.mailId
    data = mail.getMailInfo(dynamicId, characterId, mailID)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    if data.get('data',None):
        data = data.get('data')
        response.data.mailinfo.mailIdResponse = data['id']
        response.data.mailinfo.mailFrom = data['sender']
        response.data.mailinfo.mailTitle = data['title']
        response.data.mailinfo.mailContent = data['content']
        response.data.mailinfo.mailType = data['mailType']
        response.data.mailinfo.mailDate = data['mailDate']
        
    return response.SerializeToString()

@nodeHandle
def sendMail_502(dynamicId, request_proto):
    '''发送邮件'''
    argument = SendMail_pb2.sendMailRequest()
    argument.ParseFromString(request_proto)
    response = SendMail_pb2.sendMailResponse()
    
    dynamicId = dynamicId
    characterId = argument.id
    playerName = argument.acceptName
    title = argument.mailTitle
    content = argument.mailContent
    data = mail.sendMail(dynamicId, characterId, playerName, title, content)
    response.result = data.get('result',False)
    response.message = u''#"<font color=#00FF00>%s</font>"%data.get('message','')
    return response.SerializeToString()

@nodeHandle
def SaveAndDeleteMail_503(dynamicId, request_proto):
    '''保存或删除邮件'''
    argument = SaveAndDeleteMail_pb2.saveAndDeleteMailRequest()
    argument.ParseFromString(request_proto)
    response = SaveAndDeleteMail_pb2.saveAndDeleteMailResponse()
    
    
    characterId = argument.id
    setType = argument.setType
    requestInfo = argument.requestInfo
    mailId = argument.mailId
    mailType = argument.mailType
    data = mail.SaveAndDeleteMail(dynamicId, characterId, setType, requestInfo, mailId,mailType)
    response.result = data.get('result',False)
    response.message = data.get('message','')
    if data.get('data',None):
        data = data.get('data')
        response.data.maxPage = data['maxPage']
        response.data.setTypeResponse = data['setTypeResponse']
    return response.SerializeToString()
    
