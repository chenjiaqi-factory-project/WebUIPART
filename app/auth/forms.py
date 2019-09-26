from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, widgets
from wtforms.validators import DataRequired, EqualTo, Email


# Reset password form
class ResetPasswordForm(FlaskForm):
    new_password = PasswordField("Your new Password", validators=[DataRequired()])
    re_new_password = PasswordField(
        "Entry again", validators=[DataRequired(), EqualTo("new_password")]
    )
    submit = SubmitField("Reset")


# Reset password request form
class ResetPasswordRequestForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Request Password Reset")


# Register request form
class RegisterRequestForm(FlaskForm):
    submit = SubmitField("Click to Verify Your Email")


# Login form
class LoginForm(FlaskForm):
    email = StringField(
        "用户邮箱",
        validators=[DataRequired(), Email()],
        widget=widgets.TextInput(),
        render_kw={
            "class": "form-control",
            "placeholder": "请输入用户邮箱",
            "required": "",
            "autofocus": "",
        },
    )
    password = PasswordField(
        "密码",
        validators=[DataRequired()],
        widget=widgets.PasswordInput(),
        render_kw={
            "class": "form-control",
            "placeholder": "请输入密码",
            "required": "",
            "autofocus": "",
        },
    )
    captcha = StringField(
        "验证码",
        validators=[DataRequired()],
        render_kw={
            "class": "form-control",
            "placeholder": "请输入验证码",
            "required": "",
            "autofocus": "",
        },
    )
    submit = SubmitField("登陆")


# Register form
class RegisterForm(FlaskForm):
    email = StringField(
        "用户邮箱",
        validators=[DataRequired(), Email()],
        render_kw={
            "class": "form-control",
            "placeholder": "请输入邮箱地址",
            "required": "",
            "autofocus": "",
        },
    )
    nickname = StringField(
        "用户姓名",
        validators=[DataRequired()],
        render_kw={
            "class": "form-control",
            "placeholder": "请输入用户姓名",
            "required": "",
            "autofocus": "",
        },
    )
    password = PasswordField(
        "输入密码",
        validators=[DataRequired()],
        render_kw={
            "class": "form-control",
            "placeholder": "请输入密码",
            "required": "",
            "autofocus": "",
        },
    )
    re_password = PasswordField(
        "确认密码",
        validators=[DataRequired()],
        render_kw={
            "class": "form-control",
            "placeholder": "请再次确认密码",
            "required": "",
            "autofocus": "",
        },
    )
    account_status = SelectField(
        "账户类型",
        choices=[
            ("employee", "员工"),
            ("employer", "主管"),
        ],
        validators=[DataRequired()],
    )
    captcha = StringField(
        "验证码",
        validators=[DataRequired()],
        render_kw={
            "class": "form-control",
            "placeholder": "请输入四位验证码",
            "required": "",
            "autofocus": "",
        },
    )
    submit = SubmitField("创建新用户")

