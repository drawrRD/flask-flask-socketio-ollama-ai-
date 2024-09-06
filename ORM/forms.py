import wtforms
from wtforms.validators import Email, EqualTo
from ORM.models import User
from config.extends import redis



class RegisterForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message='邮箱格式不正确')])
    captcha = wtforms.StringField(validators=[wtforms.validators.Length(min=4, max=4, message='验证码格式不正确')])
    username = wtforms.StringField(validators=[wtforms.validators.Length(min=3, max=20, message='用户名格式不正确')])
    password = wtforms.StringField(validators=[wtforms.validators.Length(min=6, max=20, message='密码格式不正确')])
    password_confirm = wtforms.StringField(validators=[EqualTo("password", message='两次密码不一致！')])


    def validate_email(self, field):
        email = field.data
        user = User.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError(message="该邮箱已被注册！")


    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        captcha_bytes = redis.get(email)
        if captcha_bytes and (captcha_bytes.decode('utf-8') == captcha):
            pass
        else:
            raise wtforms.ValidationError(message="验证码错误！")


class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message='邮箱格式不正确')])
    password = wtforms.StringField(validators=[wtforms.validators.Length(min=6, max=20, message='密码格式不正确')])


class QuestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[wtforms.validators.Length(min=3, max=100, message='标题格式不正确')])
    content = wtforms.StringField(validators=[wtforms.validators.Length(min=3, max=10000, message='内容格式不正确')])


class AnswerForm(wtforms.Form):
    content = wtforms.StringField(validators=[wtforms.validators.Length(min=1, max=300, message='内容格式不正确')])
    question_id = wtforms.IntegerField(validators=[wtforms.validators.DataRequired(message='问题id必须传')])