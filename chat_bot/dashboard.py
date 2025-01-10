from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

# Load data from Excel
def load_customer_data():
    df = pd.read_excel('user_selections.xlsx')
    return df.to_dict(orient='records')

@app.route('/')
def index():
    # Load customer data
    customer_data = load_customer_data()
    return render_template('dashboard.html', customer_data=customer_data)

if __name__ == '__main__':
    app.run(debug=True)
