import secrets
import smtplib
import pyrebase
from flask import *

config = { #config to connect app with firebase

#add ur config here as per registered web app on firebase
	
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
	s.login("","") #creds for our email 1st is for email and 2nd is for password
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




	










	

