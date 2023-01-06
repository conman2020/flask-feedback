from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User
from forms import RegisterUserForm, LoginForm


app = Flask(__name__)
app.app_context().push()
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///flask_feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)

@app.route('/')
def home_page():
    return redirect("/register")




@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = RegisterUserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        # new_user = User.register(username, password,) Add in registration like video here to add encryption 
        new_user = User.register(username, password, email, first_name, last_name)

        db.session.add(new_user)
        try:
            db.session.commit()
            session['username'] = new_user.id
            flash('Welcome! Successfully Created Your Account!', "success")
            return redirect(f"/username/{new_user.id}")
        except IntegrityError:
            form.username.errors.append('Username taken.  Please pick another')
            return render_template('register.html', form=form)
    

    return render_template('register.html', form=form)
@app.route('/username/<username>', methods=["GET", "POST"])
def users_updated(username):
    """Show edit form for pet."""
    if "username" not in session or username != session['username']:
      return redirect("/")

    user = User.query.get(username)

    

    return render_template("/username/details.html", username=user)


@app.route("/logout")
def logout():
    """Logout route."""

    session.pop("username")
    return redirect("/")



@app.route("/login",methods=['GET', 'POST'] )
def login():
    """Logout route."""
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data


        user = User.login(username, password)  # <User> or False
        if user:
            session['username'] = user.id
            return redirect(f"/username/{user.id}")
        else:
            form.username.errors = ["Invalid username/password."]
            return render_template("login.html", form=form)

    return render_template("login.html", form=form)
    
@app.route("/secret")
def secret():
    """Logout route."""

    
    return render_template("secret.html")