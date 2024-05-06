from flask import Flask, render_template, request, jsonify, redirect, session, flash
import psycopg2
from psycopg2 import Error

app = Flask(__name__)
app.secret_key = 'fashionme'

# Function to establish connection to the PostgreSQL database
def connect_to_db():
    try:
        conn = psycopg2.connect(
            host="fashionme-db",  # Hostname of PostgreSQL service
            database="fashionme_db",
            user="root",
            password="root"
        )
        return conn
    except Error as e:
        print("Error while connecting to PostgreSQL:", e)
        return None

# Route to list customers and their orders
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
                    ORDER BY
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

# Route to add a new customer
@app.route('/add', methods=['GET', 'POST'])
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
                telephone = request.form['telephone']

                # Insert customer into the customers table
                cursor.execute("INSERT INTO customers (customername, password, email, telephone) VALUES (%s, %s, %s, %s) RETURNING customer_id", (customername, password, email, telephone))
                customer_id = cursor.fetchone()[0]
                
                # Commit the transaction
                connection.commit()
                flash("Customer "+str(customer_id)+" added successfully", "success")
                return redirect('/customer/')

            except Error as error:
                print("Error while adding customer:", error)
                connection.rollback()
                flash("Failed to add customer", "error")
                return redirect('/customer/')
            finally:
                cursor.close()
                connection.close()
        else:
            return jsonify({'error': 'Failed to connect to database'}), 500
    else:
        return render_template('add_edit_customer.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5004)
