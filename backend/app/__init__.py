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
    """
    Create and configure the Flask application.

    This function initializes the Flask application, configures MongoDB and login manager,
    and registers the application blueprints for different routes.
    
    Returns:
        app (Flask): The initialized Flask application instance.
    """

    load_dotenv()

    #initialize the Flask app with custom template and static folder paths
    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(__file__), "../templates"),
        static_folder=os.path.join(os.path.dirname(__file__), "../static")
    )

    #set up MongoDB connection URI and secret key from environment variables
    app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/barbuddy")
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    connection = pymongo.MongoClient(app.config["MONGO_URI"])
    db = connection.get_database("barbuddy")
    mongo.init_app(app)

    #register application blueprints for different routes
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

    #initialize login manager for user authentication
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        """
        Load the user from the database by user ID for authentication.

        Args:
            user_id (str): The ID of the user to be loaded.

        Returns:
            User: A user instance if found, or None if no user matches the given ID.
        """

        user = db.User.find_one({'_id': ObjectId(user_id)})
        if user:
            return User(user)
        return None

    #user class for handling user session and authentication
    class User(UserMixin):
        """
        User class to represent a user in the application.

        Inherits from `UserMixin` for Flask-Login integration.

        Attributes:
            id (str): The unique identifier for the user (MongoDB ObjectId).
            name (str): The name of the user.
            username (str): The username of the user.
            password (str): The hashed password of the user.
        """

        def __init__(self, user):
            self.id = str(user['_id'])
            self.name = user['name']
            self.username = user['username']
            self.password = user['password']

    #registration form for user sign-up
    class RegistrationForm(FlaskForm):
        """
        Form class for user registration.

        Attributes:
            name (StringField): Name of the user.
            username (StringField): Username for login.
            password (PasswordField): Password for the user.
        """

        name = StringField('Name', validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Name"})
        username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
        password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
        submit = SubmitField('Register')

        def validate_username(self, username1):
            """
            Custom validation for username to ensure it is unique.

            Args:
                username1 (StringField): The username inputted by the user.
            """

            user = db.User.find_one({
                'username': username1.data
            })

            if user:
                raise ValidationError('Username already exists')
    
    #login form for user sign-in
    class LoginForm(FlaskForm):
        """
        Form class for user login.

        Attributes:
            username (StringField): Username of the user for login.
            password (PasswordField): Password of the user for login.
        """

        username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
        password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
        submit = SubmitField('Login')

    #routes for registration, login, logout, and user dashboard
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        """
        Route for user registration page and handling the registration process.

        GET: Display the registration form.
        POST: Handle form submission, register the user, and log them in.
        """

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
        """
        Route for user login page and handling the login process.

        GET: Display the login form.
        POST: Handle form submission, authenticate the user, and log them in.
        """

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
        """
        Route for logging out the user and redirecting them to the dashboard.

        The user must be logged in to access this route.
        """

        logout_user()
        return redirect(url_for('dashboard'))


    @app.route("/")
    def dashboard():
        """
        Route for displaying the main dashboard page.

        GET: Show the user dashboard.
        """

        return render_template("index.html")

    @app.route("/inventory")
    def inventory_page():
        """
        Route for displaying the inventory page.

        If the user is authenticated, show the inventory page.
        Otherwise, show a "not logged in" page.
        """

        if current_user.is_authenticated:
            return render_template("inventory.html")
        else:
            return render_template("not_logged_in.html")

    @app.route("/suggestions")
    def suggestions_page():
        """
        Route for displaying the suggestions page.

        If the user is authenticated, show the suggestions page.
        Otherwise, show a "not logged in" page.
        """

        if current_user.is_authenticated:
            return render_template("suggestions.html")
        else:
            return render_template("not_logged_in.html")

    @app.route("/alerts")
    def alerts_page():
        """
        Route for displaying the alerts page.

        If the user is authenticated, show the alerts page.
        Otherwise, show a "not logged in" page.
        """

        if current_user.is_authenticated:
            return render_template("alerts.html")
        else:
            return render_template("not_logged_in.html")
    
    @app.route("/askai")
    def ask_ai_page():
        """
        Route for displaying the "ask AI" page.
        """

        return render_template("ask_ai.html")
    
    @app.route("/favorites")
    def favorites_page():
        """
        Route for displaying the favorites page.

        If the user is authenticated, show the favorites page.
        Otherwise, show a "not logged in" page.
        """
        
        if current_user.is_authenticated:
            return render_template("favorites.html")
        else:
            return render_template("not_logged_in.html")

    return app
