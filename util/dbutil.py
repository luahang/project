import pymysql

from util.myutil import release


class Dbutil:
    def __init__(self,**kwargs):
        # 获取数据库连接参数
        # 建立与数据库的连接
        host = kwargs.get('host','localhost')
        port = kwargs.get('port',3306)
        user = kwargs.get('user','root')
        password = kwargs.get('password','123456')
        database = kwargs.get('database','blog_db')
        charset =  kwargs.get('charset','utf8')
        connection = pymysql.connect(host=host,
                                     port=port,
                                     user=user,
                                     password=password,
                                     database=database,
                                     charset=charset)
        if connection:
            self.cursor = connection.cursor()
        else:
            raise Exception('数据库连接参数有误!')

    def sucess(self,uname,upwd):
        # 根据输入的用户名和密码
        sql = 'select count(*) from tb_user WHERE user_name=%s and ' \
              'user_password=%s'
        params = (uname,upwd)
        self.cursor.execute(sql,params)
        result = self.cursor.fetchone()
        # 判定用户是否成功
        if result[0]:
            return True
        else:
            return False

    def saveuser(self,uname,upwd,city,avatar):
        # 根据用户输入的信息　完成注册
        sql = 'insert into tb_user' \
                  '(user_name, user_password, user_avatar, user_city)' \
                  'VALUES (%s,%s,%s,%s)'
        params = (uname,upwd,avatar,city)
        try:
            self.cursor.execute(sql,params)
            self.cursor.connection.commit()
        except Exception as e:
            err = str(e)
            code = err.split(',')[0].split('(')[1]
            r = 'error'
            if code:
                r = 'duplicate'
            raise Exception(r)

    def getblogs(self):
        sql = '''
                        select user_name,blog_title,blog_content,user_avatar,tc,c
                        from (select comment_blog_id,count(*)c
                        from tb_comment
                        group by comment_blog_id)t3
                        right join(select user_name,user_avatar,blog_id,blog_title,blog_content,tc
                        from tb_user
                        join(select blog_id,blog_title,blog_content,tc,blog_user_id
                        from tb_blog
                        left join(select rel_blog_id, group_concat(tag_content)tc
                        from tb_tag
                        join(  select rel_blog_id,rel_tag_id
                        from tb_blog_tag )t
                        on tag_id = rel_tag_id
                        group by rel_blog_id )t1
                        on blog_id = rel_blog_id)t2
                        on user_id = blog_user_id)t4
                        on comment_blog_id = blog_id;
                '''
        self.cursor.execute(sql)
        list = self.cursor.fetchall()
        L = []
        blogs = []
        for i in list:
            L.append(i)
        for j in L:
            dict = {
                'author': j[0],
                'title': j[1],
                'cotent': j[2],
                'avatar': j[3],
                'tags': j[4],
                'count': j[5],
            }
            blogs.append(dict)
        return blogs

    def isexists(self,uname):
        sql = 'select count(*) from tb_user WHERE user_name=%s'
        params = (uname,)
        self.cursor.execute(sql,params)
        result = self.cursor.fetchone()
        if result[0]:
            # 用户表中已经存在
            return True
        else:
            # 不存在
            return False

    # def judgepass(self,upwd):
    #     sql = ''
    #     pwd = release(upwd)
    #     params = (pwd,)
    #     self.cursor.execute(sql,params)
    #     result = self.cursor.fetchone()
    #     if result:
    #         return True
    #     else:
    #         return False

    def judgeimg(self,uname):
        sql = 'select user_avatar from tb_user WHERE user_name=%s'
        params = (uname,)
        self.cursor.execute(sql,params)
        result = self.cursor.fetchone()
        if result:
            if result[0]:
                return result[0]
            else:
                return 'default_avatar.png'
        else:
            return 'default_avatar.png'