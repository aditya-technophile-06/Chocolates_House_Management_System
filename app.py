from flask import Flask, render_template, request, redirect, url_for
import database
import os

# Specify the template folder explicitly using an absolute path
template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=template_path)

# Debugging: Print current working directory, template folder, and check if 'ingredients.html' exists
print("Current working directory:", os.getcwd())
print("Template folder:", template_path)

# Check for ingredients.html file
ingredients_path = os.path.join(template_path, 'ingredients.html')
if not os.path.exists(ingredients_path):
    print("Error: 'ingredients.html' template not found in the 'templates/' folder at path:", ingredients_path)
else:
    print("'ingredients.html' template found at path:", ingredients_path)

# Initialize the database on the first request using a flag
initialized = False

@app.before_request
def initialize():
    global initialized
    if not initialized:
        print("Initializing the database...")
        database.create_tables()
        initialized = True

@app.teardown_appcontext
def close_connection(exception):
    database.close_connection(exception)

# ---------- Home Page ----------
@app.route('/')
def index():
    return render_template('index.html')

# ---------- Seasonal Flavors Routes ----------
@app.route('/flavors')
def flavors():
    db = database.get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM seasonal_flavors')
    flavors_list = cursor.fetchall()
    return render_template('flavors.html', flavors=flavors_list)

@app.route('/add_flavor', methods=['GET', 'POST'])
def add_flavor():
    if request.method == 'POST':
        flavor_name = request.form['flavor_name']
        availability_start = request.form['availability_start']
        availability_end = request.form['availability_end']

        db = database.get_db()
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO seasonal_flavors (flavor_name, availability_start, availability_end)
            VALUES (?, ?, ?)
        ''', (flavor_name, availability_start, availability_end))
        db.commit()
        return redirect(url_for('flavors'))
    return render_template('add_flavor.html')

@app.route('/edit_flavor/<int:flavor_id>', methods=['GET', 'POST'])
def edit_flavor(flavor_id):
    db = database.get_db()
    cursor = db.cursor()
    if request.method == 'POST':
        flavor_name = request.form['flavor_name']
        availability_start = request.form['availability_start']
        availability_end = request.form['availability_end']
        cursor.execute('''
            UPDATE seasonal_flavors
            SET flavor_name = ?, availability_start = ?, availability_end = ?
            WHERE id = ?
        ''', (flavor_name, availability_start, availability_end, flavor_id))
        db.commit()
        return redirect(url_for('flavors'))
    else:
        cursor.execute('SELECT * FROM seasonal_flavors WHERE id = ?', (flavor_id,))
        flavor = cursor.fetchone()
        return render_template('edit_flavor.html', flavor=flavor)

@app.route('/delete_flavor/<int:flavor_id>', methods=['GET', 'POST'])
def delete_flavor(flavor_id):
    db = database.get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM seasonal_flavors WHERE id = ?', (flavor_id,))
    db.commit()
    return redirect(url_for('flavors'))

# ---------- Ingredient Inventory Routes ----------
@app.route('/ingredients')
def ingredients():
    db = database.get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM ingredient_inventory')
    ingredients_list = cursor.fetchall()
    return render_template('ingredients.html', ingredients=ingredients_list)

@app.route('/add_ingredient', methods=['GET', 'POST'])
def add_ingredient():
    if request.method == 'POST':
        ingredient_name = request.form['ingredient_name']
        quantity_in_stock = request.form['quantity_in_stock']

        db = database.get_db()
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO ingredient_inventory (ingredient_name, quantity_in_stock)
            VALUES (?, ?)
        ''', (ingredient_name, quantity_in_stock))
        db.commit()
        return redirect(url_for('ingredients'))
    return render_template('add_ingredient.html')

@app.route('/edit_ingredient/<int:ingredient_id>', methods=['GET', 'POST'])
def edit_ingredient(ingredient_id):
    db = database.get_db()
    cursor = db.cursor()
    if request.method == 'POST':
        ingredient_name = request.form['ingredient_name']
        quantity_in_stock = request.form['quantity_in_stock']
        cursor.execute('''
            UPDATE ingredient_inventory
            SET ingredient_name = ?, quantity_in_stock = ?
            WHERE id = ?
        ''', (ingredient_name, quantity_in_stock, ingredient_id))
        db.commit()
        return redirect(url_for('ingredients'))
    else:
        cursor.execute('SELECT * FROM ingredient_inventory WHERE id = ?', (ingredient_id,))
        ingredient = cursor.fetchone()
        return render_template('edit_ingredient.html', ingredient=ingredient)

@app.route('/delete_ingredient/<int:ingredient_id>', methods=['GET', 'POST'])
def delete_ingredient(ingredient_id):
    db = database.get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM ingredient_inventory WHERE id = ?', (ingredient_id,))
    db.commit()
    return redirect(url_for('ingredients'))

# ---------- Customer Suggestions Routes ----------
@app.route('/suggestions')
def suggestions():
    db = database.get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM customer_suggestions')
    suggestions_list = cursor.fetchall()
    return render_template('suggestions.html', suggestions=suggestions_list)

@app.route('/add_suggestion', methods=['GET', 'POST'])
def add_suggestion():
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        suggested_flavor = request.form['suggested_flavor']
        allergy_concern = request.form['allergy_concern']

        db = database.get_db()
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO customer_suggestions (customer_name, suggested_flavor, allergy_concern)
            VALUES (?, ?, ?)
        ''', (customer_name, suggested_flavor, allergy_concern))
        db.commit()
        return redirect(url_for('suggestions'))
    return render_template('add_suggestion.html')

@app.route('/edit_suggestion/<int:suggestion_id>', methods=['GET', 'POST'])
def edit_suggestion(suggestion_id):
    db = database.get_db()
    cursor = db.cursor()
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        suggested_flavor = request.form['suggested_flavor']
        allergy_concern = request.form['allergy_concern']
        cursor.execute('''
            UPDATE customer_suggestions
            SET customer_name = ?, suggested_flavor = ?, allergy_concern = ?
            WHERE id = ?
        ''', (customer_name, suggested_flavor, allergy_concern, suggestion_id))
        db.commit()
        return redirect(url_for('suggestions'))
    else:
        cursor.execute('SELECT * FROM customer_suggestions WHERE id = ?', (suggestion_id,))
        suggestion = cursor.fetchone()
        return render_template('edit_suggestion.html', suggestion=suggestion)

@app.route('/delete_suggestion/<int:suggestion_id>', methods=['GET', 'POST'])
def delete_suggestion(suggestion_id):
    db = database.get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM customer_suggestions WHERE id = ?', (suggestion_id,))
    db.commit()
    return redirect(url_for('suggestions'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
