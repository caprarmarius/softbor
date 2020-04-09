from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__) #instantiaza o aplicatie Flask (cu parametru numele fisierului actual din __name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usertasks.db'
db = SQLAlchemy(app) #creem baza de date

class UserTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    task_done = db.Column(db.Integer, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    def __repr__(self):
        return 'User Task ' + str(self.id) + self.title


#Homepage
@app.route('/') #executa functia pentru parametru URL
def index():
    return render_template('index.html') #returneaza templateu(pagina) index.html

#User tasks
@app.route('/tasks', methods=['GET','POST'])
def tasks():

    if request.method == 'POST':
        task_title = request.form['title']
        task_content = request.form['content']
        task_done = 0
        new_task = UserTask(title=task_title, content=task_content, task_done = task_done)
        db.session.add(new_task)
        db.session.commit()
        return redirect('/tasks')
    else:
        all_tasks = UserTask.query.order_by(UserTask.date_posted).all()    
        return render_template('tasks.html', tasks=all_tasks)


#Task done
@app.route('/tasks/done/<int:id>')
def done(id):
    task = UserTask.query.get_or_404(id)
    task.task_done = 1
    db.session.commit()
    return redirect('/tasks')

#Delete Task
@app.route('/tasks/delete/<int:id>')
def delete(id):
    task = UserTask.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect('/tasks')

#Edit Task
@app.route('/tasks/edit/<int:id>', methods=['GET','POST'])
def edit(id):
    task = UserTask.query.get_or_404(id)
    if request.method == 'POST':
        task.title = request.form['title']
        task.content = request.form['content']
        db.session.commit()
        return redirect('/tasks')
    else:
        return render_template('edit.html', task=task)


#verifica daca asta ii modulu principal si activeaza debuggingu (erorile is prezentate mai fain, poti face update la aplicatie fara sa restartezi serveru, etc.)
if __name__=="__main__":
    app.run(debug=True)