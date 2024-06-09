import firebase_admin
from firebase_admin import credentials, auth, firestore
import os
from flask import Flask, request, jsonify, render_template, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'ssaaaaaaaadddddd'  # Replace with your own secret key

# Initialize Firebase Admin SDK
cred = credentials.Certificate('config/child-trauma-f268e-firebase-adminsdk-7an6d-40fe47f894.json')
firebase_admin.initialize_app(cred)

# Initialize Firestore DB
db = firestore.client()

@app.route('/')
def home():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup():
    full_name = request.form['full_name']
    email = request.form['email']
    id_number = request.form['id_number']
    country_code = request.form['country_code']
    phone_number = request.form['phone_number']
    password = request.form['password']

    try:
        user = auth.create_user(
            email=email,
            password=password,
            display_name=full_name,
        )
        # Add additional user information to Firestore
        db.collection('users').document(user.uid).set({
            'full_name': full_name,
            'email': email,
            'id_number': id_number,
            'country_code': country_code,
            'phone_number': phone_number
        })
        return jsonify({'success': True, 'message': 'Signup successful'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    try:
        user = auth.get_user_by_email(email)
        if not user:
            return jsonify({'success': False, 'message': 'Invalid email or password'}), 400

        # Verify password (Firebase Auth doesn't provide password verification directly)
        # Instead, you'd typically handle this on the client side with Firebase SDK
        user_record = auth.get_user(user.uid)
        if user_record:
            session['email'] = email
            return jsonify({'success': True, 'message': 'Login successful'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/predict', methods=['POST'])
def predict():
    if 'email' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401

    data = request.form.to_dict()

    # Process your prediction logic here

    return jsonify({'prediction': 'your_prediction'})

if __name__ == '__main__':
    app.run(debug=True)
