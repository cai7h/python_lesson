from flask import Flask
from flask import request
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    """主页
    ---
    get:
        description: 返回主页
        responses:
            200:
                description: 成功
    post:
        description: 不支持的 POST 请求
        responses:
            200:
                description: 不支持的 POST 请求
    """
    return '<h1>Home</h1>'

@app.route('/signin', methods=['GET'])
def signin_form():
    """登录表单
    ---
    get:
        description: 返回登录表单
        responses:
            200:
                description: 成功
    """
    return '''<form action="/signin" method="post">
              <p><input name="username"></p>
              <p><input name="password" type="password"></p>
              <p><button type="submit">Sign In</button></p>
              </form>'''

@app.route('/signin', methods=['POST'])
def signin():
    """登录验证
    ---
    post:
        description: 验证用户名和密码
        parameters:
            - in: formData
              name: username
              type: string
              required: true
              description: 用户名
            - in: formData
              name: password
              type: string
              required: true
              description: 密码
        responses:
            200:
                description: 登录成功或失败
    """
    # 需要从request对象读取表单内容：
    if request.form['username'] == 'admin' and request.form['password'] == 'password':
        return '<h3>Hello, admin!</h3>'
    return '<h3>Bad username or password.</h3>'

if __name__ == '__main__':
    app.run(debug=True)