from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from collections import defaultdict

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'


# Read the Excel file into a DataFrame
df = pd.read_excel('car_data.xlsx')

# Initialize a defaultdict to hold the nested dictionary
car_data = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))

# Group the data by 'Brand', 'Model', and 'Type'
for _, row in df.iterrows():
    brand = row['Make']
    model = row['Model']
    car_type = row['Variant']
    color = row['Color']
    accessories = row['Accessory'].split(', ')  # Assuming accessories are separated by commas

    # Fill the nested dictionary
    car_data[brand][model][car_type] = {
        'colors': car_data[brand][model][car_type].get('colors', []) + [color],
        'accessories': accessories
    }

# Convert defaultdict to regular dict for a cleaner output
car_data = {brand: {model: {car_type: dict(details) for car_type, details in models.items()}
                      for model, models in brand_models.items()}
               for brand, brand_models in car_data.items()}

# Print the nested data
# print(car_data)



# Path to the Excel file
EXCEL_FILE_PATH = 'user_selections.xlsx'


def save_to_excel(user_data):
    # Initialize the DataFrame
    df_new = pd.DataFrame([user_data])
    
    if os.path.exists(EXCEL_FILE_PATH):
        # Load existing data to determine the next ID
        df_existing = pd.read_excel(EXCEL_FILE_PATH)
        
        # Determine the next ID
        if not df_existing.empty:
            next_id = df_existing['ID'].max() + 1
        else:
            next_id = 1
        
        # Assign the next ID to the new data
        df_new['ID'] = next_id

        df_new = df_new[['ID','make', 'model', 'variant', 'accessory', 'color', 'quantity', 'email', 'phone']]

        # Append the new data
        with pd.ExcelWriter(EXCEL_FILE_PATH, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
            df_new.to_excel(writer, index=False, header=False, startrow=writer.sheets['Sheet1'].max_row)
    else:
        
        # Assign ID starting from 1 if the file doesn't exist
        df_new['ID'] = 1
        df_new = df_new[['ID','make', 'model', 'variant', 'accessory', 'color', 'quantity', 'email', 'phone']]

        
        # Create a new Excel file with the necessary headers
        with pd.ExcelWriter(EXCEL_FILE_PATH, engine='openpyxl') as writer:
            df_new.to_excel(writer, index=False, header=True)




def send_order_email(order_details):
    sender_email = "madhusudanbaldua@gmail.com"  # Replace with your email
    receiver_email = order_details['email']  # User's email from the order details
    password = "bult pohf puqg bdda"  # Replace with your email password

    subject = "New Car Order Received"
    body = f"""
    New car order received with the following details:

    Make: {order_details['make']}
    Model: {order_details['model']}
    Variant: {order_details['variant']}
    Accessory: {order_details['accessory']}
    Color: {order_details['color']}
    Quantity: {order_details['quantity']}
    Email: {order_details['email']}
    Phone: {order_details['phone']}
    
    Thank you for your order.
    """

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Load data from Excel
def load_customer_data():
    df = pd.read_excel('user_selections.xlsx')
    return df.to_dict(orient='records')


# To store the user's choices
user_selection = {
    'make': None,
    'model': None,
    'variant': None,
    'accessory': None,
    'color': None,
    'quantity': None
}

# Helper function for validating selections
def validate_selection(selection, options):
    return selection in options

@app.route('/')
def home():
    return render_template('index.html', data=car_data)

@app.route('/select_make', methods=['POST'])
def select_make():
    make = request.form.get('make')
    if validate_selection(make, car_data.keys()):
        user_selection['make'] = make
        return redirect(url_for('select_model'))
    else:
        return render_template('error.html', message="Car make not available. Please choose a valid make.")


@app.route('/select_model', methods=['GET', 'POST'])
def select_model():
    make = user_selection.get('make')
    if not make:
        return redirect(url_for('home'))

    if request.method == 'POST':
        model = request.form.get('model')
        if validate_selection(model, car_data[make].keys()):
            user_selection['model'] = model
            return redirect(url_for('select_variant'))
        return render_template('error.html', message="Invalid model selected.")

    return render_template('select_model.html', make=make, models=car_data[make].keys())

@app.route('/select_variant', methods=['GET', 'POST'])
def select_variant():
    make = user_selection.get('make')
    model = user_selection.get('model')
    if not make or not model:
        return redirect(url_for('home'))

    if request.method == 'POST':
        variant = request.form.get('variant')
        if validate_selection(variant, car_data[make][model].keys()):
            user_selection['variant'] = variant
            return redirect(url_for('select_accessory'))
        return render_template('error.html', message="Invalid variant selected.")

    return render_template('select_variant.html', make=make, model=model, variants=car_data[make][model].keys())

@app.route('/select_accessory', methods=['GET', 'POST'])
def select_accessory():
    make = user_selection.get('make')
    model = user_selection.get('model')
    variant = user_selection.get('variant')
    if not make or not model or not variant:
        return redirect(url_for('home'))

    if request.method == 'POST':
        accessory = request.form.get('accessory')
        if validate_selection(accessory, car_data[make][model][variant]['accessories']):
            user_selection['accessory'] = accessory
            return redirect(url_for('select_color'))
        return render_template('error.html', message="Invalid accessory selected.")

    return render_template('select_accessory.html', accessories=car_data[make][model][variant]['accessories'])

@app.route('/select_color', methods=['GET', 'POST'])
def select_color():
    make = user_selection.get('make')
    model = user_selection.get('model')
    variant = user_selection.get('variant')
    if not make or not model or not variant:
        return redirect(url_for('home'))

    if request.method == 'POST':
        color = request.form.get('color')
        if validate_selection(color, car_data[make][model][variant]['colors']):
            user_selection['color'] = color
            return redirect(url_for('select_quantity'))
        return render_template('error.html', message="Invalid color selected.")

    return render_template('select_color.html', colors=car_data[make][model][variant]['colors'])

@app.route('/select_quantity', methods=['GET', 'POST'])
def select_quantity():
    if request.method == 'POST':
        quantity = request.form.get('quantity')
        if quantity and quantity.isdigit():
            user_selection['quantity'] = int(quantity)
            print(quantity)
            # Redirect to user_info to collect email and phone
            return redirect(url_for('user_info'))
        return render_template('error.html', message="Invalid quantity entered.")

    return render_template('select_quantity.html')

@app.route('/user_info', methods=['GET', 'POST'])
def user_info():
    if request.method == 'POST':
        email = request.form.get('email')
        phone = request.form.get('phone')
        user_selection['email'] = email
        user_selection['phone'] = phone
        print(email)
        print(phone)

        # Save order details to Excel
        save_to_excel(user_selection)

        # Send the order details via email
        send_order_email(user_selection)

        return redirect(url_for('order_summary'))
    return render_template('user_info.html')

@app.route('/order_summary')
def order_summary():
    return render_template('order_summary.html', selection=user_selection)


@app.route('/dashboard')
def dashboard():
    # Simple authentication check, for example purposes only
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))
    customer_data = load_customer_data()
    print(customer_data)
    return render_template('dashboard.html', customer_data=customer_data) 


 # Ensure you have a 'dashboard.html' file

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'password123':  # Replace with secure logic
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid credentials. Please try again.")
    return render_template('login.html')


@app.route('/logout', methods=['POST'])
def logout():
    session.clear()  # Clears all session data
    return redirect(url_for('login')) 


@app.route('/update_order_status', methods=['POST'])
def update_order_status():
    row_id = request.form['row_id']
    print(row_id)
    new_status = request.form['order_status']
    print(new_status)

    # Load your Excel file
    df = pd.read_excel('user_selections.xlsx')

    # Update the order status
    df.loc[df['ID'] == int(row_id), 'OrderStatus'] = new_status

    # Save the updated Excel file
    df.to_excel('user_selections.xlsx', index=False)

    return redirect(url_for('dashboard'))



if __name__ == '__main__':
    app.run(debug=True)
