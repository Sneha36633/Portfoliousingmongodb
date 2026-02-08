from flask import Flask, render_template, request, redirect, flash
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = "secret_portfolio_key" 


client = MongoClient("mongodb+srv://snehagade76_db_user:6fikSamEtfFXfOAb@cluster0.woj4yte.mongodb.net/?appName=Cluster0")
db = client['portfolio_db']  

@app.route('/')
def index():
    
    user_data = db.about_me.find_one()
    
    if not user_data:
        user_data = {
            "name": "Aapka Naam",
            "degree": "B.Tech / Master",
            "experience": "Fresher",
            "email": "example@mail.com",
            "address": "City, India"
        }
    
    return render_template('index.html', data=user_data)

@app.route('/contact', methods=['POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')

        msg_doc = {
            "name": name,
            "email": email,
            "subject": subject,
            "message": message
        }
        
        db.contacts.insert_one(msg_doc)
        
        flash("Message successfully sent!")
        return redirect('/#contact')


def setup_db():
    if db.about_me.count_documents({}) == 0:
        db.about_me.insert_one({
            "name": "Sneha Gade",
            "degree": "Bachler In CSE",
            "phone": "8006757633",
            "email": "sgade5591@gmail.com",
            "address": "Bareilly, India",
            "birthday": "4 September 2005"
        })
        print("Initial data inserted!")

if __name__ == '__main__':
    app.run(debug=True)