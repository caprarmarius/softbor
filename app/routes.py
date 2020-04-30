from app import app, login_manager
from flask import render_template, request, redirect, jsonify, session
from flask_login import LoginManager, login_user, login_required, logout_user, fresh_login_required, current_user
from urllib.parse import urlparse, urljoin
from werkzeug.urls import url_parse
from flask_session import Session
from app.models import User, UserTask
from app.schemas import UserTaskSchema



user_task_schema = UserTaskSchema()
user_tasks_schema = UserTaskSchema(many = True)

sess = Session()

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc

#@app.route('/login', methods = ['POST'])
#def softbor_login():
 #   user = User.query.filter_by(username = 'user1')
  #  login_user(user, remember = True)
 #   if 'next' in session:
 #       next = session['next']
 #       if is_safe_url(next):
 #           return redirect(next)
 #  return 'User logged'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return "render_template('login.html', title='Sign In', form=form)"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return 'User registered'

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Logged out!'

#Homepage
@app.route('/') #executa functia pentru parametru URL
def index():
    return render_template('index.html') #returneaza templateu(pagina) index.html

#Create a task
@app.route('/tasks', methods=['POST'])
#@login_required
def create_task():
    task_title = request.json['title']
    task_content = request.json['content']
    new_task = UserTask(title=task_title, content=task_content)
    db.session.add(new_task)
    db.session.commit()
    #return redirect('/tasks')
    return user_task_schema.jsonify(new_task)

#Read all tasks
@app.route('/tasks', methods=['GET'])
#@login_required
def get_tasks():
    all_tasks = UserTask.query.order_by(UserTask.date_posted).all()    
    #return render_template('tasks.html', tasks=all_tasks)
    get_user_tasks = user_tasks_schema.dump(all_tasks)
    return jsonify(get_user_tasks)


#Read (get) a task
@app.route('/tasks/<int:id>', methods = ['GET'])
#@login_required
def get_a_task(id):
    task = UserTask.query.get_or_404(id)
    return user_task_schema.jsonify(task)

#Update (edit) Task
@app.route('/tasks/edit/<int:id>', methods=['PUT'])
#@login_required
def edit(id):
    task = UserTask.query.get_or_404(id)
    if not task.task_done:
        task.title = request.json['title']
        task.content = request.json['content']
        task.task_done = request.json['task_done']
        db.session.commit()
    return user_task_schema.jsonify(task)

#Delete Task
@app.route('/tasks/delete/<int:id>', methods=['DELETE'])
#@login_required
def delete(id):
    task = UserTask.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return 'Resource deleted'
   # return redirect('/tasks')