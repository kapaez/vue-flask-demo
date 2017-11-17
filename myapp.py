# -*- coding: utf-8 -*-
from flask import Flask,render_template,redirect,url_for, flash, jsonify
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, \
    SelectField,validators
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from wtforms import ValidationError
from flask_login import LoginManager, UserMixin, current_user, login_required, \
    login_user, logout_user
# 创建app实例
app = Flask(__name__)
#实例相关变量命名空间
login_manager = LoginManager()
db = SQLAlchemy(app)
login_manager.login_view = 'login'
Bootstrap(app)
login_manager.init_app(app)

#数据库
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    username = db.Column(db.String(64))
    view_total = db.Column(db.Integer)
    password = db.Column(db.String(64))
    view_arrive = db.Column(db.Integer)
    register_nums = db.Column(db.Integer)
    table_nums = db.Column(db.Integer)
    employee = db.Column(db.Integer)
    groups = db.Column(db.Integer)

#连接数据库
app.config['SQLALCHEMY_DATABASE_URI'] = \
    "mysql://root:root123@172.17.0.2:3306/flask"
app.config['SECRET_KEY'] = 'nidaye!'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#html表单
class TestForm(FlaskForm):
    name = StringField(u'真实姓名', validators=[Required()])
    password = PasswordField(u'密码', validators=[Required()])
    username = StringField(u'用户名', validators=[Required()])
    view_total = StringField(u'浏览量', validators=[Required()])
    view_arrive = StringField(u'到店量', validators=[Required()])
    register_nums = StringField(u'打卡量', validators=[Required()])
    table_nums = StringField(u'报名量', validators=[Required()])
    employee = StringField(u'员工', validators=[Required()])
    groups = StringField(u'小组', validators=[Required()])
    submit = SubmitField(u'提交')

#登录表单
class LoginForm(FlaskForm):
    name = StringField(u'名字', validators=[Required()])
    password = PasswordField(u'密码', validators=[Required()])
    submit = SubmitField(u'登录')
#flask_login所需的自定义回调函数
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#自定义路由
@app.route('/test', methods=['GET','POST'])
def test():
    form = TestForm()
    if form.validate_on_submit():
       user = User()
       user.name = form.name.data
       user.password = form.password.data
       user.username = form.username.data
       user.view_total = form.view_total.data
       user.view_arrive = form.view_arrive.data
       user.register_nums = form.register_nums.data
       user.table_nums = form.table_nums.data
       user.employee = form.employee.data
       user.groups = form.groups.data
       db.session.add(user)
       db.session.commit()
       return redirect(url_for('test'))
    return render_template('test.html', form=form)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form =  LoginForm()
    if form.validate_on_submit():
        user_in = User.query.filter_by(name=form.name.data).first()
        if user_in is not None and user_in.password==form.password.data:
            print 'ok'
            login_user(user_in, True)
            return redirect(url_for('manage'))
        flash(u'用户名或密码错误，请重新登录')
    return render_template('login.html',form=form)

@app.route('/api/<username>')
def api(username):
    user = User.query.filter_by(username=username).first()
    msg = {'stat':"suc",
           "data":[{
            'name' : user.name,
            'username': user.username
        }]
           }
    return jsonify({'msg':msg}), 200

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('test'))


@app.route('/manage')
@login_required
def manage():
    return render_template('manage.html')

if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0')
