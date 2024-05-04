from flask import Flask, request, jsonify, render_template, session, redirect
import psycopg2
from psycopg2 import Error

app = Flask(__name__)

app.secret_key = 'fashionme'

def connect_to_db():
    try:
        conn = psycopg2.connect(
            host="fashionme-db",
            database="fashionme_db",
            user="root",
            password="root"
        )
        return conn
    except Error as e:
        print("Error while connecting to PostgreSQL:", e)
        return None


def manage_orders(user_id):
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM orders WHERE user_id = %s", (user_id,))
            orders = cursor.fetchall()
            return orders
        except (Exception, Error) as error:
            print("Error while retrieving orders:", error)
        finally:
            cursor.close()
            connection.close()


def manage_cart(user_id):
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM carts WHERE user_id = %s", (user_id,))
            cart = cursor.fetchall()
            return cart
        except (Exception, Error) as error:
            print("Error while retrieving cart data:", error)
        finally:
            cursor.close()
            connection.close()


@app.route('/')
def index():

    access_token = session.get('access_token')  # Assuming you store user_id in session upon login
    
    if access_token:
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT id, username, email FROM users WHERE id = %s", (session['user_id'],))
                user_data = cursor.fetchone()
                if user_data:
           
                    orders = manage_orders(session['user_id'])
                    cart_list = manage_cart(session['user_id'])
                    return render_template('index.html', user_name=session['user_name'], user_email=session['user_email'], orders=orders, cart=cart_list)
                else:
                    return jsonify({"msg": "User not found"}), 404
            except (Exception, Error) as error:
                print("Error:", error)
                return jsonify({"msg": "Internal Server Error"}), 500
            finally:
                cursor.close()
                connection.close()
    else:
        return redirect('/auth/admin')  # Redirect to login page if user is not logged in



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
