#encoding: utf-8
from  flask  import  Flask,request,render_template
import  user

app=Flask(__name__)

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
        return "登录成功"
    else:
        return render_template('login.html',username=username,error="username or password is error")
    print username
    print password
      
    return ''

if __name__=='__main__':
    app.run(host='0.0.0.0',port=9001,debug=True)
