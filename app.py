from flask import Flask, request, render_template, redirect
import mysql.connector
from mysql.connector import Error
import openai
from flask import Flask, request, jsonify

# Flask app initialization
app = Flask(__name__)

# Set your OpenAI API key here
openai.api_key = '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'

# Database configuration
db_config = {
    'host': 'localhost',
    'database': 'userregistration',
    'user': 'root',
    'password': 'Faiz@0502'
}

# Function to connect to the MySQL database
def connect_to_database(config):
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

# Route to serve the signup page and handle signup functionality
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        connection = connect_to_database(db_config)
        if connection:
            email = request.form.get('email')
            phone = request.form.get('phone')
            password = request.form.get('password')

            query = "INSERT INTO users (email, phone, password) VALUES (%s, %s, %s)"
            cursor = connection.cursor()
            cursor.execute(query, (email, phone, password))
            connection.commit()
            cursor.close()
            connection.close()
            return "Signup successful"
        else:
            return "Database connection error"
    return render_template('signup.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json['text']
    
    # Structure the payload as in your .NET application
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message}
        ],
        "max_tokens": 150
    }

    try:
        openai_response = openai.ChatCompletion.create(**payload)
        response_text = openai_response['choices'][0]['message']['content'].strip()
        return jsonify({'text': response_text})
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'text': "Sorry, I couldn't process that message."})

    
# Route to serve the login page and handle login functionality
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        connection = connect_to_database(db_config)
        if connection:
            email = request.form.get('email')  # Match the 'name' attribute in the HTML form
            password = request.form.get('password')  # Match the 'name' attribute in the HTML form

            query = "SELECT * FROM users WHERE email = %s AND password = %s"
            cursor = connection.cursor()
            cursor.execute(query, (email, password))
            user = cursor.fetchone()
            cursor.close()
            connection.close()

            if user:
                return render_template('index.html')  # Redirect to index.html upon successful login
            else:
                return "Invalid credentials"
        else:
            return "Database connection error"
    return render_template('login.html')

# Add a route for signout
@app.route('/signout')
def signout():
    # You can add any session cleanup or other signout logic here if needed
    return redirect('/login')
# Route to serve the forgot password page and handle password reset functionality
@app.route('/forgotpassword', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        connection = connect_to_database(db_config)
        if connection:
            email = request.form.get('email')
            phone = request.form.get('phone')
            new_password = request.form.get('new_password')

            query = "UPDATE users SET password = %s WHERE email = %s AND phone = %s"
            cursor = connection.cursor()
            cursor.execute(query, (new_password, email, phone))
            updated_rows = cursor.rowcount
            connection.commit()
            cursor.close()
            connection.close()

            if updated_rows:
                return "Password updated successfully"
            else:
                return "User not found or incorrect details"
        else:
            return "Database connection error"
    return render_template('forgotpassword.html')

    app.run(debug=True)
# Placeholder code to run the Flask app
if __name__ == '__main__':
    app.run(debug=True) 
