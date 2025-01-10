from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from collections import defaultdict

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Make sure to set a secret key for session handling

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        selected_date = request.form.get('selected_date')
        # Save the selected date or process it as needed
        print(f"Selected date: {selected_date}")  # You can save this to a database or file
        
        # Optionally, store the selected date in the session
        session['selected_date'] = selected_date
        return redirect(url_for('confirmation'))  # Redirect to a confirmation page or somewhere else
    
    return render_template('index.html')

@app.route('/confirmation')
def confirmation():
    selected_date = session.get('selected_date', None)
    if selected_date:
        return f"You have selected: {selected_date}"
    else:
        return "No date selected."

if __name__ == '__main__':
    app.run(debug=True)
