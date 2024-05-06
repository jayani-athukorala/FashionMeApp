from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
import psycopg2
import os
from psycopg2 import Error

app = Flask(__name__)

app.secret_key = 'fashionme'

# Function to connect to the PostgreSQL database
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

# Function to retrieve all products
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

# Function to retrieve product information by ID
def get_product(product_id):
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                SELECT p.product_id, p.name, p.category_id, p.description, p.price, pi.image_url
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

# Function to retrieve all product categories
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

# Route to add a new product
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
                category_id = request.form['category']
                image = request.files['image']
                
                # Insert product into the products table
                cursor.execute("INSERT INTO products (name, category_id, description, price) VALUES (%s, %s, %s, %s) RETURNING product_id", (name, category_id, description, price))
                product_id = cursor.fetchone()[0]

                # Save product image
                directory = '/product/static/images/'
                os.makedirs(directory, exist_ok=True)
                os.chmod(directory, 0o755)  # Set directory permissions to allow writing
                image_path = os.path.join(directory, 'image' + str(product_id) + '.jpg')
                image.save(image_path)

                image_url = 'image' + str(product_id) + '.jpg'
                cursor.execute("INSERT INTO product_images (product_id, image_url) VALUES (%s, %s)", (product_id, image_url))
                
                connection.commit()
                flash("Product "+str(product_id)+" added successfully", "success")
                return redirect('/product/')
            except Error as error:
                print("Error while creating product:", error)
                connection.rollback()
                flash("Failed to add product", "error")
                return redirect(url_for('add_product'))
            finally:
                cursor.close()
                connection.close()
        else:
            return jsonify({'error': 'Failed to connect to database'}), 500
    else:
        categories = get_categories()
        return render_template('add_edit_product.html', categories=categories)

# Route to edit an existing product
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
                category_id = request.form['category']                 
                # Update product in the products table
                cursor.execute("UPDATE products SET name = %s, category_id = %s, description = %s, price = %s WHERE product_id = %s", (name, category_id, description, price, product_id))
                
                # Update product image in the product_images table
                image_url = request.form['image_url']
                cursor.execute("UPDATE product_images SET image_url = %s WHERE product_id = %s", (image_url, product_id))
                
                connection.commit()
                flash("Product updated successfully", "success")
                return redirect('/product/')
            except Error as error:
                print("Error while updating product:", error)
                connection.rollback()
                flash("Failed to update product", "error")
                return redirect(url_for('edit_product', product_id=product_id))
            finally:
                cursor.close()
                connection.close()
        else:
            return jsonify({'error': 'Failed to connect to database'}), 500
    else:
        product_data = get_product(product_id)
        
        if product_data:
            product = {
                'id': product_data[0],
                'name': product_data[1],
                'category_id': product_data[2],
                'description': product_data[3],
                'price': float(product_data[4]),
                'image_url': product_data[5]
            }
            # Fetch product categories to populate the dropdown in the form
            categories = get_categories()
            return render_template('add_edit_product.html', product=product, categories=categories)
        else:
            return "Product not found", 404

# Route to delete a product
@app.route('/remove/<int:product_id>', methods=['GET'])
def delete_product(product_id):
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        try:
            # Delete product images associated with the product
            cursor.execute("DELETE FROM product_images WHERE product_id = %s", (product_id,))
            
            # Delete the product itself
            cursor.execute("DELETE FROM products WHERE product_id = %s", (product_id,))
            
            connection.commit()
            flash("Product deleted successfully", "success")
            return redirect('/product/')
        except Error as error:
            print("Error while deleting product:", error)
            connection.rollback()
            flash("Failed to delete product", "error")
            return redirect('/product/')
        finally:
            cursor.close()
            connection.close()
    else:
        return jsonify({'error': 'Failed to connect to database'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)
