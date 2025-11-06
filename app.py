#INITIAL SETUP!!!
#***********************************************************
# Main Application File: app.py
#===========================================================
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = '12345'  # Needed for session management # I do not know what for
# End of Main Application File
#===========================================================

# Database connection function
#===========================================================
def get_db_connection():
    conn = sqlite3.connect('ordering.db')
    conn.row_factory = sqlite3.Row
    return conn
# End of Database connection function
#===========================================================
#End of INITIAL SETUP!!!
#***********************************************************



#LOGIN AND NEW USER PAGES!!!
#***********************************************************
#Login Page - Where everything starts
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

#New Customer Registration Page
#===========================================================



#End of New Customer Registration Page
#===========================================================
#End of LOGIN AND NEW USER PAGES!!!
#***********************************************************



#Now we move to different user sections!!!!
 
#ADMIN SECTION!!!
#************************************************************
#Admin Home Page
#===========================================================
@app.route('/admin_home')
def admin_home():
    if session.get('user_type') != 'admin':
        return redirect(url_for('login'))
    conn = get_db_connection()
    vendors = conn.execute('SELECT * FROM vendor').fetchall()
    conn.close()
    return render_template('vendor_admin.html', vendors=vendors)
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
            return render_template('new_vendor.html', error='Passwords do not match')

         # Insert new vendor into the database
        
        conn.execute('INSERT INTO vendor (vendor_id, name, location, phone_number, email, username, password, bank_name, account_number, branch_code) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',

                     (new_vendor_id, name, location, phone_number, email, username, password, bank_name, account_number, branch_code))
        conn.commit()
        conn.close()

        return redirect(url_for('admin_home'))

    return render_template('new_vendor.html')

#End of Add vendor page
#===============================================================
#End of ADMIN SECTION!!!
#***************************************************************



#CUSTOMER SECTION!!!
#***************************************************************
#Customer home page 
#================================================================
@app.route('/customer_home')
def customer_home():
    if session.get('user_type') != 'customer':
        return redirect(url_for('login'))

    conn = get_db_connection()
    vendors = conn.execute('SELECT * FROM vendor').fetchall()
    conn.close()
    return render_template('customer-main.html', vendors=vendors)
    
#End of Customer home page
#================================================================

#Menu section
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
    return render_template('menu.html', menu_items=menu_items, selected_vendor=selected_vendor, categories = categories)

#End of Menu section
#================================================================


#End of CUSTOMER SECTION!!!
#***************************************************************


#VENDOR SECTION!!!
#***************************************************************
# Vendor home page
#===============================================================
@app.route('/vendor_home')
def vendor_home():
    if session.get('user_type') != 'vendor':
        return redirect(url_for('login'))
    return render_template('vendor_main.html')
#End of Vendor home page
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



