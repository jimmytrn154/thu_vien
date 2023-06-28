from flask import Flask, render_template, request
import firebase_admin
from firebase_admin import credentials, db

app = Flask(__name__)

# Initialize Firebase app with service account credentials
cred = credentials.Certificate('C:\\Users\\Admin\\Documents\\Vital docs\\CODING\\PYTHON\\oke\\fb.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://v-thuvien-default-rtdb.asia-southeast1.firebasedatabase.app/m/'
})

# Define database reference, the name of database
db_ref = db.reference('users')

#register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        users = db_ref.get()

        for user_id in users:
            user_data = users[user_id]
            if user_data['email'] == email and user_data['password'] == password:
                return render_template('register.html', message='the account exists, try another email please')
            elif user_data['email'] == email and user_data['password'] != password:
                return render_template('register.html', message = 'the account exists, try another email please')
        #if none of the condition above fulfill, the below block will send user's info to the database    
        new_user_ref = db_ref.push()
        new_user_ref.set({
            'email': email,
            'password': password
        })    
        return render_template('xin-chao.html')           
    return render_template('register.html')            

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':

        mail = request.form['login_email']
        password = request.form['login_password']

        users = db_ref.get()

        for user_id in users:
            user_data = users[user_id]
            if user_data['email'] == mail and user_data['password'] == password:
                return render_template('trang-chu.html')
        
    return render_template('login.html')

#lounge route
@app.route('/')
def home():
    return render_template('xin-chao.html')

if __name__ == '__main__':
    app.run(debug=True)
