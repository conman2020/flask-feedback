from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import RegisterUserForm, LoginForm, DeleteForm, FeedbackForm
from sqlalchemy.exc import IntegrityError
import os


app = Flask(__name__)
app.app_context().push()
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///flask_feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY', 'hellosecret')
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)

@app.route('/')
def home_page():
    return render_template("base.html")




@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if "id" in session:
        return redirect(f"/username/{session['id']}")

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
            session['id'] = new_user.id
            flash('Welcome! Successfully Created Your Account!', "success")
            return redirect(f"/username/{new_user.id}")
        except IntegrityError:
            form.username.errors.append('Username taken.  Please pick another')
            return render_template('register.html', form=form)
    

    return render_template('register.html', form=form)
@app.route('/username/<id>', methods=["GET", "POST"])
def users_updated(id):
    """Show edit form for pet."""
    if "id" not in session:
      return redirect("/")

    user = User.query.get(id)
    form=DeleteForm()

    

    return render_template("/username/details.html", user=user, form=form)


@app.route("/logout")
def logout():
    """Logout route."""

    session.pop("id")
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
            session['id'] = user.id
            return redirect(f"/username/{user.id}")
        else:
            form.username.errors = ["Invalid username/password."]
            return render_template("login.html", form=form)

    return render_template("login.html", form=form)
    
@app.route("/secret")
def secret():
    """Logout route."""

    
    return render_template("secret.html")




@app.route("/<username>/<id>/feedback/new",  methods=["GET", "POST"])
def new_feedback(username, id):
    """new feedback route."""
    if "id" not in session :
      return redirect("/")

    user = User.query.get(id)
    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(
            title=title,
            content=content,
            username=username,
        )

        db.session.add(feedback)
        db.session.commit()
        flash('Message added', "Post Added")

    
    return render_template("/feedback/new.html", form=form, user=user)




@app.route("/<username>/<id>/feedback/<feedback_id>/update", methods=["GET", "POST"])
def update_feedback(username, id, feedback_id):
    """Show update-feedback form and process it."""

    feedback = Feedback.query.get(feedback_id)

    if "id" not in session :
        raise Unauthorized()
    user = User.query.get(id)

    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()
    
   

    return render_template("/feedback/update.html", form=form, feedback=feedback, user=user)