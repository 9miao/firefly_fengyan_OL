#coding:utf8
'''
Created on 2012-4-20
工具类方法 处理各种公式算法
@author: jt
'''
import math

def ceiling(a,b):
    '''Excel 中的算法'''
    a=float(a)
    b=float(b)
    
    da=0
    if a<=b:
        da= b
    else:
        da=math.ceil(a/b)*b
    print "ceiling(%s,%s)=%s  ,  %s"%(a,b,da,int(da))
    print ""
    
    return da

def addDict(a,b):
    '''两个字典类型相加，有相同key的value值相加，不同的key合并,只支持value值为数值类型
    '''
    allkeys = set(a.keys()).union(b.keys())
    info = {}
    for key in allkeys:
        info[key] = a.get(key,0)+ b.get(key,0)
    return info
    
    
    
    
