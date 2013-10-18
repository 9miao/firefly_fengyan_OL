#coding:utf8
'''
Created on 2011-5-26

@author: sean_lan
'''
from app.scense.applyInterface import scene
from app.scense.serverconfig.node import nodeHandle
from app.scense.protoFile.scene import moveInScene_pb2

@nodeHandle
def moveInScene_603(dynamicId, request_proto):
    '''在场景中移动'''
    argument = moveInScene_pb2.moveInSceneRequest()
    argument.ParseFromString(request_proto)
    
    characterId = argument.id
    sceneId = argument.sceneId
    x = argument.x
    y = argument.y
    
    scene.moveInScene(dynamicId, characterId,sceneId, x, y)
    