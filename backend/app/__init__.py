import os
from flask import Flask, render_template, redirect, url_for, flash, jsonify
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import pymongo
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from wtforms import StringField, PasswordField, SubmitField
from flask_wtf import FlaskForm
from bson.objectid import ObjectId
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash

mongo = PyMongo()

def create_app():
    load_dotenv()

    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(__file__), "../templates"),
        static_folder=os.path.join(os.path.dirname(__file__), "../static")
    )

    app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/barbuddy")
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    connection = pymongo.MongoClient(app.config["MONGO_URI"])
    db = connection.get_database("barbuddy")
    mongo.init_app(app)

    from .routes.inventory import inventory_bp
    from .routes.suggest import suggest_bp
    from .routes.alert import alert_bp
    from .routes.ai_suggest import ai_bp
    from .routes.favorites import favorites_bp
    app.register_blueprint(favorites_bp, url_prefix="/api/favorites")
    app.register_blueprint(ai_bp, url_prefix="/api/ai")
    app.register_blueprint(inventory_bp, url_prefix="/api/inventory")
    app.register_blueprint(suggest_bp, url_prefix="/api/suggestions")
    app.register_blueprint(alert_bp, url_prefix="/api/alerts")

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        user = db.User.find_one({'_id': ObjectId(user_id)})
        if user:
            return User(user)
        return None


    class User(UserMixin):
        def __init__(self, user):
            self.id = str(user['_id'])
            self.name = user['name']
            self.username = user['username']
            self.password = user['password']

    class RegistrationForm(FlaskForm):
        name = StringField('Name', validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Name"})
        username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
        password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
        submit = SubmitField('Register')

        def validate_username(self, username1):
            user = db.User.find_one({
                'username': username1.data
        })

            if user:
                raise ValidationError('Username already exists')
        
    class LoginForm(FlaskForm):
        username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
        password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
        submit = SubmitField('Login')


    @app.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegistrationForm()

        if form.validate_on_submit():
            form.validate_username(form.username)
            hashed_password = Bcrypt().generate_password_hash(form.password.data)

            user = {
                'name': form.name.data,
                'username': form.username.data,
                'password': hashed_password
            }

            db.User.insert_one(user)
            login_user(User(user))
            return redirect(url_for('dashboard'))
        return render_template('registration.html', form=form)
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            user = db.User.find_one({'username': form.username.data})

            if user and Bcrypt().check_password_hash(user['password'], form.password.data):
                login_user(User(user))
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid username or password', 'danger')

        return render_template('login.html', form=form)


    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('dashboard'))


    @app.route("/")
    def dashboard():
        return render_template("index.html")

    @app.route("/inventory")
    def inventory_page():
        if current_user.is_authenticated:
            return render_template("inventory.html")
        else:
            return render_template("not_logged_in.html")

    @app.route("/suggestions")
    def suggestions_page():
        if current_user.is_authenticated:
            return render_template("suggestions.html")
        else:
            return render_template("not_logged_in.html")

    @app.route("/alerts")
    def alerts_page():
        if current_user.is_authenticated:
            return render_template("alerts.html")
        else:
            return render_template("not_logged_in.html")
    
    @app.route("/askai")
    def ask_ai_page():
        return render_template("ask_ai.html")
    
    @app.route("/favorites")
    def favorites_page():
        if current_user.is_authenticated:
            return render_template("favorites.html")
        else:
            return render_template("not_logged_in.html")

    return app
