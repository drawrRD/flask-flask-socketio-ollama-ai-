from flask import Flask, render_template, g, session
from werkzeug.exceptions import HTTPException

from config import settings
# from flaskwebgui import FlaskUI

from ORM.models import *
from practice01.views.authority import bp as au_bp
from practice01.views.qa import bp as qa_bp
from practice01.views.chatroom import bp as ct_bp

def create_app():
    app = Flask(__name__)
    # 服务器端配置为ProSetting， 本机测试为TestSetting
    app.config.from_object(settings.ProSettings)

    app.register_blueprint(au_bp)
    app.register_blueprint(qa_bp)
    app.register_blueprint(ct_bp)

    @app.before_request
    def before_request():
        user_id = session.get('user_id')
        if user_id:
            user = User.query.get(user_id)
            setattr(g, 'user', user)
        else:
            setattr(g, 'user', None)

    @app.context_processor
    def my_context_processor():
        return {'user': g.user}

    # 自定义错误页面
    @app.errorhandler(Exception)
    def handle_error(e):
        code = 500
        if isinstance(e, HTTPException):
            code = e.code
        return render_template('error.html', error_code=code), code

    @app.route('/')
    def index():
        questions = Question.query.order_by(Question.create_time.desc()).all()
        return render_template('index.html', questions=questions)

    return app
