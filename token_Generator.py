import secrets
import smtplib
import pyrebase
from flask import *

config = { #config to connect app with firebase

 'apiKey': "AIzaSyAJGyOccVxQOoWGZvEdhU0vS_WtVBraN5E",
  'authDomain': "user-management-ad70b.firebaseapp.com",
  'databaseURL': "https://user-management-ad70b-default-rtdb.asia-southeast1.firebasedatabase.app",
  'projectId': "user-management-ad70b",
  'storageBucket': "user-management-ad70b.appspot.com",
  'messagingSenderId': "198158431364",
  'appId': "1:198158431364:web:0836c63b5f259a0b3b7ed1",
  'measurementId': "G-GK0B42QGS5"
	
}

app = Flask(__name__) #constructor of flask 


def token(): #generates 16bit token 
	return secrets.token_hex(8)

def email(): #manages smtp requests to send email with 16bit token
	Target = request.form["email"] # target's email
	temp = token() #adding token to temp file
	s = smtplib.SMTP('smtp.gmail.com',587) #sends request to gmail server 
	s.ehlo() #to ensure that server supports 
	s.starttls() #request for tls encryption to email with security
	s.login("techsnet111@gmail.com","salaryorshare?") #creds for our email
	msg = request.form["msg"] #msg you want to share along with token
	msg = msg  +" \n your 16 bit authentication code is :\n" + str(temp) #concating token wit msg
	s.sendmail("techsnet111@gmail.com",Target,msg) #sends email to target
	s.quit() #logout from server

	return temp #returns the token

fb = pyrebase.initialize_app(config) #initialising firebase database
db = fb.database() #accessing realtime database



@app.route('/') #homepage
def index():
	title = "token_generator"
	return render_template("token.html") #renders ui of web app


@app.route('/',methods=["POST"])
def sucess():
	temp = email() #calling email function and storing token in temp
	db.child("Tokens").push({"token":temp}) #adding token to realtime database under token node
	
	return render_template("done.html") #shows sucess page after email is sent and token is stored in database

app.run(debug="true") #app starts from here




	










	

