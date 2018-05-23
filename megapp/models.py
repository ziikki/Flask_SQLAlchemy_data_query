from megapp import db #SQLAlchemy(app)
from datetime import datetime
from flask_login import UserMixin
from megapp import login
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    #posts = db.relationship('Post', backref='author', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return '<User {}>'.format(self.username)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
    
# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     body = db.Column(db.String(140))
#     timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

#     def __repr__(self):
#         return '<Post {}>'.format(self.body)

class CancerData(db.Model):
    __tablename__ = 'cancer_data'
    id = db.Column(db.Integer, primary_key=True)
    Class = db.Column(db.String(40))
    age = db.Column(db.String(10))
    menopause = db.Column(db.String(10))
    tumor_size = db.Column(db.String(10))
    inv_nodes = db.Column(db.String(10))
    node_caps = db.Column(db.String(10))
    deg_malig = db.Column(db.Integer)
    breast = db.Column(db.String(10))
    breast_quad = db.Column(db.String(10))
    irradiat = db.Column(db.String(10))

    
    def to_str(self):
        return '[Class]  {},  [age]  {},  [menopause]  {},  [tumor_size]  {},  [inv_nodes]  {},  [node_caps]  {},  [deg_malig]  {},  [breast]  {},  [breast_quad]  {},  [irradiat] {}'.format(self.Class, self.age, self.menopause, self.tumor_size, self.inv_nodes, self.node_caps, self.deg_malig, self.breast, self.breast_quad, self.irradiat)
    
    def __repr__(self):
        return '<EntryId {}>'.format(self.id)

