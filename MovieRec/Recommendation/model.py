#The file links the website responses to the offline Database. These can be used by other templates. 
#It also runs queries to retrieve the user ids, usernames, as well as passwords of the users to be able to run other scripts smoothly
#The model defines the parameters of different fields in all the forms used in this website.

from msilib.schema import Property
from Recommendation import db, login_manager
from Recommendation import bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
   return user.query.get(int(user_id))

class user(UserMixin, db.Model):
   id = db.Column(db.Integer(), primary_key=True)
   username = db.Column(db.String(length=30),unique=True, nullable=False)
   email_address = db.Column(db.String(length=50),unique=True, nullable=False)
   password_hash = db.Column(db.String(length=60),nullable=False)
  
   def get_pwd(self):
      return self.password_hash
   @property
   def password(self):
      return self.password

   @password.setter
   def password(self, plain_text_password):
      self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')


   def check_password_correction(self, attempted_password):
      return bcrypt.check_password_hash(self.password_hash, attempted_password)
      
 

