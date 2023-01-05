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
    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(password)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # return instance of user w/username and hashed pwd
        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)






# c2 = User(
#     username="chocolate",
#     password="small",
#     email="balllli@msn.com",
#     first_name="small",
#     last_name="big"
# )