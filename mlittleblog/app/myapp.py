from os import remove
from tornado.web import Application, RequestHandler, UIModule
import uuid

from util.dbutil import Dbutil
from util.mysession import MySession
from util.myutil import release


class LoginHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.set_cookie('cookie1','ilikecookie')
        msg = self.get_query_argument('msg', None)
        if msg:
            self.render('login.html', info='用户名或密码错误')

        else:
            self.render('login.html', info='')

    def post(self, *args, **kwargs):
        uname = self.get_body_argument('uname', None)
        upwd = self.get_body_argument('upwd', None)

        pwd = release(upwd)
        dbutil = Dbutil()
        if dbutil.sucess(uname,pwd):
            s = MySession(self)
            s['islogin'] = True
            self.redirect('/sucess?uname=' + uname)
        else:
            self.redirect('/login?msg=fail')

class LoginModule(UIModule):
    def render(self, *args, **kwargs):
        if self.request.uri == '/login?msg=fail':
            info = '用户名或密码错误'
        else:
            info = ''
        return self.render_string('mymodule/login_module.html',info=info)

class SucessHandler(RequestHandler):
    def get(self, *args, **kwargs):
        s = MySession(self)
        if s['islogin']:
            self.render('blog.html')
        else:
            self.redirect('/login')

    def post(self, *args, **kwargs):
        pass

class IndexHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.render('login.html')

class BlogMoudle(UIModule):
    def render(self, *args, **kwargs):
        dbutil = Dbutil()
        blogs = dbutil.getblogs()
        return self.render_string('mymodule/blog_module.html',blogs=blogs)

class RegisterHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.render('register.html')

    def post(self, *args, **kwargs):
        uname = self.get_body_argument('uname',None)
        upwd = self.get_body_argument('upwd',None)
        city = self.get_body_argument('city',None)

        if uname and upwd and city:
            avatar = None
            if self.request.files:
                fs = self.request.files['avatar'][0]
                body = fs.get('body')
                fname = str(uuid.uuid4()) + fs.get('filename')
                with open('mystatics/images/%s'%fname,'wb') as f:
                    f.write(body)
                    avatar = fname
            # 加密
            pwd = release(upwd)
            dbutil = Dbutil()
            try:
                dbutil.saveuser(uname,pwd,city,avatar)
            except Exception as e:
                if avatar:
                    remove('mystatics/images/%s'%avatar)
                err = str(e)
                code = err.split(',')[0].split('(')[1]
                r = ''
                if code == '1062':
                    r = 'duplicate'
                else:
                    r = 'error'
                self.redirect('/register?msg=' + r)

            else:
                self.redirect('/login')

        else:
            self.redirect('/register?msg=empty')

class RegisterModule(UIModule):
    def render(self, *args, **kwargs):
        print(self.request.query)
        result = ''
        if self.request.uri == '/register?msg=duplicate':
            result = '该用户已经存在'
        if self.request.uri == '/register?msg=empty':
            result = '请输入完整,在点击注册'
        if self.request.uri == '/register?msg=error':
            result = '数据库错误'
        return self.render_string('mymodule/register_module.html',result=result)

class MyApplication(Application):

    def __init__(self,handlers,templatepath,staticpath,moduelers):
        super().__init__(handlers=handlers,
                         templatepath=templatepath,
                         static_path=staticpath,
                         ui_modules=moduelers)
        self.dbutil = Dbutil()

class CheckHandler(RequestHandler):
    def get(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        uname = self.get_body_argument('uname',None)
        # 将uname送入数据库进行查询
        dbutil = Dbutil()
        if dbutil.isexists(uname):
            # 根据相应内容生成响应格式
            self.write({'msg':'fail'})
        else:
            self.write({'msg':'ok'})

class CheckPassHandler(RequestHandler):
    def get(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        uname = self.get_body_argument('uname',None)
        upwd = self.get_body_argument('upwd',None)
        dbutil = Dbutil()
        if not(dbutil.isexists(uname)) and dbutil.judgepass(upwd):
            self.write({'msg':'ok'})
        else:
            self.write({'msg':'fail'})

class CheckImgHandler(RequestHandler):
    def get(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        uname = self.get_body_argument('uname')
        dbutil = Dbutil()
        avatar = dbutil.judgeimg(uname)
        self.write({'msg':avatar})



