#coding:utf8
'''
Created on 2009-12-8

@author: sean_lan
'''

import csv, sqlite3, os

class DataLoader(object):
    '''
    数据加载类，用于读取文件夹指定文件的数据到内存数据库中
    '''

    def __init__(self):
        '''
        Constructor
        '''

    def getTableName(self, fileName):
        '''
                    根据文件名生成内存数据库表名
        '''
        if(fileName != ''):
            tableName = fileName.split('.')[0]
        else:
            tableName = ''
        return tableName

    def formatColumnName(self, columnName):
        '''
                     将读进的列名首字母去掉，并lowercase当前的首字母
        @columnName:文件中读到的第一行的各项，用于生成表的列名
        '''
        if(columnName == '' or columnName == None):
            #print 'The column name to format is null'
            return
        chars = columnName.split()[0][1:]
        chars = chars.replace(chars[0], chars[0].lower(), 1)
        return chars

    def generateCreateTableSql(self, row, tableName):
        '''
                        根据cvs文件的字段组装生成table的sql语句
        @row:数据文件中的头一行
        @tableName创建的表名
        '''
        if tableName == '':
            #print('table name is null')
            return
        sql = "create table " + tableName + "(";
        length = len(row)
        for i in range(0, length):
            if(i == 0):
                sql += self.formatColumnName(row[i]) + " integer primary key,"
            elif(i == length - 1):
                sql += self.formatColumnName(row[i])
                sql = self.getColumType(sql, row[i])
            else:
                sql += self.formatColumnName(row[i])
                sql = self.getColumType(sql, row[i])
                sql += ','
        sql += ")"
        ##print sql
        return sql

    def generateInsertSql(self, tableName, row, columnRow):
        '''
                    组装插入数据sql
        @tableName:表名
        @row:数据行
        @columnRow:字段名行
        '''
        sql = "insert into " + tableName + " values("
        consoleSql = "insert into " + tableName + " values("
        rows = []#存放格式化后插入数据项
        length = len(row)
        for i in range(0, length):
            if(i == length - 1):
                sql += "?)"
                consoleSql += row[i].decode('gbk') + ")"
            else:
                sql += "?,"
                consoleSql += row[i].decode('gbk') + ","
            if(columnRow[i].startswith('s')):
                rows.append(unicode(row[i], 'gbk'))
            elif(columnRow[i].startswith('i')):
                rows.append(int(row[i]))
            elif(columnRow[i].startswith('f')):
                rows.append(float(row[i]))
        return sql, rows

    def getColumType(self, sql, columnName):
        '''
                        确定表列的类型
         @sql:sql语句
         @columnName:字段名            
        '''
        if(columnName == '' or columnName == None):
            #print 'column name is null'
            return
        if(columnName.startswith('i')):
            sql += ' integer'
        elif(columnName.startswith('f')):
            sql += ' float'
        elif(columnName.startswith('s')):
            sql += ' text'
        return sql

    def read(self, folderName):
        '''
                    从文件夹路径下读取所有文件数据到内存中（创建内存数据库表）
        @folderName:文件夹名
        '''
        for item in os.listdir(folderName):
            info = folderName + '/' + item
            if os.path.isfile(info):
                self.readSingleFile(info, item)
        return
#        for files in os.walk(folderName):
#            csvs = files[2]#目前含有svn文件，所以暂时这样(index=2)，以后动态修改
#            for csvfile in csvs:
#                if(csvfile.find('.csv.svn-base')==-1 and csvfile.find('.csv')!=-1):
#                    filePath = folderName+csvfile
#                    self.readSingleFile(filePath,csvfile) 

    def readSingleFile(self, filePath, fileName):
        '''
                    读取每个文件数据到内存中
        @filePath:文件路径
        @fileName:文件名
        '''
        reader = csv.reader(open(filePath, 'r'))
        tableName = self.getTableName(fileName)
        if tableName == "place":
            assert 1 == 1
        columnRow = None
        i = 1
        for row in reader:
            if(i == 1):
                columnRow = row
                createTableSql = self.generateCreateTableSql(row, tableName)
                connection.execute(createTableSql)
            else:
                ret = self.generateInsertSql(tableName, row, columnRow)
                insertSql = ret[0]
                datas = ret[1]
                ##print insertSql
                ##print datas
                connection.execute(insertSql, datas)
            i += 1

#--------------------------------------------------Query-------------------------------------------------------            
    def getById(self, tableName, idValue, props):
        '''根据id查询内存数据库'''
        querySql = 'select'
        querySql = self.forEachQueryProps(querySql, props)
        querySql += 'from `%s` where id = %d' % (tableName, int(idValue))
        ##print querySql
        cursor = connection.cursor()
        cursor.execute(querySql)
        result = cursor.fetchone()
        cursor.close()
        return result
    
    def get(self, tableName, propName, propValue, props):
        ''''''
        queryStr = 'select'
        queryStr = self.forEachQueryProps(queryStr, props)
        queryStr += "from `%s` where %s = '%s'" % (tableName, propName, str(propValue))
#        #print queryStr 
        cursor = connection.cursor()
        result = cursor.execute(queryStr).fetchall()
        cursor.close()
        return result
    
    def getall(self, tableName, props):
        queryStr = 'select'
        queryStr = self.forEachQueryProps(queryStr, props)
        queryStr += "from `%s`" % (tableName)
        cursor = connection.cursor()
        result = cursor.execute(queryStr).fetchall()
        cursor.close()
        return result
#        #print queryStr 
         
    def getDataByMultiOption(self, tableName, multiopt, multival, props):
        assert len(multiopt) == len(multival) != 0
        def parse(opt, val):
            assert len(opt) == len(val)
            ret = ' '
            for i in range(len(opt)):
                ret += str(opt[i]) + '=' + str(val[i]) + ' '
            return ret
        querySql = 'select'
        querySql = self.forEachQueryProps(querySql, props)
        querySql += 'from `%s` where %s' (tableName, parse(multiopt, multival))
        ##print querySql
        cursor = connection.cursor()
        cursor.execute(querySql)
        result = cursor.fetchone()
        cursor.close()
        return result

    def formatRow(self, cursor, row):
        '''设置记录为dict的形式'''
        dict = {}
        for idx, col in enumerate(cursor.description):
            dict[col[0]] = row[idx]
        return dict

    def forEachQueryProps(self, str, props):
        '''遍历所要查询属性，以生成sql语句'''
        if props == '*':
            str += " * "
        elif type(props) is list:
            str += ' ' + ', '.join(props) + ' '
        else:
            pass
            #print 'props to query must be list '
        return str
    
    
#-------------------------------------------------------------------------------------------------------------------  

    def test(self):
        u, v = self.getById('skill', 1, '*'), '-----'
        #print u, v
        #print self.getById('skill', 1, ['name', 'id'])
        #print self.get('skill', 'name', '毒药术', '*')
        ret4 = self.getById("place", 101, ['TeamType'])
        #print "ret4 =", ret4
        allnpc = loader.getById('quest_template', 113203, ['name'])
        if allnpc:
            allnpc = [allnpc]
            data = []
            for i in allnpc:
                info = loader.getById('generals', 1, '*')
                if info:
                    data.append(info)
            #print data

connection = sqlite3.connect(":memory:")
loader = DataLoader()
connection.row_factory = loader.formatRow

def getSkillId(groupType,level):
    '''根据技能分组获取技能的id
    @param GroupType: int 技能分组
    @param level: int 技能的等级
    '''
    sql = "select id from `skill` where groupType =%d and level = %d"%(groupType,level)
    cursor = connection.cursor()
    cursor.execute(sql)
    ret = cursor.fetchone()
    cursor.close()
    if ret:
        return ret['id']
    return 0
    

def getDutyNameById(id):
    '''根据id获取职位字段名称'''
    dutyName = loader.getById('duty',id,['dutyName'])
    dutyName = dutyName['dutyName']
    return dutyName
    
if __name__ == '__main__':
    loader.read("../data")
    data = loader.getById('methodMap',100,['methodName'])
    getDutyNameById(3)
    #print data
    npcInfo = loader.getById('duty', 2, ['id', 'dutyName','name'])
    
    #print npcInfo
    #print loader.get('methodMap', 'methodName', 'pushChatMessage', ['id'])
