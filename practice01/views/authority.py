import random
import string
from io import BytesIO

import requests
from captcha.image import ImageCaptcha
from flask import Blueprint, render_template, request, jsonify, redirect, session, Response, send_file
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash
from config.extends import db, mail, redis
from ORM.models import User
from ORM.forms import RegisterForm, LoginForm

bp = Blueprint('authority', __name__, url_prefix='/')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')


    user_captcha = request.form.get('captcha')
    if user_captcha.lower() != session.get('captcha').lower():
        print('验证码错误')
        return redirect('/login')

    form = LoginForm(request.form)
    if form.validate():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                session['user_id'] = user.id
                return redirect('/')
            else:
                print('用户名或密码错误')
                return redirect('/login')
        else:
            print('用户不存在')
            return redirect('/login')
    else:
        print(form.errors)
        return redirect('/login')

@bp.route('/captcha/login')
def get_captcha():
    """生成随机的验证码字符串和对应的图像"""
    source = string.digits * 2
    captcha_text = ''.join(random.sample(source, 4))
    image = ImageCaptcha(width=160, height=55)
    captcha_image = image.generate_image(captcha_text)


    # 将图像数据保存到内存缓冲区
    buffer = BytesIO()
    captcha_image.save(buffer, format='PNG')
    buffer.seek(0)

    # 将验证码文本存入 session
    print(captcha_text)
    session['captcha'] = captcha_text
    return send_file(buffer, mimetype='image/jpeg')





@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            db.session.add(User(email=email, username=username, password=generate_password_hash(password, 'pbkdf2')))
            db.session.commit()
            return redirect('/login')
        else:
            print(form.errors)
            return redirect('/register')


@bp.route('/captcha/email', methods=['GET'])
def get_email_captcha():
    email = request.args.get('email')
    source = string.digits + string.ascii_lowercase
    captcha = ''.join(random.sample(source, 4))
    print('邮箱：', email)
    print('验证码：', captcha)
    message = Message(subject='论坛注册验证码', recipients=[email], body=f'您的验证码是：{captcha},将在5分钟后失效')
    mail.send(message)
    redis.set(email, captcha, ex=300)
    # RESTFUL API {code:200/400/500, message: '..', data:{}}
    return jsonify({'code': 200, 'msg': 'ok', 'data': None})


@bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')




@bp.route('/mail/test')
def mail_test():
    # message = Message(subject='邮箱测试', recipients=['*****@gmail.com'], body='这是一条测试邮件from flask-mail')
    # mail.send(message)
    return '邮件发送成功！'

@bp.route('/ollama/test')
def ollama_test():
    return render_template('ai-chat.html')

@bp.route('/ai/chat', methods=['GET', 'POST'])
def ai_chat():
    if request.method == 'GET':
        return render_template('ai-chat.html')
    else:
        # 从前端请求中获取数据
        data = request.get_json()

        # ollama API
        api_url = "http://localhost:11434/api/chat"
        api_data = {
            "model": "qwen2:7b",
            "messages": [
                {
                    "role": "user",
                    "content": data.get("message")
                }
            ],
            "stream": True
        }

        # 向实际API发送请求，并流式返回响应
        def generate_streamed_response():
            try:
                with requests.post(api_url, json=api_data, stream=True) as r:
                    # 检查响应是否成功
                    if r.status_code != 200:
                        error_message = f"Request failed with status code {r.status_code}"
                        yield f"Error: {error_message}\n"
                    else:
                        for line in r.iter_lines():
                            if line:
                                decoded_line = line.decode('utf-8')
                                yield f"{decoded_line}\n"
            except requests.exceptions.RequestException as e:
                # 处理网络问题或请求异常
                yield f"Error: Request failed due to an exception - {e}\n"

        # 返回流式响应
        return Response(generate_streamed_response(), content_type='application/json')
