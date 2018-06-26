#encoding: utf-8
from  flask  import  Flask,request,render_template,redirect,url_for,flash,session
import userdb as user
import  sys
reload(sys)
sys.setdefaultencoding('utf8')
from  functools  import  wraps


app=Flask(__name__)
app.secret_key="dsfjksakjf"

def  login_required(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if  session.get('user')  is None:
            return redirect('/')
        rt=func(*args,**kwargs)
        return  rt
    return wrapper



@app.route('/',methods=['GET'])
def  index():
    return render_template('login.html')

@app.route('/login',methods=['POST','GET'])
def  login():
    print  request.method
    params= request.args  if request.method == 'GET' else request.form
#    if request.method=='GET':
#        params=request.args
#    else:
#        params=request.form
    username=params.get('username','')
    password=params.get('password','')
    if user.validate_login(username,password):
        session['user']={'username':username}
        return  redirect('/users/')
    else:
        return render_template('login.html',username=username,error="username or password is error")
    print username
    print password
      
    return ''

@app.route('/users/')
@login_required
def users():
#    print session
#    if session.get('user')  is  None:
#        return redirect('/')
    return render_template('users.html',user_list=user.get_users(),msg=request.args.get('msg',''))
#    return render_template('users.html',user_list=user.get_users())

@app.route('/user/create/')                         #将url path=/user/create/的get请求交由create_user处理
@login_required
def create_user():
    return render_template('user_create.html')      #加载渲染user_create.html


@app.route('/user/add/', methods=['POST'])          #将url path=/user/add的post请求交由add_user处理
@login_required
def add_user():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    age = request.form.get('age', '')

    #检查用户信息
    _is_ok, _error = user.validate_add_user(username, password, age)
    if _is_ok:
        user.add_user(username, password, age)      #检查ok，添加用户信息
        flash('增加用户成功')  
        return redirect(url_for('users'))                  #跳转到用户列表url_for
    else:
        #跳转到用户新建页面，回显错误信息&用户信息
        return render_template('user_create.html', \
                                error=_error, username=username, \
                                password=password, age=age)


@app.route('/user/modify/')                          #将url path=/user/modify/的歌特请求交由modify_user函数处理
@login_required
def modify_user():
    username = request.args.get('username', '')
    _user = user.get_user(username)
    _error = ''
    _username = ''
    _password = ''
    _age = ''
    if _user is None:
        _error = '用户信息不存在'
    else:
        _username = _user.get('username')
        _password = _user.get('password')
        _age = _user.get('age')

    return render_template('user_modify.html', error=_error, password=_password, age=_age, username=_username)

@app.route('/user/update/', methods=['POST'])           #将url path=/user/update/的post请求交由update_user函数处理
@login_required
def update_user():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    age = request.form.get('age', '')

    #检查用户信息
    _is_ok, _error = user.validate_update_user(username, password, age)
    if _is_ok:
        user.update_user(username, password, age)
        flash('修改用户信息成功')
        return redirect('/users/')
    else:
        return render_template('user_modify.html', error=_error, username=username, password=password, age=age)

@app.route('/user/delete/')
@login_required
def delete_user():
    username = request.args.get('username')
    user.delete_user(username)
    flash('删除用户信息成功')
    return redirect('/users/')

@app.route('/logout/')
@login_required
def logout():
    session.clear()
    print session
    return  redirect("/")



if __name__=='__main__':
    app.run(host='0.0.0.0',port=9001,debug=True,threaded=True)
