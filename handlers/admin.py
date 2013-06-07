#!/usr/bin/env python
# encoding: utf-8
'''
Created on 2013-2-27

@author: Administrator
'''
from db import MRBAC
from handler import BaseHandler
class AdminHome(BaseHandler):
    def get(self):
        self.render("admin/index.html")
class AdminRole(BaseHandler):
    def get(self):
        roles=self.db.query("select * from role")
        privileges=self.db.query("select * from privilege")
        self.render("admin/role.html",roles=roles,privileges=privileges)
    def post(self):
        rolename=self.get_argument("rolename",None)
        desc=self.get_argument("desc",None)
        privilegeIDs=self.get_arguments("privilegeID")
        if rolename and desc and privilegeIDs:
            print True
            rbac=MRBAC(self.db)
            rbac.addRole(rolename,desc)
            for privilegeID in privilegeIDs:
                rbac.grantPermission(rolename, privilegeID)
                
        self.redirect('/admin/role')
class DeleteRole(BaseHandler):
    def post(self):
        ids=self.get_arguments("roleID")
        for id in ids:
            self.db.execute("delete from role where id=%s",int(id))
        
        self.redirect("/admin/role")
class AdminPost(BaseHandler):
    def get(self):
        entries=self.db.query("select * from entry order by status desc")
        self.render("admin/entry.html",entries=entries)
    def post(self):
        pass
class AdminUsers(BaseHandler):
    def get(self):
        current_page=int(self.get_argument("page", 0)) 
        if current_page<0:
            current_page=0
        limit=10
        index=limit*current_page
        users=self.db.query("select * from user order by status desc limit %s,%s ",index,limit)
        print users
        self.render("admin/users.html",users=users,current_page=current_page)
    def post(self):
        username=self.get_argument("username", None)        
        if username:
            users=self.db.query("select * from user where username=%s",username)
            self.render("admin/users.html",users=users,current_page=0)
        else:
            self.redirect("/admin/users")
class VerifyUsers(BaseHandler):
    def post(self):
        ids=self.get_arguments("userID")
        for id in ids:
            self.db.execute("update user set status=1 where id=%s",int(id))
        self.redirect("/admin/users")
class DeleteUsers(BaseHandler):
    def post(self):
        ids=self.get_arguments("userID")
        for id in ids:
            self.db.execute("delete from user where id=%s",int(id))
        
        self.redirect("/admin/users")
 
        
        
admin_urls = [
        (r"/admin",AdminHome),
         (r"/admin/users",AdminUsers),
          (r"/admin/users/verify",VerifyUsers),
          (r"/admin/users/delete",DeleteUsers),
          (r"/admin/role",AdminRole),
         
          (r"/admin/role/delete",DeleteRole),
           (r"/admin/post",AdminPost),
        
]
import tornado.testing
class MyHTTPTest(tornado.testing.AsyncHTTPTestCase):
    def get_app(self):
        from app import Application
        return Application()

    def homepage(self):
        # The following two lines are equivalent to
        #   response = self.fetch('/')
        # but are shown in full here to demonstrate explicit use
        # of self.stop and self.wait.
        self.http_client.fetch(self.get_url('/register'), self.stop,method="POST",body="username=yanweijie&password=123000")
        response = self.wait()
        print response.body
    def test_register(self):
        # The following two lines are equivalent to
        #   response = self.fetch('/')
        # but are shown in full here to demonstrate explicit use
        # of self.stop and self.wait.
        self.http_client.fetch(self.get_url('/register'), self.stop,method="POST",body="jk=ui")
        response = self.wait()
        print response.body
        