# Car Order Web Application

This Flask-based web application allows users to order cars by selecting various options such as make, model, variant, color, accessories, and quantity. Users can also enter their personal details such as email and phone number. The order details are saved to an Excel file and a confirmation email is sent to the user.

## Features

- Select a car's make, model, variant, accessories, and color.
- View a summary of the selected order.
- Save order details to an Excel file (`user_selections.xlsx`).
- Send a confirmation email to the user after placing an order.
- Admin login to view the customer order dashboard.

## Requirements

- Python 3.6 or higher
- Flask
- pandas
- openpyxl
- smtplib (for email functionality)

You can install the required packages by running:

```bash
pip install -r requirements.txt


## Setup Instructions

1. **Clone the repository**:
    ```bash
    git clone git clone https://github.com/mbaldua30/chatbot.git
    cd car-order-webapp
    ```

2. **Create a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```


5. **Run the application:**
```bash
    python chatbot.py
```

6. **Access the application**:
    Open your web browser and go to `http://127.0.0.1:5000`.

## File Structure

- `chatbot.py`: Main Flask application code.
- `car_data.xlsx`: Excel file containing the car data (make, model, variant, etc.).
- `user_selections.xlsx`: Excel file where the user orders are stored.
- `templates/`: Folder containing the HTML templates (index.html, select_*.html, user_info.html, etc.).
- `static/`: Folder containing static files like CSS, images, and JavaScript.

## How It Works

1. **Select Car Options**: The user is prompted to select a car make, model, variant, color, accessories, and quantity.
2. **Enter Personal Details**: After filling in the order, the user enters their personal details (email and phone).
3. **Save Order**: The order is saved to `user_selections.xlsx`.
4. **Send Confirmation Email**: A confirmation email is sent to the user.
5. **Admin Dashboard**: Admins can log in to view the customer orders and update the order status.
