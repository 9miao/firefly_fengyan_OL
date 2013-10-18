#coding:utf8
'''
Created on 2011-4-14

@author: sean_lan
'''
from app.scense.component.Component import Component

class SceneAttributeComponent(Component):
    '''场景属性组件'''
    def __init__(self,owner):
        Component.__init__(self,owner)
        