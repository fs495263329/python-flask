#encoding=utf-8
import gconf
import  json

def get_users():
    try:
        handler=open(gconf.USER_FILE,'rb')
        cxt=handler.read()
        handler.close()
        return  json.loads(cxt)   
    except:
        return []

def validate_login(username,password):
    users=get_users()
    for user  in users:
        if  user.get('username')==username and user.get('password')==password:
            return True
    return  False
