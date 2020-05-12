from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from config import Config

app=Flask(__name__) #instantiaza o aplicatie Flask (cu parametru numele fisierului actual din __name__)
app.config.from_object(Config)


db = SQLAlchemy(app) #instantiem o referinta la o baza de date
migrate = Migrate(app, db)
ma = Marshmallow(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from app import routes, models

#verifica daca asta ii modulu principal si activeaza debuggingu (erorile is prezentate mai fain, poti face update la aplicatie fara sa restartezi serveru, etc.)
if __name__=="__main__":
    app.run(debug=True)