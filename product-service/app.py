from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import psycopg2
import os
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

# Get all products
@app.route('/')
def list_products():
    access_token = session.get('access_token')
    if access_token:
        connection = connect_to_db()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("""
                        SELECT p.product_id, p.name AS product_name, pc.name AS category_name, p.description, p.price, pi.image_url
                        FROM products p
                        JOIN product_categories pc ON p.category_id = pc.category_id
                        JOIN product_images pi ON p.product_id = pi.product_id
                    """)
                products = cursor.fetchall()
                product_list = []
                for product in products:
                    product_list.append({
                        'id': product[0],
                        'name': product[1],
                        'category': product[2],
                        'description': product[3],
                        'price': float(product[4]),
                        'image': product[5]
                    })
                return render_template('index.html', user_name=session['user_name'], user_email=session['user_email'], products=product_list, active_tab='products')
            except Error as e:
                print("Error while retrieving products:", e)
                return None
        else:
            return jsonify({'error': 'Failed to connect to database'}), 500
    else:
        return redirect('/auth/admin')

def get_product(product_id):
    # Retrieve product information from the database
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                SELECT p.product_id, p.name, p.description, p.price, pi.image_url
                FROM products p
                JOIN product_images pi ON p.product_id = pi.product_id
                WHERE p.product_id = %s
            """, (product_id,))
            product = cursor.fetchone()
            if product:
                return product
            else:
                return None
        except (Exception, Error) as error:
            print("Error while retrieving product:", error)
            return None
        finally:
            cursor.close()
            connection.close()


def get_categories():
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT category_id, name FROM product_categories")
            category_list = cursor.fetchall()
            categories = []
            for category in category_list:
                categories.append({
                    'category_id': category[0],
                    'name': category[1]
                })

            return categories
        except Error as error:
            print("Error while fetching categories:", error)
            return []
        finally:
            cursor.close()
            connection.close()
    else:
        return []
    

@app.route('/add', methods=['GET','POST'])
def add_product():
    if request.method == 'POST':
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            try:
                # Extract product data from the form
                name = request.form['name']
                price = request.form['price']
                description = request.form['description']
                category_id = request.form['category']  # Assuming category_id is provided in the form
                image = request.files['image']
                                
                # Insert product into the products table
                cursor.execute("INSERT INTO products (name, category_id, description, price) VALUES (%s, %s, %s, %s) RETURNING product_id", (name, category_id, description, price))
                product_id = cursor.fetchone()[0]

                directory = '/product/static/images/'
                os.chmod(directory, 0o755)  # Set directory permissions to allow writing
                image_path = os.path.join(directory, 'image' + str(product_id) + '.jpg')
                image.save(image_path)

                image_url = 'image' + str(product_id) + '.jpg'
                cursor.execute("INSERT INTO product_images (product_id, image_url) VALUES (%s, %s)", (product_id, image_url))
                
                connection.commit()
                return redirect(url_for('index', success='Product added successfully'))
            except Error as error:
                print("Error while creating product:", error)
                connection.rollback()
                return redirect(url_for('index', error='Failed to create product'))
            finally:
                cursor.close()
                connection.close()
        else:
            return jsonify({'error': 'Failed to connect to database'}), 500
    else:
        categories = get_categories()
        return render_template('add_edit_product.html', categories=categories)

# Create a new product
@app.route('/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    if request.method == 'POST':
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            try:
                # Extract product data from the form
                name = request.form['name']
                price = request.form['price']
                description = request.form['description']
                category_id = request.form['category']  # Assuming category_id is provided in the form
                
                # Update product in the products table
                cursor.execute("UPDATE products SET name = %s, category_id = %s, description = %s, price = %s WHERE product_id = %s", (name, category_id, description, price, product_id))
                
                # Update product image in the product_images table
                # Assuming image_url is provided in the form, adjust accordingly if you are handling file uploads
                image_url = request.form['image_url']
                cursor.execute("UPDATE product_images SET image_url = %s WHERE product_id = %s", (image_url, product_id))
                
                connection.commit()
                return redirect(url_for('index', success='Product updated successfully'))
            except Error as error:
                print("Error while updating product:", error)
                connection.rollback()
                return redirect(url_for('index', error='Failed to update product'))
            finally:
                cursor.close()
                connection.close()
        else:
            return jsonify({'error': 'Failed to connect to database'}), 500
    else:
        product_data = get_product(product_id)
        if product_data:
            # Fetch product categories to populate the dropdown in the form
            categories = get_categories()
            return render_template('add_edit_product.html', product=product_data, categories=categories)
        else:
            return "Product not found", 404



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)