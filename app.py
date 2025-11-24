#INITIAL SETUP!!!
#***********************************************************
# Main Application File: app.py
#===========================================================
from flask import Flask, render_template, request, redirect, url_for, g, session, flash
import sqlite3
import io, base64
import os
from datetime import datetime, timedelta, date, time 
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

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
                return redirect(url_for('customer_main'))
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
@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    
    if request.method == 'POST':

        conn = get_db_connection()
        #users = conn.execute('SELECT * FROM user').fetchall()
        user_type = 'customer'


        # Data from form

        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        cell_number = request.form['cell_number']
        student_number = request.form['student_number']
        date_of_birth = request.form['date_of_birth']
        cell_number = request.form['cell_number']
        username = request.form['username']
        password = request.form['new_password']
        password_confirm = request.form['confirm_password']

        # Check if username already exists
        check_existing_user = conn.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone()

        if check_existing_user:
            conn.close()
            return render_template('new_customer.html', error1='Username already exists', form_data=request.form)

        if password != password_confirm:
            conn.close()
            return render_template('admin_new_vendor.html', error2='Passwords do not match', form_data=request.form)

         # Insert new customer into the database
        
        conn.execute('INSERT INTO user (username, password, student_number, name, surname, date_of_birth, cell_number, email, user_type) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',

                     (username, password, student_number, name, surname, date_of_birth, cell_number, email, user_type))
        conn.commit()
        conn.close()
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('new_customer.html')


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
# Standard operating hours for all vendors 
# Just specified here for easy editing later (could be  added to DB if vendors will have different hours)
# For the purpose of this project, all vendors have same hours: 08:00–16:00
STANDARD_OPEN = time(8, 0)   # 08:00
STANDARD_CLOSE = time(16, 0) # 16:00

#function to check if vendor is open
def is_open_now():
    """Returns True if current time is within standard operating hours."""
    now = datetime.now().time()
    return STANDARD_OPEN <= now <= STANDARD_CLOSE

#Customer home page (customer_main.html)
#================================================================
@app.route('/customer_main')
def customer_main():
    if session.get('user_type') != 'customer':
        return redirect(url_for('login'))

    user_id = session.get('user_id')
    conn = get_db_connection()

    # ------------------------
    # Vendors with status
    # ------------------------
    vendors = conn.execute("SELECT * FROM vendor").fetchall()
    now = datetime.now().time()
    vendors_with_status = []

    for vendor in vendors:
        vendor_dict = dict(vendor)
        if is_open_now():  # your function
            vendor_dict['status_text'] = f"Open — Closes at {STANDARD_CLOSE.strftime('%H:%M')}"
            vendor_dict['status_class'] = 'bg-success'
        else:
            if now < STANDARD_OPEN:
                vendor_dict['status_text'] = f"Closed — Opens at {STANDARD_OPEN.strftime('%H:%M')}"
            else:
                vendor_dict['status_text'] = f"Closed — Opens at {STANDARD_OPEN.strftime('%H:%M')} tomorrow"
            vendor_dict['status_class'] = 'bg-danger'
        vendors_with_status.append(vendor_dict)

    # ------------------------
    # Active orders (not Collected)
    # ------------------------
    active_orders_raw = conn.execute("""
        SELECT o.*, v.name AS vendor_name
        FROM orders o
        JOIN orderItem oi ON oi.orders_order_id = o.order_id
        JOIN vendor v ON oi.vendor_id = v.vendor_id
        WHERE o.user_id = ? AND o.status != 'Collected'
        GROUP BY o.order_id
        ORDER BY o.collection_time ASC
    """, (user_id,)).fetchall()

    active_orders = []
    for order in active_orders_raw:
        order_dict = dict(order)

        # Fetch items for this order
        items = conn.execute("""
            SELECT oi.*, m.name AS item_name, m.category
            FROM orderItem oi
            JOIN menuItem m ON oi.menuItem_menuItem_id = m.menuItem_id
            WHERE oi.orders_order_id = ?
        """, (order['order_id'],)).fetchall()

        # Convert rows to dicts
        order_dict['items'] = [dict(item) for item in items]

        # Calculate total
        order_dict['total'] = sum(item['price_per_item'] for item in order_dict['items'])
        

        # Progress mapping
        status_map = {
            'Submitted': (25, 'bg-warning'),
            'Preparing': (50, 'bg-primary'),
            'Ready': (75, 'bg-info'),
            'Collected': (100, 'bg-success'),
            'Uncollected': (0, 'bg-danger')
        }
        progress_value, progress_class = status_map.get(order['status'], (0, 'bg-secondary'))
        order_dict['progress_value'] = int(progress_value)
        order_dict['progress_class'] = progress_class

        active_orders.append(order_dict)

    # ------------------------
    # Last 3 collected orders
    # ------------------------
    last_collected_orders_raw = conn.execute("""
        SELECT o.*, v.name AS vendor_name
        FROM orders o
        JOIN orderItem oi ON oi.orders_order_id = o.order_id
        JOIN vendor v ON oi.vendor_id = v.vendor_id
        WHERE o.user_id = ? AND o.status = 'Collected'
        GROUP BY o.order_id
        ORDER BY o.collection_time DESC
        LIMIT 3
    """, (user_id,)).fetchall()

    last_collected_orders = []
    for order in last_collected_orders_raw:
        order_dict = dict(order)
        items = conn.execute("""
            SELECT oi.*, m.name AS item_name, m.category
            FROM orderItem oi
            JOIN menuItem m ON oi.menuItem_menuItem_id = m.menuItem_id
            WHERE oi.orders_order_id = ?
        """, (order['order_id'],)).fetchall()
        order_dict['items'] = [dict(item) for item in items]
        order_dict['total'] = sum(item['price_per_item'] for item in order_dict['items'])
        last_collected_orders.append(order_dict)

    conn.close()

    return render_template(
        'customer_main.html',
        vendors=vendors_with_status,
        active_orders=active_orders,
        last_collected_orders=last_collected_orders
    )
    
#End of Customer home page
#================================================================

#Menu section (customer_menu.html)
#================================================================
# For view menu of [vendor]
@app.route('/customer/<int:vendor_id>/menu')
def customer_menu(vendor_id):
    if session.get('user_type') != 'customer':
        return redirect(url_for('login'))
    

    conn = get_db_connection()
    selected_vendor = conn.execute('SELECT * FROM vendor WHERE vendor_id = ?', (vendor_id,)).fetchone()
    menu_items = conn.execute('SELECT * FROM menuItem WHERE vendor_id = ?', (vendor_id,)).fetchall()
    conn.close()

    #save last vendor id in session
    session['last_vendor_id'] = vendor_id

    menu_items = [dict(item) for item in menu_items]

    # Format prices to 2 decimal places
    for item in menu_items:
        item['price'] = f"{item['price']:.2f}"

    categories = sorted({item['category'] for item in menu_items})
    return render_template('customer_menu.html', menu_items=menu_items, selected_vendor=selected_vendor, categories = categories)

#Add to cart function
#################################################################
@app.route('/add_to_cart/<int:item_id>/<int:vendor_id>')
def add_to_cart(item_id, vendor_id):
    if 'cart' not in session:
        session['cart'] = []

    conn = get_db_connection()
    item = conn.execute(
        "SELECT menuItem_id, name, category, price, vendor_id FROM menuItem WHERE menuItem_id = ?", (item_id,)
    ).fetchone()
    conn.close()

    if not item:
        flash("Item not found.", "danger")
        return redirect(url_for('customer_menu', vendor_id=vendor_id))

    # Check if item is already in cart
    for cart_item in session['cart']:
        if cart_item['id'] == item['menuItem_id']:
            cart_item['quantity'] += 1
            break
    else:
        session['cart'].append({
            'id': item['menuItem_id'],
            'name': item['name'],
            'category': item['category'],
            'price': float(item['price']),
            'quantity': 1,
            'vendor_id': item['vendor_id']
        })

    session.modified = True
    flash(f"Added {item['name']} {item['category']} to cart.", "success")
    return redirect(url_for('customer_menu', vendor_id=vendor_id))
#end of Add to cart function
#################################################################
#End of Customer Menu section
#================================================================

#Customer cart page (customer_cart.html)
#================================================================
@app.route('/cart')
def view_cart():
    cart = session.get('cart', [])
    total = sum(item['price'] * item['quantity'] for item in cart)
    return render_template('customer_cart.html', cart=cart, total=total)

#Plus button function
##########################################################
@app.route('/cart/increment/<int:item_id>')
def increment_cart_item(item_id):
    cart = session.get('cart', [])
    for item in cart:
        if item['id'] == item_id:
            item['quantity'] += 1
            break
    session['cart'] = cart
    session.modified = True
    return redirect(url_for('view_cart'))
#End of Plus button function
##########################################################

#Minus button function
##########################################################
@app.route('/cart/decrement/<int:item_id>')
def decrement_cart_item(item_id):
    cart = session.get('cart', [])
    for item in cart:
        if item['id'] == item_id:
            if item['quantity'] > 1:
                item['quantity'] -= 1
            break
    session['cart'] = cart
    session.modified = True
    return redirect(url_for('view_cart'))
#End of Minus button function
##########################################################

#Remove item from cart function
#########################################################
@app.route('/remove_from_cart/<int:item_id>')
def remove_from_cart(item_id):
    cart = session.get('cart', [])
    cart = [item for item in cart if item['id'] != item_id]
    session['cart'] = cart
    session.modified = True
    return redirect(url_for('view_cart'))
#End of Remove item from cart function
##########################################################
#End of Customer cart page
#================================================================

#Confirm payment page (customer_confirm_payment.html)
#================================================================
# Function to generate pickup times
##########################################################
def generate_pickup_times():
    """Generate 5-min interval pickup times within operating hours,
    starting 30 minutes from now and aligned to :00, :05, :10...:55."""
    
    now = datetime.now()

    # If closed now → no pickup times
    if not is_open_now():
        return []

    times = []

    # Operating hour boundaries
    start = datetime.combine(now.date(), STANDARD_OPEN)
    end = datetime.combine(now.date(), STANDARD_CLOSE)

    # Start 30 minutes from now
    start_time = now + timedelta(minutes=30)

    # Round UP to nearest 5-min mark
    minute_mod = start_time.minute % 5
    if minute_mod != 0:
        start_time += timedelta(minutes=(5 - minute_mod))
    start_time = start_time.replace(second=0, microsecond=0)

    # If the first available time is before opening → push to opening
    if start_time < start:
        start_time = start

    # Generate 5-minute slots
    current = start_time
    while current <= end:
        times.append(current.strftime("%H:%M"))
        current += timedelta(minutes=5)

    return times
#End of generate pickup times function
###########################################################

# Confirm payment if they choose to pay on collection (cash)
############################################################
@app.route('/confirm_payment/cash', methods=['GET', 'POST'])
def confirm_payment_cash():
    cart = session.get('cart', [])
    if not cart:
        flash("Your cart is empty.", "info")
        return redirect(url_for('customer_main'))

    total = sum(item['price'] * item['quantity'] for item in cart)
    pickup_times = generate_pickup_times()

    if request.method == 'POST' and 'confirm_payment' in request.form:
        selected_pickup = request.form.get('pickup_time')
        if not pickup_times:
            flash("Sorry, vendor is closed. Orders can only be placed 08:00–16:00.", "danger")
        elif not selected_pickup:
            flash("Please select a pickup time.", "danger")
        else:
            process_order(cart, payment_method='cash', payment_status='unpaid', pickup_time=selected_pickup)
            session.pop('cart', None)
            flash("Order confirmed!", "success")
            return redirect(url_for('customer_main'))

    return render_template(
        'customer_confirm_payment.html',
        cart=cart,
        total=total,
        pay_option='cash',
        pickup_times=pickup_times,
        errors={},
        form_data={}
    )
#End of confirm payment if cash
############################################################

# Confirm payment if they choose to pay online (card)
#############################################################
@app.route('/confirm_payment/online', methods=['GET', 'POST'])
def confirm_payment_online():
    cart = session.get('cart', [])
    if not cart:
        flash("Your cart is empty.", "info")
        return redirect(url_for('customer_main'))

    total = sum(item['price'] * item['quantity'] for item in cart)
    pickup_times = generate_pickup_times()
    errors = {}
    form_data = request.form

    if request.method == 'POST' and 'confirm_payment' in request.form:
        # Pickup time
        selected_pickup = form_data.get('pickup_time')
        if not pickup_times:
            flash("Sorry, vendor is closed. Orders can only be placed 08:00–16:00.", "danger")
        if not selected_pickup:
            errors['pickup_time'] = "Please select a pickup time."

        # Card validations
        card_first = form_data.get('card_first', '').strip()
        card_last = form_data.get('card_last', '').strip()
        card_number = form_data.get('card_number', '').replace(" ", "")
        card_cvv = form_data.get('card_cvv', '').strip()
        card_expiry = form_data.get('card_expiry', '').strip()

        if not card_first: errors['card_first'] = "First name required."
        if not card_last: errors['card_last'] = "Last name required."
        if not card_number.isdigit() or not (13 <= len(card_number) <= 19):
            errors['card_number'] = "Card number must be 13–19 digits."
        if not card_cvv.isdigit() or len(card_cvv) not in [3,4]:
            errors['card_cvv'] = "CVV must be 3 or 4 digits."
        try:
            exp_year, exp_month = map(int, card_expiry.split("-"))
            exp_date = datetime(exp_year, exp_month, 1)
            exp_date = exp_date.replace(day=28) + timedelta(days=4)
            exp_date = exp_date - timedelta(days=exp_date.day)
            if exp_date < datetime.today(): errors['card_expiry'] = "Card expired."
        except:
            errors['card_expiry'] = "Invalid expiry date."

        if errors:
            return render_template(
                'customer_confirm_payment.html',
                cart=cart,
                total=total,
                pay_option='online',
                pickup_times=pickup_times,
                errors=errors,
                form_data=form_data
            )

        # All good, process order
        process_order(cart, payment_method='online', payment_status='paid', pickup_time=selected_pickup)
        session.pop('cart', None)
        flash("Order confirmed!", "success")
        return redirect(url_for('customer_main'))

    return render_template(
        'customer_confirm_payment.html',
        cart=cart,
        total=total,
        pay_option='online',
        pickup_times=pickup_times,
        errors=errors,
        form_data=form_data
    )
#End of confirm payment if online
#############################################################

#final order processing function
#########################################################
def process_order(cart, payment_method, payment_status, pickup_time):
    conn = get_db_connection()
    cur = conn.cursor()
    vendor_id = cart[0]['vendor_id']  # Assuming all items from same vendor

    # Get current date
    order_date = datetime.now().date()

    cur.execute("""
        INSERT INTO orders (user_id, order_date, collection_time, status, payment_method, payment_status, created_at, updated_at)
        VALUES (?, ?, ?, 'Submitted', ?, ?, ?, ?)
    """, (
        session.get('user_id'),
        order_date,
        pickup_time,
        payment_method,
        payment_status,
        datetime.now(),
        datetime.now()
    ))
    order_id = cur.lastrowid

    for item in cart:
        for _ in range(item['quantity']):
            cur.execute("""
                INSERT INTO orderItem (orders_order_id, menuItem_menuItem_id, vendor_id, price_per_item)
                VALUES (?, ?, ?, ?)
            """, (order_id, item['id'], vendor_id, item['price']))

    conn.commit()
    conn.close()
#End of final order processing function
#########################################################
#End of Confirm payment page
#================================================================
#End of CUSTOMER SECTION!!!
#***************************************************************

#VENDOR SECTION!!!
#***************************************************************
# Vendor orders page (vendor_main.html)
#===============================================================
@app.route('/vendor_home', methods=['GET', 'POST'])
def vendor_home():
    # 1. Authentication and Vendor ID Retrieval
    if session.get('user_type') != 'vendor':
        return redirect(url_for('login'))

    vendor_id = session['vendor_id']

    conn = get_db_connection()

    # 2. SQL Query to fetch all orders for the vendor
    sql_query = """
    SELECT 
        o.order_id, 
        o.collection_time, 
        o.status,
        SUM(oi.price_per_item) AS total_cost,
        GROUP_CONCAT(CAST(mI.name AS TEXT) || ' (R' || printf('%.2f', oi.price_per_item) || ')', ', ') AS order_products_summary
    FROM "orders" o
    JOIN "orderItem" oi ON o.order_id = oi.orders_order_id
    JOIN "menuItem" mI ON oi.menuItem_menuItem_id = mI.menuItem_id
    WHERE oi.vendor_id = ?
    GROUP BY o.order_id, o.collection_time, o.status
    ORDER BY o.collection_time ASC;
    """

    orders_data_raw = conn.execute(sql_query, (vendor_id,)).fetchall()

    orders_for_template = []
    for row in orders_data_raw:
        fee_status = 'Unpaid'
        if row['status'] in ['Collected', 'Ready']:
            fee_status = 'Paid'

        orders_for_template.append({
            'tracking_id': f"#{row['order_id']}",
            'collection_time': row['collection_time'],
            'order_products': row['order_products_summary'],
            'cost': row['total_cost'],
            'fee_status': fee_status,
            'status': row['status']
        })

    # 3. Handle selection of a specific order
    selected_order = None
    if request.method == 'POST':
        selected_id = request.form.get('selected_order_id')
        if selected_id:
            # strip # if it’s included
            selected_id_clean = selected_id.replace('#', '')
            for order in orders_for_template:
                if order['tracking_id'] == f"#{selected_id_clean}":
                    selected_order = order
                    break

    # Default to first order if none selected
    if not selected_order and orders_for_template:
        selected_order = orders_for_template[0]

    conn.close()

    return render_template(
        'vendor_main.html',
        orders=orders_for_template,
        selected_order=selected_order
    )

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
@app.route('/vendor_analytics_ABC', methods=['GET'])
def vendor_analytics_ABC():
    if session.get('user_type') != 'vendor':
        return redirect(url_for('login'))

    vendor_id = session['vendor_id']
    timeframe = request.args.get('timeframe', 'monthly')  # default monthly
    metric = request.args.get('metric', 'Profit')
    month_filter = request.args.get('month_filter', 'october').lower()  # default: October

    conn = get_db_connection()

    # Get min/max dates from vendor's orders
    date_row = conn.execute("""
        SELECT 
            MIN(DATE(o.order_date)) AS min_date, 
            MAX(DATE(o.order_date)) AS max_date
        FROM orders o
        JOIN orderItem oi ON o.order_id = oi.orders_order_id
        WHERE oi.vendor_id = ?
    """, (vendor_id,)).fetchone()

    if not date_row or not date_row['min_date'] or not date_row['max_date']:
        conn.close()
        return render_template("vendor_analytics_ABC.html", image_data=None, data=[], metric=metric, timeframe=timeframe, month_filter=month_filter)

    db_min_date = date.fromisoformat(date_row['min_date'])
    db_max_date = date.fromisoformat(date_row['max_date'])

    # Determine start and end date
    if timeframe == 'monthly':
        prev_month = (db_max_date.replace(day=1) - timedelta(days=1)).replace(day=1)  # start of October if db_max_date is November

        if month_filter == 'october':
            start_date = prev_month
            end_date = prev_month.replace(day=31)
        elif month_filter == 'november':
            start_date = db_max_date.replace(day=1)
            end_date = db_max_date
        elif month_filter == 'all':  #
            start_date = prev_month
            end_date = db_max_date
        else:
            start_date = prev_month
            end_date = prev_month.replace(day=31)
    elif timeframe == 'yearly':
        start_date = db_max_date.replace(month=1, day=1)
        end_date = db_max_date
    else:
        start_date = db_min_date
        end_date = db_max_date

    # Query per menu item
    query = """
    SELECT
        mi.menuItem_id AS menu_item_id,
        mi.category AS category,
        mi.name AS item_name,
        COUNT(*) AS units_sold,
        SUM(oi.price_per_item) AS total_revenue,
        SUM(mi.cost) AS total_cost,
        SUM(oi.price_per_item) - SUM(mi.cost) AS total_profit
    FROM orderItem oi
    JOIN orders o ON oi.orders_order_id = o.order_id
    JOIN menuItem mi ON oi.menuItem_menuItem_id = mi.menuItem_id
    WHERE oi.vendor_id = ?
      AND DATE(o.order_date) BETWEEN DATE(?) AND DATE(?)
    GROUP BY mi.menuItem_id, mi.category, mi.name
    """

    rows = conn.execute(query, (vendor_id, start_date.isoformat(), end_date.isoformat())).fetchall()
    conn.close()

    data = []
    for r in rows:
        label = f"{r['category']} ({r['item_name']})"
        data.append({
            'menu_item_id': r['menu_item_id'],
            'label': label,
            'category': r['category'],
            'item_name': r['item_name'],
            'units_sold': int(r['units_sold'] or 0),
            'total_revenue': float(r['total_revenue'] or 0.0),
            'total_cost': float(r['total_cost'] or 0.0),
            'total_profit': float(r['total_profit'] or 0.0)
        })

    # Determine metric used
    metric_key = 'units_sold' if metric == 'Orders' else \
                 'total_cost' if metric == 'Cost' else 'total_profit'

    data.sort(key=lambda x: x[metric_key], reverse=True)

    values = [d[metric_key] for d in data]
    total_value = sum(values) or 1.0
    cum_sum = 0.0
    for d, v in zip(data, values):
        cum_sum += v
        d['cum_value'] = cum_sum
        d['cum_percent'] = (cum_sum / total_value) * 100.0

    for d in data:
        cp = d['cum_percent']
        if cp <= 70.0:
            d['abc_class'] = 'A'
        elif cp <= 90.0:
            d['abc_class'] = 'B'
        else:
            d['abc_class'] = 'C'

    # Plot ABC chart
    import matplotlib.pyplot as plt
    import io, base64
    from matplotlib.patches import Patch

    labels = [d['label'] for d in data]
    plot_values = [d[metric_key] for d in data]
    classes = [d['abc_class'] for d in data]

    color_map = {'A': 'tab:green', 'B': 'tab:orange', 'C': 'tab:gray'}
    colors = [color_map[c] for c in classes]

    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(range(len(labels)), plot_values, color=colors)
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha='right')
    ax.set_ylabel(metric)
    ax.set_xlabel('Menu Item (Category (Name))')
    ax.set_title(f'ABC Classification by {metric} ({month_filter.capitalize()} {start_date.year})')
    plt.tight_layout()

    legend_elements = [Patch(facecolor=color_map['A'], label='A (Top 70%)'),
                       Patch(facecolor=color_map['B'], label='B (70-90%)'),
                       Patch(facecolor=color_map['C'], label='C (Bottom 10%)')]
    ax.legend(handles=legend_elements, loc='upper right')

    # Cumulative % line
    ax2 = ax.twinx()
    cum_percents = [d['cum_percent'] for d in data]
    ax2.plot(range(len(labels)), cum_percents, color='black', marker='o', linewidth=1)
    ax2.set_ylim(0, 110)
    ax2.set_ylabel('Cumulative %')

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)

    return render_template('vendor_analytics_ABC.html',
                           image_data=image_base64,
                           data=data,
                           metric=metric,
                           timeframe=timeframe,
                           month_filter=month_filter,
                           start_date=start_date,
                           end_date=end_date)

#End of vendor analytics ABC page
#===============================================================

#vendor analytics trends page (vendor_analytics_trends.html)
#===============================================================
def get_db_connection():
    conn = sqlite3.connect('ordering.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/vendor_analytics_trends', methods=['GET'])
def vendor_analytics_trends():
    if session.get('user_type') != 'vendor':
        return redirect(url_for('login'))

    vendor_id = session['vendor_id']

    # Fetch all menu items for the vendor
    conn = get_db_connection()
    menu_items = conn.execute(
        "SELECT category, name FROM menuItem WHERE vendor_id=?",
        (vendor_id,)
    ).fetchall()
    menu_items_list = [f"{item['category']}({item['name']})" for item in menu_items]

    # Get query parameters
    product1 = request.args.get('product1', menu_items_list[0] if menu_items_list else '')
    product2 = request.args.get('product2', menu_items_list[1] if len(menu_items_list) > 1 else '')
    metric = request.args.get('metric', 'Units Sold')
    timeframe = request.args.get('timeframe', 'monthly')  # 'monthly' or 'yearly'
    month = request.args.get('month', 'October')  # Only used if timeframe=monthly

    # Helper function to fetch data for line graph
    def get_product_data(product_display, timeframe, month):
        if '(' in product_display and ')' in product_display:
            category, name = product_display.split('(')
            name = name.rstrip(')')
        else:
            category, name = '', product_display

        query = """
        SELECT o.order_date, oi.price_per_item, m.cost
        FROM orderItem oi
        JOIN orders o ON oi.orders_order_id = o.order_id
        JOIN menuItem m ON oi.menuItem_menuItem_id = m.menuItem_id
        WHERE oi.vendor_id=? AND m.name=? AND m.category=?
        """
        rows = conn.execute(query, (vendor_id, name, category)).fetchall()
        data = {}
        for row in rows:
            date_key = row['order_date']
            # Filter by month if monthly
            if timeframe == 'monthly':
                if month == 'October' and not date_key.startswith('2025-10'):
                    continue
                if month == 'November' and not date_key.startswith('2025-11'):
                    continue
            elif timeframe == 'yearly':
                if not (date_key.startswith('2025-10') or date_key.startswith('2025-11')):
                    continue
            if date_key not in data:
                data[date_key] = {'Units Sold':0, 'Total Profit':0, 'Total Cost':0}
            data[date_key]['Units Sold'] += 1
            data[date_key]['Total Profit'] += row['price_per_item'] - row['cost']
            data[date_key]['Total Cost'] += row['cost']
        return data
    
    #Helper function to calculate totals for table summary
    def calculate_totals(aggregated_data):
        totals = {'Units Sold': 0, 'Total Profit': 0.0, 'Total Cost': 0.0}
        for period_key in aggregated_data:
            totals['Units Sold'] += aggregated_data[period_key]['Units Sold']
            totals['Total Profit'] += aggregated_data[period_key]['Total Profit']
            totals['Total Cost'] += aggregated_data[period_key]['Total Cost']
        # Format currency fields to Rands (R) with 2 decimal places
        totals['Total Profit'] = f"R{totals['Total Profit']:.2f}"
        totals['Total Cost'] = f"R{totals['Total Cost']:.2f}"
        return totals
    
    # Fetch data for both products
    data1 = get_product_data(product1, timeframe, month)
    data2 = get_product_data(product2, timeframe, month)

    # Calculate summary data for the table
    summary1 = calculate_totals(data1)
    summary2 = calculate_totals(data2)

    # Structure data for easy iteration in the HTML template
    table_data = [
        {'item': product1, 'summary': summary1},
        {'item': product2, 'summary': summary2}
    ]

    # Prepare line graph with sorted dates
    all_dates = sorted(set(list(data1.keys()) + list(data2.keys())))
    # Convert to datetime objects for proper sorting and plotting
    all_dates_dt = [datetime.strptime(d, "%Y-%m-%d") for d in all_dates]

    values1 = [data1.get(d.strftime("%Y-%m-%d"), {metric:0})[metric] for d in all_dates_dt]
    values2 = [data2.get(d.strftime("%Y-%m-%d"), {metric:0})[metric] for d in all_dates_dt]

    plt.figure(figsize=(12,5))
    plt.plot(all_dates_dt, values1, marker='o', label=product1)
    plt.plot(all_dates_dt, values2, marker='o', label=product2)
    plt.title(f"{metric} Trends")
    plt.xlabel("Date")
    plt.ylabel(metric)
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.legend()

    # Format X-axis as 'DD MMM' for readability
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%d %b'))

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()

    conn.close()

    return render_template('vendor_analytics_trends.html',
                           graph_url=graph_url,
                           menu_items=menu_items_list,
                           product1=product1,
                           product2=product2,
                           metric=metric,
                           timeframe=timeframe,
                           month=month,
                           table_data=table_data)
                           
#End of vendor analytics trends page
#===============================================================

#vendor analytics forecasting page (vendor_analytics_forecasting.html)
#===============================================================
def get_menu_items(conn, vendor_id):
    """Fetches a list of all individual menu items (ID, category, name) for the vendor."""
    items = conn.execute(
        'SELECT menuItem_id, category, name FROM menuItem WHERE vendor_id = ? ORDER BY category, name',
        (vendor_id,)
    ).fetchall()
    
    return [f"{row[0]}|{row[1]} ({row[2]})" for row in items]

@app.route('/vendor_analytics_forecasting', methods=['GET'])
def vendor_analytics_forecasting():
    if session.get('user_type') != 'vendor':
        return redirect(url_for('login'))

    # Ensure request is imported: from flask import request, ...
    vendor_id = session['vendor_id']
    conn = get_db_connection()
    
    # --- Item Selection Logic ---
    
    # 1. Get all individual menu items for the dropdown
    menu_items = get_menu_items(conn, vendor_id)
    
    # 2. Get the selected item ID from the URL (name="product1")
    selected_item_id = request.args.get('product1') 
    
    # Set a default item ID if none is selected
    if not selected_item_id and menu_items:
        # Default to the first item ID in the list
        selected_item_id = str(menu_items[0]['menuItem_id'])
        
    # Find the name and category of the selected item for display and analysis
    # Need to convert ID to string for comparison since request.args.get returns string
    selected_item_data = next((item for item in menu_items if str(item['menuItem_id']) == selected_item_id), None)
    
    # Set the primary analysis variables
    target_item_id = selected_item_id
    target_item_name = f"{selected_item_data['category']} - {selected_item_data['name']}" if selected_item_data else 'Item Not Found'
    
    # --- 1. Define Historical Periods (Remains the same) ---
    weekly_periods = [
        {'id': 1, 'start': '2025-10-27', 'end': '2025-11-02'},
        {'id': 2, 'start': '2025-10-20', 'end': '2025-10-26'},
        {'id': 3, 'start': '2025-10-13', 'end': '2025-10-19'},
    ]
    
    historical_data = []

    # --- 2. Calculate Historical Data (Per Week) ---
    for period in weekly_periods:
        start_date = period['start']
        end_date = period['end']
        week_data = {'id': period['id'], 'units_sold': 0, 'peak_time': 'N/A', 'avg_daily_peak': 0}
        
        # SQL to get Units Sold
        units_sql = """
            SELECT COUNT(T1.orderItem_id)
            FROM orderItem AS T1
            INNER JOIN orders AS T2 ON T1.orders_order_id = T2.order_id
            INNER JOIN menuItem AS T3 ON T1.menuItem_menuItem_id = T3.menuItem_id
            WHERE T3.menuItem_id = ? AND T3.vendor_id = ?
              AND T2.order_date BETWEEN ? AND ?;
        """
        units_sold = conn.execute(units_sql, (target_item_id, vendor_id, start_date, end_date)).fetchone()[0]
        week_data['units_sold'] = units_sold
        
        if units_sold > 0:
            # SQL to get Most Frequent Pickup Time (Peak Time)
            peak_time_sql = """
                SELECT T2.collection_time 
                FROM orderItem AS T1
                INNER JOIN orders AS T2 ON T1.orders_order_id = T2.order_id
                INNER JOIN menuItem AS T3 ON T1.menuItem_menuItem_id = T3.menuItem_id
                WHERE T3.menuItem_id = ? AND T3.vendor_id = ?
                  AND T2.order_date BETWEEN ? AND ?
                GROUP BY T2.collection_time
                ORDER BY COUNT(T2.collection_time) DESC
                LIMIT 1;
            """
            peak_time = conn.execute(peak_time_sql, (target_item_id, vendor_id, start_date, end_date)).fetchone()[0]
            week_data['peak_time'] = peak_time

            # SQL to get orders during the peak time within this week 
            peak_orders_sql = """
                SELECT COUNT(order_id)
                FROM orders
                WHERE order_date BETWEEN ? AND ?
                  AND collection_time = ?;
            """
            orders_at_peak = conn.execute(peak_orders_sql, (start_date, end_date, peak_time)).fetchone()[0]
            
            # Calculate Average Daily Orders During Peak
            week_data['avg_daily_peak'] = round(orders_at_peak / 7.0, 2)
        
        historical_data.append(week_data)

    # --- 3. Calculate Forecasting Metrics ---
    
    # 3a. Predicted Weekly Demand
    total_units_sold_3w = sum(w['units_sold'] for w in historical_data)
    # Handle division by zero edge case safely
    if len(weekly_periods) > 0:
        predicted_demand = round(total_units_sold_3w / len(weekly_periods), 0)
    else:
        predicted_demand = 0

    # 3b. Busiest Time (Most frequent peak time across all 3 weeks)
    busiest_time_sql = """
        SELECT T2.collection_time 
        FROM orderItem AS T1
        INNER JOIN orders AS T2 ON T1.orders_order_id = T2.order_id
        INNER JOIN menuItem AS T3 ON T1.menuItem_menuItem_id = T3.menuItem_id
        WHERE T3.menuItem_id = ? AND T3.vendor_id = ?
          AND T2.order_date BETWEEN '2025-10-13' AND '2025-11-02'
        GROUP BY T2.collection_time
        ORDER BY COUNT(T2.collection_time) DESC
        LIMIT 1;
    """
    busiest_time_result = conn.execute(busiest_time_sql, (target_item_id, vendor_id)).fetchone()
    busiest_time = busiest_time_result[0] if busiest_time_result else 'N/A'

    # 3c. Predicted Daily Demand During Peak Time (Safely handled if busiest_time is 'N/A')
    total_days = 21 
    predicted_daily_demand = 0.0 # Initialize to 0.0

    if busiest_time != 'N/A':
        daily_peak_orders_sql = """
            SELECT COUNT(order_id)
            FROM orders
            WHERE order_date BETWEEN '2025-10-13' AND '2025-11-02'
              AND collection_time = ?;
        """
        total_orders_at_peak = conn.execute(daily_peak_orders_sql, (busiest_time,)).fetchone()[0]
        predicted_daily_demand = round(total_orders_at_peak / total_days, 2)

    conn.close() 

    # --- Pass Data to Template ---
    return render_template('vendor_analytics_forecasting.html', 
        historical_data=historical_data,
        target_item_name=target_item_name,  
        menu_items=menu_items,              
        selected_item_id=selected_item_id,  
        predicted_demand=int(predicted_demand), 
        busiest_time=busiest_time,
        predicted_daily_demand=predicted_daily_demand
    )

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

