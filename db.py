#!/usr/bin/env python
# encoding: utf-8
'''
Created on 2013-2-15

@author: Administrator
'''
import itertools
from rbac import RBAC
import logging 
class MRBAC(RBAC):
    def __init__(self,db):
        self.db=db  
    def isUserExist(self,username):
        users=self.db.query("select username from user where username=%s",username)
        return True if users else False
    def login(self,username,password):
        user=self.db.query("select * from user where username=%s and password=%s",username,password)
        return True if user else False    

    def addUser(self,*user):
        sql="insert into user(username,password,status,rolename,add_time) values(%s,%s,0,'游客',NOW())" 
        self.db.execute(sql,*user)
         
        
 
    def deleteUser(self,userID):
        self.db.execute("delete from user where id=%s",userID)

    def addRole(self,rolename,description):
        self.db.execute("insert into role(rolename,description,add_time) values(%s,%s,now())",rolename,description)
         
    def deleteRole(self,roleID):
        self.db.execute("delete from role where id=%s",roleID)

    def assignUser(self,userID,roleID):
        self.db.execute("insert into user_role_assignment(user,role) values(%s,%s)",userID,roleID)
         
            
    def deassignUser(self,userID,roleID):
        self.db.execute("delete from user_role_assignment where user=%s and role=%s",userID,roleID)
    def addPrivilege(self,resource,operation):
        self.db.execute("insert into privilege(resource,operation) values(%s,%s)",resource,operation)
        
    def grantPermission(self,rolename,privilegeID):
        self.db.execute("insert into role_privilege_assignment(role,privilege) values(%s,%s)",rolename,privilegeID)
    def revokePermission(self,rolename,privilegeID):
        self.db.execute("delete into role_privilege_assignment where role=%s and privilege=%",rolename,privilegeID)
        
    def checkAccess(self,roleID,resource,operation):
        
        privilegeIDs=self.db.query("select * from role_privilege_assignment where role=%s",roleID)
        for id in privilegeIDs:
            privilege=self.db.query("select * from privilege\
            where id=%s and resource=%s and operation=%s",id,resource,operation)
            if privilege:
                return True
        return False

    
import unittest
class DatabaseTest(unittest.TestCase):
    def setUp(self):
        import tornado.database
        self.db = tornado.database.Connection(
            host="127.0.0.1:3306", database="role_model",
            user="root", password="123000")
        self.rbac=MRBAC(self.db)
        
    def test_isuserexist(self):
        print self.rbac.isUserExist("yanfffffffffffweijie")
    def test_login(self): 
        print self.rbac.login("yanweijie", "123000")
        print self.rbac.login("yanweijfffffffffffffie", "123000")
    def test_adduser(self):
        import time
        t1=time.time()
        for i in range(1):
            self.rbac.addUser("Sdfsdf","sdfsdf")
        t2=time.time()
        print t2-t1
    def test_drop(self):
            self.rbac.deleteUser(10)
#    def test_check(self):
#        print self.con.execute("INSERT INTO `user` (`username`, `password`) VALUES ('%s', '%s')","weijieyan","123000")