from flask import Flask, render_template, request, jsonify, redirect, session, url_for
import psycopg2
from psycopg2 import Error

app = Flask(__name__)
app.secret_key = 'fashionme'

def connect_to_db():
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            host="fashionme-db",  # This should match the service name in Kubernetes
            database="fashionme_db",
            user="root",
            password="root"
        )
        return conn
    except Error as e:
        print("Error while connecting to PostgreSQL:", e)
        return None

@app.route('/')
def list_customers():
    access_token = session.get('access_token')
    if access_token:
        connection = connect_to_db()
        if connection:
            try:
                cur = connection.cursor()

                # Query to retrieve customer info and count of orders on each status
                cur.execute("""
                    SELECT 
                        c.customer_id,
                        c.customername,
                        c.email,
                        c.telephone,
                        c.account_created_date,
                        COUNT(CASE WHEN o.status_id = 1 THEN 1 END) AS pending_count,
                        COUNT(CASE WHEN o.status_id = 2 THEN 1 END) AS packed_count,
                        COUNT(CASE WHEN o.status_id = 3 THEN 1 END) AS dispatched_count,
                        COUNT(CASE WHEN o.status_id = 4 THEN 1 END) AS delivered_count,
                        COUNT(CASE WHEN o.status_id = 5 THEN 1 END) AS returned_count
                    FROM 
                        customers c
                    LEFT JOIN 
                        orders o ON c.customer_id = o.customer_id
                    GROUP BY 
                        c.customer_id
                """)

                # Fetch all rows
                customer_orders = cur.fetchall()
                return render_template('index.html', user_name=session['user_name'], user_email=session['user_email'], customers=customer_orders)

            except Error as e:
                print("Error while fetching data from PostgreSQL:", e)
                return render_template('error.html', message='Failed to fetch order details')

            finally:
                cur.close()
                connection.close()

        else:
            return jsonify({'error': 'Failed to connect to database'}), 500

    else:
        return redirect('/auth/admin')

# Function to Add a new customer
@app.route('/add', methods=['GET','POST'])
def add_customer():
    if request.method == 'POST':
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            try:
                # Extract customer data from the form
                customername = request.form['customername']
                password = request.form['password']
                email = request.form['email']
                telephone = request.form['telephone']  # Assuming telephone is provided in the form

                # Insert customer into the customers table
                cursor.execute("INSERT INTO customers (customername, password, email, telephone) VALUES (%s, %s, %s, %s) RETURNING customer_id", (customername, password, email, telephone))
                customer_id = cursor.fetchone()[0]
                
                # Commit the transaction
                connection.commit()
                return redirect(url_for('index', success='Customer added successfully',))
            except Error as error:
                print("Error while adding customer:", error)
                connection.rollback()
                return redirect(url_for('index', error='Failed to add customer')) 
            finally:
                cursor.close()
                connection.close()
        else:
            return jsonify({'error': 'Failed to connect to database'}), 500
    else:
        return render_template('add_edit_customer.html')  # Assuming you have a template for adding a new customer

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5004)

