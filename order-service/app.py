from flask import Flask, render_template, request, jsonify, redirect, session, flash
import psycopg2
from psycopg2 import Error

app = Flask(__name__)
app.secret_key = 'fashionme'

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

# Render index.html
@app.route('/')
def list_orders():
    access_token = session.get('access_token')
    if access_token:
        connection = connect_to_db()
        if connection:
            try:
                cur = connection.cursor()

                # Query to retrieve order details for the given customer including product and customer info
                cur.execute("""
                    SELECT 
                        o.order_id,
                        o.order_date,
                        o.status_id,
                        os.status_name,
                        c.customername,
                        c.email,
                        p.name as product_name,
                        pc.name as product_category
                    FROM 
                        orders o
                    JOIN
                        order_status os ON o.status_id = os.status_id
                    JOIN 
                        customers c ON o.customer_id = c.customer_id
                    JOIN 
                        order_items oi ON o.order_id = oi.order_id
                    JOIN 
                        products p ON oi.product_id = p.product_id
                    JOIN 
                        product_categories pc ON p.category_id = pc.category_id
                """)
                
                # Fetch all rows
                orders = cur.fetchall()
                order_status = get_order_status()
                return render_template('index.html', user_name=session['user_name'], user_email=session['user_email'], orders=orders, order_status=order_status, active_tab='orders')

            except Error as e:
                print("Error while fetching data from PostgreSQL:", e)
                return render_template('error.html', message='Failed to fetch order details')
        else:
            return jsonify({'error': 'Failed to connect to database'}), 500
    else:
        return redirect('/auth/admin')

# Function to fetch order status from the database
def get_order_status():
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM order_status")
            categories = cursor.fetchall()
            status_list = []
            for status in categories:
                status_list.append({
                    'status_id': status[0],
                    'status_name': status[1]
                })
            return status_list
        except Error as error:
            print("Error while fetching order status:", error)
            return []
        finally:
            cursor.close()
            connection.close()
    else:
        return []

# Update Order Status
@app.route('/status', methods=['POST'])
def update_order_status():
    # Retrieve the selected status from the form data
    selected_status_id = request.form.get('order_status')
    order_id = request.form.get('order_id')

    # Update the order status in the database
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("UPDATE orders SET status_id = %s WHERE order_id = %s", (selected_status_id, order_id))
            connection.commit()
            
            flash("Order "+order_id+" status updated successfully", "success")
            return redirect('/order/')
        except Error as error:
            print("Error while updating order status:", error)
            connection.rollback()
            return "Failed to update order status", 500
        finally:
            cursor.close()
            connection.close()
    else:
        return "Failed to connect to the database", 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5005)