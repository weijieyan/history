#!/usr/bin/env python
# encoding: utf-8
'''
Created on 2013-3-28

@author: Administrator
'''
class RBAC(object):
    def isUserExist(self,username):
        pass
    def login(self,username,password):
        pass
    def addUser(self,user):
        pass
        
 
    def deleteUser(self,userID):
        pass
    def addRole(self,role):
        pass
    def deleteRole(self,roleID):
        pass
    def assignUser(self,userID,roleID):
        pass
            
    def deassignUser(self,userID,roleID):
        pass
    def grantPermission(self,roleID,privilegeID):
        pass
    def revokePermission(self,roleID,privilegeID):
        pass
    def checkAccess(self,roleID,resource,operation):
        pass
           