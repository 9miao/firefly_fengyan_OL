#coding:utf8
'''
Created on 2011-12-20
副本殖民挑战对应表
@author: SIOP_09
'''
allColonizeChallenge={}#殖民挑战对应表
allMosterNameByinstance={}#殖民副本组id获取怪物名称
from twisted.python import log

def getMosterNameByinstanceid(did):
    '''根据殖民副本组id获取怪物名称'''
    name=u"地狱小蝙蝠"
    try:
        info=allMosterNameByinstance[did]
        name=info[1]
    except:
        log.err(u"tb_instance_colonize_challenge表  不存在  副本组id%s"%did)
    return name

def getColonizeChallengeByMosterid(did):
    '''根据副本id获取怪物id'''
    info=allColonizeChallenge[did]
    did=info[0]
    return did