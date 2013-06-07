#!/usr/bin/env python
# encoding: utf-8
'''
Created on 2013-2-23

@author: Administrator
'''
class User(object):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String(50))

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.username)
class Role(object):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    rolename= Column(String(45),unique=True)
    role_describe=Column(String(100))
    def __init__(self,rolename=None):
        """Documentation"""
        self.rolename=rolename
class UserRoleAssignment(object):
    __tablename__ = 'user_role_assingment'
    id = Column(Integer, primary_key=True)
    role= Column(Integer)
    user=Column(Integer)

    def __init__(self, role=None, user=None):
        self.role = role
        self.user = user

     
class Privilege(object):
    __tablename__ = 'privileges'
    id = Column(Integer, primary_key=True)
    resource= Column(String(45))
    operate= Column(String(45))
    def __init__(self, resource=None,operate=None):
        """Documentation"""
        self.resource=resource
        self.operate=operate



class RolePrivilegeAssignment(object):
    __tablename__ = 'role_privilege_assignment'
    id = Column(Integer, primary_key=True)
    role= Column(String(45))
    privilege= Column(Integer)
    def __init__(self, role=None,privilege=None):
        """Documentation"""
        self.role=role
        self.privilege=privilege
        
class RoleInherit(object):
    __tablename__ = 'role_inherit'
    id = Column(Integer, primary_key=True)
    from_role= Column(Integer)
    to_role= Column(Integer)
    def __init__(self, from_role=None, to_role=None):
        self.from_role = from_role
        self.to_role = to_role
