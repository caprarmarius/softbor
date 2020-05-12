from datetime import datetime
from flask_login import UserMixin
from app import db, login_manager




# Definirea modelelor(tabelelor) pe care le folosim in baza de date

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, index=True, unique=True)
    email = db.Column(db.String(120), nullable=False, index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(self.username + password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, self.username + password)
    
    def __repr__(self):
        return '<User {}>'.format(self.username)   

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(id))






class UserTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    task_done = db.Column(db.Boolean, nullable=False, default=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return 'User Task ' + str(self.id) + self.title
