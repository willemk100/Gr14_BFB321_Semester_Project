import sqlite3
from flask import Flask, jsonify, render_template

# 1. Initialize the Flask App
app = Flask(__name__)
DB_FILE = 'ordering.db'

# Helper function to connect to the database
def get_db_connection():
    # Use sqlite3.connect to open the database file
    conn = sqlite3.connect(DB_FILE)
    # Set the row factory to sqlite3.Row to get dictionary-like rows
    conn.row_factory = sqlite3.Row
    return conn

# 2. Define the API Endpoint to Fetch Vendor Data
@app.route('/api/vendor_menu', methods=['GET'])
def get_vendor_menu():
    conn = get_db_connection()
    
    # SQL query to join vendor and menu items
    sql_query = """
    SELECT 
        v.name AS vendor_name, 
        m.catagory, 
        m.name AS menu_item_name, 
        m.price
    FROM vendor v
    JOIN menuItem m ON v.vendor_id = m.vendor_id
    WHERE v.name = 'Tenz' 
    ORDER BY m.catagory, m.menu_item_name;
    """
    
    # Execute the query and fetch all results
    items = conn.execute(sql_query).fetchall()
    conn.close()
    
    # Convert the list of sqlite3.Row objects to a list of Python dictionaries
    items_list = [dict(item) for item in items]

    # Return the data as JSON
    return jsonify(items_list)

# 3. Define the Route for the HTML Page
@app.route('/')
def index():
    # Renders the HTML template
    return render_template('index.html')

# 4. Run the Application
if __name__ == '__main__':
    # Flask runs on port 5000 by default
    app.run(debug=True)