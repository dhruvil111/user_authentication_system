import pyrebase
from flask import *


config = { #config files to connect with firebase
	
	#add your firebase config of app registered on firebase here
}

fb = pyrebase.initialize_app(config) #initializing database
db = fb.database() #accessing realtime database

		

app = Flask(__name__) # flask constructor



@app.route('/') #homepage
def home():

	title = "login_page"
	return render_template("login.html") #displays homepage

@app.route('/',methods=["GET","POST"])
def register(): #function of app after user press register / login button to submit details

	if request.form['btn'] == "rr": # if user press register (submit button of form not the slider showed on top)


		if request.form['cb'] == "check": #if checkbox is checked

			rusername = request.form['rusername'] #taking values from form to local variables
			rpassword = request.form['rpassword']
			remail    = request.form['remail']
			rtoken    = request.form['rtoken']

			tk = db.child("Tokens").get() # accessing Token node from db 

			for i in tk.each(): #traversing each child of Token node
				if  i.val()["token"] == rtoken: #comparing token values
					db.child("lecturer-user").push({"password":rpassword,"username":rusername,"email":remail})
					#if token matches then register user to lecturer-user node 
					return render_template("success_login.html") #renders success page to show registration was sucessfull
			else:
				return render_template("error.html") #render error page if user is not registered

		#if checkbox is unchecked			
		rusername = request.form['rusername'] #adding values from form to local variable
		rpassword = request.form['rpassword']
		remail    = request.form['remail']

		db.child("users").push({"password":rpassword,"username":rusername,"email":remail})
		#pushing data of new user to user node

		return render_template("success_registered.html") #renders sucess page to show registration has been done sucessfully

	elif request.form['btn'] == "ll": #if user press login button (submit button of form not the slider showed on top)
	
		lusername = request.form['lusername'] #taking values from form to local variables
		lpassword = request.form['lpassword']

		users = db.child("users").get() #acessing users node of db

		for i in users.each(): #traversing each child of user node
			if i.val()["username"] == lusername and i.val()["password"] == lpassword : #if credentials matches
				return render_template("success_login.html") #user sucessfully loged in
		else:

			lu    = db.child("lecturer-user").get() #acessing lecturer-user node

			for j in lu.each(): # acessing lecturer-user node

				if j.val()["username"] == lusername and j.val()["password"] == lpassword: #if creds matches
					return render_template("success_login.html") #user logged in
					
				else:
					return render_template("error.html") #error! user not found!



			
	

	


		

app.run(debug="true") #app starts from here with debug mode
	

