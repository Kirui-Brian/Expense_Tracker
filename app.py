from flask import Flask
from flask_migrate import Migrate
from models import db
from routes import app as api

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(api)

if __name__ == '__main__':
    app.run(debug=True)