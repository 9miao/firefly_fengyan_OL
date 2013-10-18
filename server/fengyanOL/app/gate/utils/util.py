#coding:utf8
'''
Created on 2009-12-15

@author: wudepeng
'''
import time
from twisted.python import log
import datetime

dbpool = object

def EachQueryProps(props):
    '''遍历字段列表生成sql语句'''
    sqlstr = ""
    if props == '*':
        return '*'
    elif type(props) == type([0]):
        for prop in props:
            sqlstr = sqlstr + prop +','
        sqlstr = sqlstr[:-1]
        return sqlstr
    else:
        log.msg('props to query must be list')
        return

def forEachQueryProps(sqlstr, props):
    '''遍历所要查询属性，以生成sql语句'''
    if props == '*':
        sqlstr += ' *'
    elif type(props) == type([0]):
        i = 0
        for prop in props:
            if(i == 0):
                sqlstr += ' ' + prop
            else:
                sqlstr += ', ' + prop
            i += 1
    else:
        log.msg('props to query must be list')
        return
    return sqlstr

def generateInsertSql(sql, props):
    '''
                生成插入数据sql
    '''
    i = 0
    for prop in props:
        if i == 0:
            sql += prop.__str__()
        else:
            if type(prop) == type('') or type(prop) == type(u''):
                sql += ",\"%s\"" % prop
            elif prop == None:
                sql += ",\"%s\"" % ''
            else:
                sql += ",%d" % prop
        i += 1
    sql += ")"
    return sql

def forEachUpdateProps(sqlstr, props):
    '''遍历所要修改的属性，以生成sql语句'''
#    if props==None or props=='':
#        return 
#    if type(props)==type({'id':5}):
    if type(props) == dict:
        i = 0
        items = props.items()
        for prop in items:
            columnName = prop[0]
            columnValue = prop[1]
            if isinstance(prop[1],basestring):
                if(i == 0):
                    sqlstr += " %s=\"%s\"" % (columnName, columnValue)
                else:
                    sqlstr += ", %s=\"%s\"" % (columnName, columnValue)
            else:
                if(i == 0):
                    sqlstr += " %s=%s" % (columnName, columnValue)
                else:
                    sqlstr += ", %s=%s" % (columnName, columnValue)
            i += 1
    else:
        #print 'props to query must be dict'
        return
    return sqlstr

def isStr(value):
    '''
    是否是合法的类型
    '''
    if not value:
        return False
    return type(value) == type('')

def isDigit(value):
    '''
    是否是合法的类型
    '''
    if  not value:
        return False
    return value.__str__().isdigit()




ISOTIMEFORMAT = '%Y-%m-%d %X'

def ISOString2Time(s):
    '''
    convert a ISO format time to second
    from:2006-04-12 16:46:40 to:23123123
    把一个时间转化为秒
    '''
    return time.strptime(s, ISOTIMEFORMAT)
def Time2ISOString(s):
    '''
    convert second to a ISO format time
    from: 23123123 to: 2006-04-12 16:46:40
    把给定的秒转化为定义的格式
    '''
    return time.strftime(ISOTIMEFORMAT, time.localtime(float(s)))

def dateMinDate(d1, d2):
    '''
    minus to iso format date,return seconds
    计算2个时间相差多少秒
    '''
    d1 = ISOString2Time(d1)
    d2 = ISOString2Time(d2)
    return time.mktime(d1) - time.mktime(d2)

def replaceWords(words, newWords, sqlstr):
    '''替换字符串'''
    import string
    newString = string.replace(sqlstr, words, newWords)
    return newString

def objectCopy(obj):
    import copy
    return copy.deepcopy(obj)

def splitPosition(position):
    position = eval("[" + position + "]")
    for elm in position:
        elm = int(elm)
    return position

def tranverEventContent(content):
    eventStr = ''
    now = datetime.datetime.now()
    if type(content) == type({}):
        eventStr = "{"
        m = 0
        for key, value in content.items():
            valueStr = ""
            if type(value) == type({}):
                valueStr = "{"
                i = 0
                for childKey, childValue in value.items():
                    i += 1
                    if i == len(value.items()):
                        if type(childValue) == type('') or type(childValue) == type(u'') or type(childValue) == type(now):
                            valueStr += "'" + childKey + "':'" + str(childValue) + "'"
                        else:
                            valueStr += "'" + childKey + "':" + str(childValue)
                    else:
                        if type(childValue) == type('') or type(childValue) == type(u''):
                            valueStr += "'" + childKey + "':'" + str(childValue) + "',"
                        else:
                            valueStr += "'" + childKey + "':" + str(childValue) + ","
                valueStr += "}"
            elif type(value) == type([]):
                valueStr = "["
                i = 0
                for child in value:
                    i += 1
                    if i == len(value):
                        valueStr += str(child)
                    else:
                        valueStr += str(child) + ","
                valueStr += "]"
            else:
                valueStr += str(value)
            m += 1
            if m == len(content.items()):
                if type(valueStr) == type('')or type(valueStr) == type(u'') or type(childValue) == type(now):
                    eventStr += "'" + key + "':'" + valueStr + "'"
                else:
                    eventStr += "'" + key + "':" + valueStr
            else:
                if type(valueStr) == type('')or type(valueStr) == type(u''):
                    eventStr += "'" + key + "':'" + valueStr + "',"
                else:
                    eventStr += "'" + key + "':" + valueStr + ","
        eventStr += "}"
    elif type(content) == type([]):
        eventStr = "["
        n = 0
        for elm in content:
            valueStr = ""
            if type(elm) == type({}):
                valueStr = "{"
                j = 0
                for childKey, childValue in elm.items():
                    if j == len(elm.items()):
                        if type(childValue) == type(u'')or type(childValue) == type('')or type(childValue) == type(now):
                            valueStr += "'" + childKey + "':'" + str(childValue) + "'"
                        else:
                            valueStr += "'" + childKey + "':" + str(childValue)
                    else:
                        if type(childValue) == type(u'')or type(childValue) == type(''):
                            valueStr += "'" + childKey + "':'" + str(childValue) + "',"
                        else:
                            valueStr += "'" + childKey + "':" + str(childValue) + ","
                valueStr += "}"
            elif type(elm) == type([]):
                valueStr = "["
                j = 0
                for child in elm:
                    if j == len(elm):
                        if type(child) == type(u'')or type(child) == type(now):
                            valueStr += "'" + str(child) + "'"
                        else:
                            valueStr += str(child)
                    else:
                        if type(child) == type(u''):
                            valueStr += "'" + str(child) + "',"
                        else:
                            valueStr += str(child) + ","
                valueStr += "]"
            elif type(elm) == type(now):
                valueStr += "'" + str() + "'"
            else:
                valueStr += str(elm)
            n += 1
            if n == len(content):
                eventStr += valueStr
            else:
                eventStr += valueStr + ","
        eventStr += "]"

    return eventStr

def tranverseObjectToPickleStr(content):
    ''''''
    import cPickle
    import string
    content = string.replace(cPickle.dumps(content), '\\u', '\\\\u').encode('utf8')
    return content

def parsePickleStrToObject(pickleString):
    ''''''
    import cPickle
    pickleObj = None
    try:
        pickleObj = cPickle.loads(pickleString.encode('utf8'))
    except Exception, e:
        log.msg(str(e))
    return pickleObj

def parseScript(script):
    '''解析附加属性脚本'''
    sqlstr = ''
    if script.find('maxHp') <> -1:
        sqlstr += '最大体力'
    elif script.find('maxHPercent') <> -1:
        sqlstr += '最大体力'
    elif script.find('maxMp') <> -1:
        sqlstr += '最大法力'
    elif script.find('maxMPercent') <> -1:
        sqlstr += '最大法力'
    elif script.find('maxAttack') <> -1:
        sqlstr += '攻击'
    elif script.find('maxAPercent') <> -1:
        sqlstr += '攻击'
    elif script.find('defense') <> -1:
        sqlstr += '防御'
    elif script.find('deFPercent') <> -1:
        sqlstr += '防御'
    elif script.find('hitrate') <> -1:
        sqlstr += '命中'
    elif script.find('dodgerate') <> -1:
        sqlstr += '最大法力'
    elif script.find('crirate') <> -1:
        sqlstr += '最大法力'
    elif script.find('bogeyrate') <> -1:
        sqlstr += '最大法力'
    elif script.find('extraStr') <> -1:
        sqlstr += '附加力量'
    elif script.find('extraDex') <> -1:
        sqlstr += '附加灵巧'
    elif script.find('extraVit') <> -1:
        sqlstr += '附加体质'

    if script.find('+') <> -1:
        sqlstr += "+"
    elif script.find('*') <> -1:
        sqlstr += "x"

    elments = script.split('=')
    index = elments[1].find(';')

    if index <> -1:
        if sqlstr.find('x') <> -1:
            value = int((float(elments[1][:index]) - 1) * 100)
            sqlstr += value.__str__()
            sqlstr += '%'
        else:
            sqlstr += elments[1][:index]

    return sqlstr

def formatListToString(props):
    '''由列表格式化生产字符串'''
    insertStr = ''
    for prop in props:
        insertStr = insertStr + str(prop) +','
    insertStr = insertStr[:-1]
    return insertStr

def producePrer(prer):
    '''生成查询语句的条件
    @param prer: dict 包含了查询的条件
    '''
    
def forEachPlusUpdateProps(props):
    if type(props) == dict:
        i = 0
        items = props.items()
        for prop in items:
            columnName = prop[0]
            columnValue = prop[1]
            if type(columnValue) == type(''):
                if(i == 0):
                    str += " %s=\"%s\"" % (columnName, columnValue.__str__())
                else:
                    str += ", %s=\"%s\"" % (columnName, columnValue.__str__())
            else:
                if(i == 0):
                    str += " %s=%s" % (columnName, columnValue)
                else:
                    str += ", %s=%s" % (columnName, columnValue)
            i += 1
    else:
        #print 'props to query must be dict'
        return
    return str
    
def forEachUpdatePropsForIncrement(sqlstr, props):
    '''遍历所要修改的属性，以生成sql语句'''
#    if props==None or props=='':
#        return 
#    if type(props)==type({'id':5}):
    if type(props) == dict:
        i = 0
        items = props.items()
        for prop in items:
            columnName = prop[0]
            columnValue = prop[1]
            if type(columnValue) == type(''):
                if(i == 0):
                    sqlstr += " %s='%s'" % (columnName, columnValue.__str__())
                else:
                    sqlstr += ", %s='%s'" % (columnName, columnValue.__str__())
            else:
                if(i == 0):
                    sqlstr += " %s=%s" % (columnName, columnValue)
                else:
                    sqlstr += ", %s=%s" % (columnName, columnValue)
            i += 1
    else:
        assert 'props to query must be dict'
        return
    return sqlstr

def produceSQLlimit(sql,props):
    '''生成带范围限制的SQL语句'''
    if type(props) == dict:
        items = props.items()
        for prop in items:
            columnName = prop[0]
            columnValue = prop[1]
            sql += " AND %s <= %d"%(columnName,columnValue)
    else:
        assert 'props to query must be dict'
    return sql
            
def froEachQueryByProps(sql,props):
    '''遍历字典类型的条件，生成sql查询条件'''
    if type(props)!=dict:
        return ''
    for item in props.items():
        if type(item[1])==str:
            sql +="and %s = '%s'"%(item[0],item[1])
        else:
            sql +="and %s = %s"%(item[0],str(item[1]))
    return sql
    
def forEachInsertByProps(sql,props):
    '''遍历字典，生成插入sql语句'''
    if type(props) == dict:
        items = props.items()
        template = "("
        insertValues = "("
        for prop in items:
            columnName = prop[0]
            columnValue = prop[1]
            template += columnName+','
            if type(columnValue) == type(''):
                insertValues += "'%s',"%columnValue
            else:
                insertValues += "%d,"%columnValue
        sql = sql + template[:-1]+") values "+insertValues[:-1]+")"
        return sql
    else:
        assert 'props to query must be dict'
        return
    return sql
     



