#!/usr/bin/env python
# encoding: utf-8
'''
Created on 2013-3-21

@author: Administrator
'''
import tornado.web
from tornado.web import HTTPError
from tornado.options import  options
from db import MRBAC
import random, string
import datetime
import uuid
import ujson
import json, re, urllib
import time, hashlib
import sys, os
import search_history
class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def get_current_user(self):
        user_id = self.get_secure_cookie("user")
        if not user_id: return None
        return self.db.get("SELECT * FROM user WHERE id = %s", int(user_id))
class Home(BaseHandler):
    def get(self):
        entries=self.db.query("select * from entry limit 0,20")
        self.render("index.html",entries=entries)
class Register(BaseHandler):
    def get(self):
        self.render("register.html")
    def post(self):
        username=self.get_argument("username", None)
        password=self.get_argument("password", None)


        if username and password:
            user=self.db.query("select * from user where username=%s",username)
            if user:
                self.redirect("/register")
                return
            rbac=MRBAC(self.db)
            rbac.addUser(username,password)       
            result=self.db.get("select * from user where username=%s and password=%s",username,password)
            user_id=result.id
            self.set_secure_cookie("user", str(user_id))
            self.redirect("/")
            return
        else :
            self.redirect("/register")    
class MongthlyVote(BaseHandler):
    def get(self):
        entries=self.db.query("select * from entry limit 0,20")
        self.render("mongthlyvote.html",entries=entries)
class Vote(BaseHandler):
    def get(self,userid,id):
        votes=self.db.query("select * from vote where entry_id=%s and user_id=%s",id,userid)
        if not votes:
            self.db.execute("insert into vote(user_id,entry_id) values(%s,%s)",userid,id)
            self.db.execute("update entry set vote=vote+1")
        self.redirect("/monthlyvote")
        
class Entry(BaseHandler):
    def get(self,id):
        entry=self.db.get("select * from entry where id=%s",id)
        self.render("entry.html",entry=entry)
class Search(BaseHandler):
    def get(self):
        self.render("search.html")
    def post(self):
        search=self.get_argument("search", None)
        if not search:
            self.redirect("/search")
        querystring=search
        matches=search_history.search(querystring)
        self.render("search_list.html",matches=matches)
class Ejournal(BaseHandler):
    def get(self):
        self.render("journal.html")
    def post(self):
        self.render("journal.html")
class Download(BaseHandler):
    @tornado.web.authenticated
    def get(self,fileid):
        if not fileid:
            self.redirect("/monthlyvote")
     
        historyfile=self.db.get("select * from historyfile where fileid=%s",fileid)
        
        self.set_header('Content-Type','application/msword') 
        self.set_header("Content-Disposition", "attachment;filename=%s"%historyfile.filename)
         
        with open(historyfile.file_url,'rb') as f:
            self.write(f.read())
        self.flush() 
class Upload(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("upload.html",login_error=None)
    def post(self):
        title=self.get_argument("title", None)
        keywords=self.get_argument("keywords", None)
        desc=self.get_argument("desc", None)
        area=self.get_argument("area", None)
        username=self.current_user.username
        fileid=self.get_argument("fileid", None)
        if title and keywords and desc  and area and fileid:
            self.db.execute("INSERT INTO entry (author,entryname,keywords,description,area,add_time,fileid) VALUES (%s,%s,%s,%s,%s,Now(),%s)",username,title,keywords,desc,area,fileid)
            
            self.redirect("/")
        else:
            self.render("upload.html",login_error="不能为空")
class FileUpload(BaseHandler):
    filenamePrefix = "tornado_history_"
    # Set to None for no size restrictions
    maxFileSize = 500 * 1000 * 1000 # MB

    def acceptedFileType(self, type):
        regexp = None
        # regexp = re.compile('image/(gif|p?jpeg|(x-)?png)')
        if regexp and regexp.match(type):
            return True
        else:
            return False
    def validate(self, file):
        """
        Takes as input a file object and raises an exception if the file does
        not conform to the criteria.
        """
        if self.maxFileSize and file['size'] < self.maxFileSize:
            raise HTTPError(406, "File too big")

        if not self.acceptedFileType(file['type']):
            raise HTTPError(406, "File of unsupported type")

    def saveFile(self, data, filelocation):
        """
        This can be ovewritten to implement your own file writing functions.
        """
        with open(filelocation, 'wb+') as f:
            f.write(data)
        
    def process_file(self, file):
        filename = re.sub(r'^.*\\', '', file['filename'])
        
        result = {}
        result['name'] = filename
        result['type'] = file['content_type']
        result['size'] = len(file['body'])

        filelocation = self.getFileLocation(filename)
#        filetoken = self.getFileToken(filelocation)

#        result['token'] = filetoken
        result['success']=True
        self.saveFile(file['body'], filelocation)
        result['fileid']=self.get_argument("qquuid")
        self.db.execute("insert into historyfile(file_url,fileid,filename,filetype,filesize) values(%s,%s,%s,%s,%s)",filelocation,result['fileid'],result['name'],result['type'],result['size'])
        return result

    def getFileToken(self, filelocation):
        """
        Ovewrite this with a function that returns the token to be given to the
        user for accessing the file.
        """
        return filelocation

    def getFileLocation(self, filename):
        """
        Ovewrite me with your own function to generate the location of where
        the file should be stored.
        """
        rname = hashlib.sha256(filename).hexdigest()
        name = "d:/history/"+self.filenamePrefix+rname+".history"
        return name

    def handle_upload(self):
        # XXX will this ever be bigger than 1?
        files = self.request.files['qqfile']
        for file in files:
            start_time = time.time()

            result = self.process_file(file)
            result['elapsed_time'] = time.time() - start_time
           
            return result

    def post(self):
        s = json.dumps(self.handle_upload())
        
        if 'application/json' in self.request.headers.get('Accept'):
            self.set_header('Content-Type', 'application/json')
        self.write(s)
class AuthLoginHandler(BaseHandler):
    def get(self):
        if self.current_user:
            self.redirect("/")
            return
        self.render("login.html")
    def post(self):
        username = self.get_argument("username",None)
        password = self.get_argument("password",None)
        if not username or not password:
            self.redirect("/auth/login")
            return
        result=self.db.get("select * from user where username=%s and password=%s",username,password)
        if not result:
            self.redirect("/auth/login")
            return
        
        user_id=result.id
        self.set_secure_cookie("user", str(user_id))
        self.redirect(self.get_argument("next","/"))

class AuthLogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", "/"))
handler_urls = [
        (r"/",Home),
         (r"/monthlyvote",MongthlyVote),
         (r"/vote/([0-9]+)/([0-9]+)",Vote),
        (r"/search",Search),
        (r"/register",Register),
        (r"/download/(.*)",Download),
        (r"/upload",Upload),
        (r"/fileupload",  FileUpload),
        (r"/entry/([0-9]+)",  Entry),
        
        (r"/auth/login", AuthLoginHandler),
        (r"/auth/logout", AuthLogoutHandler),
       
]