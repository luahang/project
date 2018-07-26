import pymysql

setttings = {
            'host': 'localhost',
            'port': 3306,
            'user': 'root',
            'password': '123456',
            'database': 'blog_db',
            'charset': 'utf8',
        }
connection = pymysql.connect(**setttings)
cursor = connection.cursor()
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
cursor.execute(sql)
list = cursor.fetchall()
L = []
blogs = []
for i in list:
    L.append(i)
for j in L:
    dict = {
        'author':j[0],
        'title':j[1],
        'cotent':j[2],
        'avatar':j[3],
        'tags':j[4],
        'count':j[5],
    }
    blogs.append(dict)
print(list[0][3])
