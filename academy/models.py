from datetime import datetime
from academy import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    user_type = db.Column(db.String(20), nullable = False)
    description = db.Column(db.String(500))
    items = db.relationship('Item', backref="item", lazy=True)

    def __repr__(self):
        return "User('{}', '{}', '{}')".format(self.username, self.email, self.user_type)

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    zip = db.Column(db.String(11), nullable=False)
    items = db.relationship('Item', backref='location', lazy=True)

    def __repr__(self):
        return "Location('{}', '{}')".format(self.name, self.city)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(30), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    startTime = db.Column(db.Time, nullable=False)
    endTime = db.Column(db.Time, nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "Item('{}', '{}', '{}')".format(self.name, self.category, self.location_id)

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(30), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "Skill('{}', '{}')".format(self.name, self.category)
class UserClass(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)

    def __repr__(self): 
        return "User {} attends Class {}".format(self.user_id, self.item_id)

# drcsb = Location(name="Desert Ridge: CSB", address="18850 N 56th St", city="Phoenix", state="AZ", zip="85050")
# dr1 = Location(name="Desert Ridge: OB1", address="18850 N 56th St", city="Phoenix", state="AZ", zip="85050")
# dr2 = Location(name="Desert Ridge: OB2", address="18850 N 56th St", city="Phoenix", state="AZ", zip="85050")
# trcn = Location(name="TRCN", address="19640 N 31st Ave", city="Phoenix", state="AZ", zip="85027")
# trcw = Location(name="TRCW", address="3202 W Behrend Dr", city="Phoenix", state="AZ", zip="85027")
# ny = Location(name="New York", address="200 Vesey St.", city="New York", state="NY", zip="10285")
# sr = Location(name="Sunrise", address="1500 NW 136th Ave", city="Sunrise", state="FL", zip="33323")