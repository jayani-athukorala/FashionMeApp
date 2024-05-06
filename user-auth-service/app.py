from flask import Flask, request, jsonify, render_template, redirect, session
from flask_jwt_extended import JWTManager, create_access_token 
import psycopg2
from psycopg2 import Error

app = Flask(__name__)
app.secret_key = 'fashionme'  # Secret key for session management
app.config['JWT_SECRET_KEY'] = 'fashionme'  # Secret key for JWT token
jwt = JWTManager(app)

# Function to establish connection to the PostgreSQL database
def connect_to_db():
    try:
        conn = psycopg2.connect(
            host="fashionme-db",  # Database host
            database="fashionme_db",
            user="root",
            password="root"
        )
        return conn
    except Error as e:
        print("Error while connecting to PostgreSQL:", e)
        return None

# Route for admin login
@app.route('/login', methods=['POST'])
def admin_login():
    data = request.form
    email = data.get('email')
    password = data.get('password')

    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            # Query to check if the provided credentials are valid for admin login
            cursor.execute("SELECT id, username, email FROM users WHERE email = %s AND password = %s AND role_id IN (SELECT id FROM user_roles WHERE role_name IN ('superadmin', 'admin', 'manager'))", (email, password))
            admin_id = cursor.fetchone()

            if admin_id:
                # If credentials are valid, create an access token and store user details in session
                access_token = create_access_token(identity=admin_id)
                session['access_token'] = access_token
                session['user_id'] = admin_id[0]  # Store user ID in session
                session['user_name'] = admin_id[1]  # Store user name in session
                session['user_email'] = admin_id[2]  # Store user email in session
                return redirect('/home')
            else:
                error_message = "Invalid email or password"
                return render_template('admin_login.html', error=error_message)
            
        except Error as error:
            print("Error while querying database:", error)
            return jsonify({"msg": "Internal Server Error"}), 500
    else:
        return jsonify({'error': 'Failed to connect to database'}), 500
        
# Route for admin logout
@app.route('/logout', methods=['GET'])
def admin_logout():
    session.clear()  # Clear session data
    return redirect('/auth/admin')  # Redirect to admin login page

# Route to render admin login form
@app.route('/admin', methods=['GET'])
def admin_login_form():
    return render_template('admin_login.html')  # Render admin login form

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)  # Run the Flask app

