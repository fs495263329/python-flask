#encoding=utf-8
import gconf
import  json
import MySQLdb
from  dbutils import execute_fetch_sql,execute_commit_sql

def get_users():
    _columns=('id','username','password','age')
    _sql='select *  from user'
    _rt=[]
    _count,_rt_list=execute_fetch_sql(_sql)
    for _line in _rt_list:
        _rt.append(dict(zip(_columns,_line)))
    return _rt


def validate_login(username,password):
    _sql='select *  from user where username=%s and  password=md5(%s)'
    _count,_rt_list=execute_fetch_sql(_sql,(username,password))
    return _count

def validate_add_user(username, password, age):
    if username.strip() == '':
        return False, u'用户名不能为空'

    #检查用户名是否重复
    _users = get_users()
    for _user in _users:
        if username == _user.get('username'):
            return False, u'用户名已存在'

    #密码要求长度必须大于等于6
    if len(password) < 6:
        return False, u'密码必须大于等于6'

    if not str(age).isdigit() or int(age) <= 0 or int(age) > 100:
        return False, u'年龄必须是0到100的数字'

    return True, ''


def add_user(username, password, age):
    _sql = 'insert  into user(username,password,age) values(%s,md5(%s),%s)'
    _args=(username,password,age)
    execute_commit_sql(_sql,_args)

def save_users(users):
    fhandler = open(gconf.USER_FILE, 'wb')
    fhandler.write(json.dumps(users))
    fhandler.close()

def get_user(username):
    _users = get_users()
    for _user in _users:
        if _user.get('username') == username:
            return _user

    return None

def validate_update_user(username, password, age):
    if get_user(username) is None:
        return False, u'用户信息不存在'

    #密码要求长度必须大于等于6
    if len(password) < 6:
        return False, u'密码必须大于等于6'

    if not str(age).isdigit() or int(age) <= 0 or int(age) > 100:
        return False, u'年龄必须是0到100的数字'

    return True, ''




def update_user(username, password, age):
    _users = get_users()
    for _user in _users:
        if _user.get('username') == username:
            _user['password'] = password
            _user['age'] = age
            save_users(_users)
            break


def delete_user(username):
    _users = get_users()
    _idx = -1
    for _user in _users:
        _idx += 1
        if _user.get('username') == username:
            del _users[_idx]
            save_users(_users)
            break

