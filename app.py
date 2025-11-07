#INITIAL SETUP!!!
#***********************************************************
# Main Application File: app.py
#===========================================================
from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os
from datetime import datetime, timedelta # For date manipulations

# -----------------------------
# Auto-create database if missing
# -----------------------------
if not os.path.exists("ordering.db"):
    if os.path.exists("ordering.sql"):
        with open("ordering.sql", "r", encoding="utf-8") as f:
            sql_script = f.read()
        conn = sqlite3.connect("ordering.db")
        cursor = conn.cursor()
        cursor.executescript(sql_script)
        conn.commit()
        conn.close()
        print("Database 'ordering.db' created automatically.")
    else:
        print("'ordering.sql' not found. Please add the SQL file in the project folder.")

# -----------------------------
# Flask App Setup
# -----------------------------
app = Flask(__name__)
app.secret_key = '12345'  # Needed for session management (stores login info, flash messages, etc.)

# -----------------------------
# Database connection function
# -----------------------------
def get_db_connection():
    conn = sqlite3.connect('ordering.db')
    conn.row_factory = sqlite3.Row
    return conn
#===========================================================
#End of INITIAL SETUP!!!
#***********************************************************



#LOGIN AND NEW USER PAGES!!!
#***********************************************************
#Login Page - Where everything starts (login.html)
#===========================================================
@app.route('/', methods=["GET", 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM user WHERE username = ? AND password = ?', (username, password)).fetchone()
        

        if user:
            session['username'] = username
            session['user_id'] = user['user_id']
            session['user_type'] = user['user_type']
            

            if user['user_type'] == 'customer':
                return redirect(url_for('customer_home'))
            elif user['user_type'] == 'admin':
                return redirect(url_for('admin_home'))
            
        # Check vendor table if not a user
        conn = get_db_connection()
        vendor = conn.execute('SELECT * FROM vendor WHERE username = ? AND password = ?', (username, password)).fetchone()

        if vendor:
            session['username'] = username
            session['vendor_id'] = vendor['vendor_id']
            session['user_type'] = 'vendor'
            conn.close()

            return redirect(url_for('vendor_home'))
        
        # Invalid Login or if there is an error
        return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')
#End of Login Page
#===========================================================

# Log out funcion
#===========================================================
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))
#End of log out
#===========================================================

#New Customer Registration Page (new_customer.html)
#===========================================================



#End of New Customer Registration Page
#===========================================================
#End of LOGIN AND NEW USER PAGES!!!
#***********************************************************



#Now we move to different user sections!!!!
 
#ADMIN SECTION!!!
#************************************************************
#Admin Home Page (admin_main.html)
#===========================================================
@app.route('/admin_home')
def admin_home():
    if session.get('user_type') != 'admin':
        return redirect(url_for('login'))
    conn = get_db_connection()
    vendors = conn.execute('SELECT * FROM vendor').fetchall()
    conn.close()
    return render_template('admin_main.html', vendors=vendors)


# Delete vendor on admin_home page
#===============================================================
@app.route('/admin_home/delete_vendor/<int:vendor_id>', methods=['POST'])
def delete_vendor(vendor_id):
    if session.get('user_type') != 'admin':
        return redirect(url_for('login'))

    conn = get_db_connection()
    conn.execute('DELETE FROM vendor WHERE vendor_id = ?', (vendor_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_home'))

#End of Admin Home Page
#===============================================================

#Add vendor page 
#===============================================================
@app.route('/add_vendor', methods=['GET', 'POST'])
def add_vendor():
    if session.get('user_type') != 'admin':
        return redirect(url_for('login'))

    if request.method == 'POST':

        conn = get_db_connection()

        vendors = conn.execute('SELECT * FROM vendor').fetchall()

        vendors_ids = [vendor['vendor_id'] for vendor in vendors]
        last_id = max(vendors_ids) if vendors_ids else 0
        new_vendor_id = last_id + 1

        name = request.form['name']
        location = request.form['location']
        phone_number = request.form['phone_number']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        password_confirm = request.form['password_confirm']
        bank_name = request.form['bank_name']
        account_number = request.form['account_number']
        branch_code = request.form['branch_code']

        

        if password != password_confirm:
            conn.close()
            return render_template('admin_new_vendor.html', error='Passwords do not match')

         # Insert new vendor into the database
        
        conn.execute('INSERT INTO vendor (vendor_id, name, location, phone_number, email, username, password, bank_name, account_number, branch_code) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',

                     (new_vendor_id, name, location, phone_number, email, username, password, bank_name, account_number, branch_code))
        conn.commit()
        conn.close()

        return redirect(url_for('admin_home'))

    return render_template('admin_new_vendor.html')

#End of Add vendor page
#===============================================================


#Edit vendor details page
#===============================================================
@app.route('/admin_home/edit_vendor/<int:vendor_id>', methods=['GET', 'POST'])
def edit_vendor(vendor_id):
    if session.get('user_type') != 'admin':
        return redirect(url_for('login'))

    conn = get_db_connection()
    vendor = conn.execute('SELECT * FROM vendor WHERE vendor_id = ?', (vendor_id,)).fetchone()

    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        phone_number = request.form['phone_number']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        bank_name = request.form['bank_name']
        account_number = request.form['account_number']
        branch_code = request.form['branch_code']

        conn.execute('UPDATE vendor SET name = ?, location = ?, phone_number = ?, email = ?, username = ?, password = ?, bank_name = ?, account_number = ?, branch_code = ? WHERE vendor_id = ?',
                     (name, location, phone_number, email, username, password, bank_name, account_number, branch_code, vendor_id))
        conn.commit()
        conn.close()
        return redirect(url_for('admin_home'))

    conn.close()
    return render_template('admin_edit_vendor_details.html', vendor=vendor)
#End of Edit vendor details page
#===============================================================
#End of ADMIN SECTION!!!
#***************************************************************



#CUSTOMER SECTION!!!
#***************************************************************
#Customer home page (customer_main.html)
#================================================================
@app.route('/customer_home')
def customer_home():
    if session.get('user_type') != 'customer':
        return redirect(url_for('login'))

    conn = get_db_connection()
    vendors = conn.execute('SELECT * FROM vendor').fetchall()
    conn.close()
    return render_template('customer_main.html', vendors=vendors)
    
#End of Customer home page
#================================================================

#Menu section (customer_menu.html)
#================================================================
# For view menu of [vendor]
@app.route('/vendor/<int:vendor_id>/menu')
def vendor_menu(vendor_id):
    if session.get('user_type') != 'customer':
        return redirect(url_for('login'))

    conn = get_db_connection()
    selected_vendor = conn.execute('SELECT * FROM vendor WHERE vendor_id = ?', (vendor_id,)).fetchone()
    menu_items = conn.execute('SELECT * FROM menuItem WHERE vendor_id = ?', (vendor_id,)).fetchall()
    conn.close()
    
    menu_items = [dict(item) for item in menu_items]

    # Format prices to 2 decimal places
    for item in menu_items:
        item['price'] = f"{item['price']:.2f}"

    categories = sorted({item['category'] for item in menu_items})
    return render_template('customer_menu.html', menu_items=menu_items, selected_vendor=selected_vendor, categories = categories)
#End of Menu section
#================================================================

#Customer cart page (customer_cart.html)
#================================================================
#!! code


#End of Customer cart page
#================================================================

#Confirm payment page (customer_confirm_payment.html)
#================================================================
#!! code


#End of Confirm payment page
#================================================================
#End of CUSTOMER SECTION!!!
#***************************************************************


#VENDOR SECTION!!!
#***************************************************************
# Vendor orders page (vendor_main.html)
#===============================================================
@app.route('/vendor_home')
def vendor_home():
    # 1. Authentication and Vendor ID Retrieval
    if session.get('user_type') != 'vendor':
        return redirect(url_for('login'))
    
    # *** IMPORTANT: Get the logged-in vendor_id from the session. ***
    # For testing with your provided SQL data, we'll assume the logged-in vendor is 'Tenz' (vendor_id = 101).
    vendor_id = session['vendor_id'] 
    
    conn = get_db_connection()
    
    # 2. SQL Query to fetch, aggregate, calculate, and sort order data
    # Joins: order <-> orderItem <-> menuItem
    sql_query = """
    SELECT 
        o.order_id, 
        o.collection_time, 
        o.status,
        -- Calculate the total cost for the order by summing up price_per_item
        SUM(oi.price_per_item) AS total_cost,
        -- Use GROUP_CONCAT to combine all ordered item names and their price per item 
        -- into a single string for the 'Order (Products)' column.
        GROUP_CONCAT(CAST(mI.name AS TEXT) || ' (R' || printf('%.2f', oi.price_per_item) || ')', ', ') AS order_products_summary
    FROM "order" o
    JOIN "orderItem" oi ON o.order_id = oi.order_order_id
    JOIN "menuItem" mI ON oi.menuItem_menuItem_id = mI.menuItem_id
    WHERE oi.vendor_id = ?  -- Filter to show only orders belonging to the current vendor
    GROUP BY o.order_id, o.collection_time, o.status
    ORDER BY o.collection_time ASC; -- Sort the results by earliest collection time
    """

    orders_data_raw = conn.execute(sql_query, (vendor_id,)).fetchall()
    conn.close()
    
    # 3. Process data for Jinja2 template
    orders_for_template = []
    for row in orders_data_raw:
        # Determine the 'fee_status' based on the order 'status'
        fee_status = 'Unpaid'
        if row['status'] in ['Collected', 'Ready']:
             fee_status = 'Paid'
        
        orders_for_template.append({
            # The HTML table expects these keys:
            'tracking_id': f"#{row['order_id']}",
            'collection_time': row['collection_time'], 
            'order_products': row['order_products_summary'],
            'cost': row['total_cost'], # The calculated total cost (float/decimal)
            'fee_status': fee_status, # 'Paid' or 'Unpaid'
            'status': row['status']
        })

    # 4. Render the template
    return render_template('vendor_main.html', orders=orders_for_template)
#End of Vendor home page
#===============================================================

#vendor menu editing page (vendor_menu_edit.html)
#===============================================================    
@app.route('/vendor_menu_edit')
def vendor_menu_edit():
    if session.get('user_type') != 'vendor':
        return redirect(url_for('login'))

    vendor_id = session['vendor_id']  # Logged-in vendor
    conn = get_db_connection()
    
    menu_items = conn.execute(
        'SELECT * FROM menuItem WHERE vendor_id = ?', (vendor_id,)
    ).fetchall()
    conn.close()

    menu_items = [dict(item) for item in menu_items]
    categories = sorted({item['category'] for item in menu_items})

    return render_template(
        'vendor_menu_edit.html',
        menu_items=menu_items,
        categories=categories
    )


# Delete menu item
###########################################################
@app.route('/vendor_delete_menu_item/<int:item_id>', methods=['POST'])
def vendor_delete_menu_item(item_id):
    if session.get('user_type') != 'vendor':
        return redirect(url_for('login'))

    vendor_id = session['vendor_id']
    conn = get_db_connection()

    # Make sure the item belongs to this vendor
    item = conn.execute(
        'SELECT * FROM menuItem WHERE menuItem_id = ? AND vendor_id = ?',
        (item_id, vendor_id)
    ).fetchone()

    if item:
        conn.execute('DELETE FROM menuItem WHERE menuItem_id = ?', (item_id,))
        conn.commit()
        flash(f'Item "{item["name"]}" deleted successfully!', 'success')
    else:
        flash('Menu item not found or does not belong to you.', 'danger')

    conn.close()
    return redirect(url_for('vendor_menu_edit'))
#End Delete menu item
###############################################
#End of vendor menu editing page
#===============================================================

#vendor edit existing menu item page (vendor_edit_menu_item.html)
#===============================================================
@app.route('/vendor_edit_menu_item/<int:item_id>', methods=['GET', 'POST'])
def vendor_edit_menu_item(item_id):
    if session.get('user_type') != 'vendor':
        return redirect(url_for('login'))

    vendor_id = session['vendor_id']
    conn = get_db_connection()

    item = conn.execute(
        'SELECT * FROM menuItem WHERE menuItem_id = ? AND vendor_id = ?',
        (item_id, vendor_id)
    ).fetchone()

    if not item:
        conn.close()
        flash('Menu item not found or does not belong to you.', 'danger')
        return redirect(url_for('vendor_menu_edit'))

    if request.method == 'POST':
        name = request.form['name'].strip()
        price_input = request.form['price'].strip()
        cost_input = request.form['cost'].strip()

        # Server-side validation (no "R" and max 2 decimals)
        if "R" in price_input or "R" in cost_input:
            flash("Do not include 'R' in price or cost fields.", "danger")
            conn.close()
            return redirect(url_for('vendor_edit_menu_item', item_id=item_id))

        try:
            price = round(float(price_input), 2)
            cost = round(float(cost_input), 2)
        except ValueError:
            flash("Price and cost must be valid numeric values.", "danger")
            conn.close()
            return redirect(url_for('vendor_edit_menu_item', item_id=item_id))

        conn.execute(
            'UPDATE menuItem SET name = ?, price = ?, cost = ? WHERE menuItem_id = ?',
            (name, price, cost, item_id)
        )
        conn.commit()
        conn.close()

        flash(f'Item "{name}" updated successfully!', 'success')
        return redirect(url_for('vendor_menu_edit'))

    conn.close()
    return render_template('vendor_edit_menu_item.html', item=item)
#End of vendor edit menu item page
#===============================================================

#vendor new menu item page (vendor_new_menu_item.html)
#===============================================================
@app.route('/vendor_new_menu_item', methods=['GET', 'POST'])
def vendor_new_menu_item():
    if session.get('user_type') != 'vendor':
        return redirect(url_for('login'))

    vendor_id = session['vendor_id']
    conn = get_db_connection()

    # Fetch current categories for the dropdown
    menu_items = conn.execute(
        'SELECT category FROM menuItem WHERE vendor_id = ?', (vendor_id,)
    ).fetchall()
    categories = sorted({item['category'] for item in menu_items})

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        existing_category = request.form.get('existing_category', '').strip()
        new_category = request.form.get('new_category', '').strip()
        price = request.form.get('price', '').strip()
        cost = request.form.get('cost', '').strip()

        errors = []

        # Validate category choice
        if existing_category and new_category:
            errors.append("Please either select an existing category or type a new one, not both.")
        elif not existing_category and not new_category:
            errors.append("You must select an existing category or enter a new category.")

        category = new_category if new_category else existing_category

        # Validate other fields
        if not name:
            errors.append("Item name is required.")
        try:
            price_val = float(price)
            if round(price_val, 2) != price_val or price_val < 0:
                errors.append("Selling price must be a positive number with up to 2 decimals.")
        except ValueError:
            errors.append("Selling price must be a valid number.")
        try:
            cost_val = float(cost)
            if round(cost_val, 2) != cost_val or cost_val < 0:
                errors.append("Estimated cost must be a positive number with up to 2 decimals.")
        except ValueError:
            errors.append("Estimated cost must be a valid number.")

        # If any errors, show them
        if errors:
            for e in errors:
                flash(e, 'danger')
            return render_template('vendor_new_menu_item.html', categories=categories)

        # Insert new item into database
        conn.execute(
            'INSERT INTO menuItem (vendor_id, category, name, price, cost) VALUES (?, ?, ?, ?, ?)',
            (vendor_id, category, name, price_val, cost_val)
        )
        conn.commit()
        conn.close()

        flash(f'Item "{name}" added successfully!', 'success')
        return redirect(url_for('vendor_menu_edit'))

    conn.close()
    return render_template('vendor_new_menu_item.html', categories=categories)

#End of vendor new menu item page
#===============================================================

#vendor analytics page (vendor_analytics.html)
#===============================================================
#definiion to get filter by date
########################################
def get_date_range(filter_option):
    today = datetime.today().date()
    if filter_option == 'daily':
        start_date = today
    elif filter_option == 'weekly':
        start_date = today - timedelta(days=today.weekday())  # start of current week
    elif filter_option == 'monthly':
        start_date = today.replace(day=1)
    elif filter_option == 'yearly':
        start_date = today.replace(month=1, day=1)
    else:
        start_date = today
    end_date = today
    return start_date, end_date
#end of date range function
#########################################

@app.route('/vendor_analytics')
def vendor_analytics():
    if session.get('user_type') != 'vendor':
        return redirect(url_for('login'))

    vendor_id = session['vendor_id']
    conn = get_db_connection()

    # Get filter option from query string (default: daily)
    filter_option = request.args.get('filter', 'daily')
    start_date, end_date = get_date_range(filter_option)
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    # --- Completed Orders ---
    completed_orders_row = conn.execute("""
        SELECT COUNT(DISTINCT o.order_id) AS completed_orders
        FROM orders o
        JOIN orderItem oi ON o.order_id = oi.orders_order_id
        WHERE oi.vendor_id = ?
          AND o.status = 'Collected'
          AND o.order_date BETWEEN ? AND ?
    """, (vendor_id, start_date_str, end_date_str)).fetchone()
    completed_orders = completed_orders_row['completed_orders'] if completed_orders_row else 0

    # --- Revenue ---
    revenue_row = conn.execute("""
        SELECT SUM(oi.price_per_item) AS revenue
        FROM orders o
        JOIN orderItem oi ON o.order_id = oi.orders_order_id
        WHERE oi.vendor_id = ?
          AND o.status = 'Collected'
          AND o.order_date BETWEEN ? AND ?
    """, (vendor_id, start_date_str, end_date_str)).fetchone()
    revenue = revenue_row['revenue'] if revenue_row['revenue'] else 0

    # --- Most Popular Item ---
    popular_item_row = conn.execute("""
        SELECT mi.name, COUNT(*) AS sold_count
        FROM orderItem oi
        JOIN menuItem mi ON oi.menuItem_menuItem_id = mi.menuItem_id
        JOIN orders o ON oi.orders_order_id = o.order_id
        WHERE oi.vendor_id = ?
          AND o.status = 'Collected'
          AND o.order_date BETWEEN ? AND ?
        GROUP BY mi.name
        ORDER BY sold_count DESC
        LIMIT 1
    """, (vendor_id, start_date_str, end_date_str)).fetchone()
    popular_item = popular_item_row['name'] if popular_item_row else "N/A"

    # --- Sales History ---
    sales_history = conn.execute("""
        SELECT o.order_id, GROUP_CONCAT(mi.name, ', ') AS items,
               SUM(oi.price_per_item) AS total_price,
               o.order_date, o.collection_time
        FROM orders o
        JOIN orderItem oi ON o.order_id = oi.orders_order_id
        JOIN menuItem mi ON oi.menuItem_menuItem_id = mi.menuItem_id
        WHERE oi.vendor_id = ?
        GROUP BY o.order_id
        ORDER BY o.order_date DESC, o.collection_time DESC
    """, (vendor_id,)).fetchall()

    conn.close()

    return render_template(
        'vendor_analytics.html',
        completed_orders=completed_orders,
        revenue=revenue,
        popular_item=popular_item,
        sales_history=sales_history,
        filter_option=filter_option
    )   

#End of vendor analytics page
#===============================================================

#vendor analytics ABC page (vendor_analytics_ABC.html)
#===============================================================
#!! code




#End of vendor analytics ABC page
#===============================================================

#vendor analytics trends page (vendor_analytics_trends.html)
#===============================================================
#!! code




#End of vendor analytics trends page
#===============================================================

#vendor analytics forecasting page (vendor_analytics_forecasting.html)
#===============================================================
#!! code



#End of vendor analytics forecasting page
#===============================================================
#End of VENDOR SECTION!!!
#***************************************************************
    


#FINAL SETUP!!!
#***********************************************************
#Run the app
#===========================================================
if __name__ == '__main__':
    app.run(debug=True)
# End of app run
#===========================================================
#End of FINAL SETUP!!!
#***********************************************************

