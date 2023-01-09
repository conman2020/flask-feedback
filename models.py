from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()



def connect_db(app):
    db.app = app 
    db.init_app(app)

class User(db.Model):

    __tablename__="users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username= db.Column(db.String(50), nullable=False, unique=True)
    password= db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), 
                         nullable=False, 
                         unique=True)
    first_name = db.Column(db.String(30), 
                         nullable=False, 
                         unique=True)
    last_name = db.Column(db.String(30), 
                         nullable=False, 
                         unique=True)
    feedback = db.relationship("Feedback", backref="user", cascade="all,delete")
    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(password)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # return instance of user w/username and hashed pwd
        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)
    
    @classmethod
    def login(cls, username, password):
        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, password):
            # return user instance
            return u
        else:
            return False

class Feedback(db.Model):
    """Feedback."""

    __tablename__ = "feedbacks"

    feedback_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(
        db.String(20),
        db.ForeignKey('users.username'),
        nullable=False,
    )






# c2 = User(
#     username="chocolate",
#     password="small",
#     email="balllli@msn.com",
#     first_name="small",
#     last_name="big"
# )