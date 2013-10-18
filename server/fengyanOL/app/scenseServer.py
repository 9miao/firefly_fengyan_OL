#coding:utf8
'''
Created on 2013-9-5

@author: jt
'''
from app.scense import initapp
from firefly.server.globalobject import GlobalObject
from firefly.utils.services import CommandService
GlobalObject().remote["gate"]._reference._service=CommandService("scensetogate")
initapp.loadModule()