import os
import pymysql
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Secure DB configuration: Never hardcode credentials, use environment variables instead
# OWASP A02:2021 - Cryptographic Failures
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'admin'),
    'password': os.getenv('DB_PASSWORD', 'secret123')  # TODO: Replace with environment variables
}

# A03: Injection - Input validation to prevent SQL injection and script injection
def get_user_input():
    user_input = input('Enter your name: ').strip()
    # Ensuring input only contains letters and spaces
    if not re.match(r'^[A-Za-z ]+$', user_input):
        raise ValueError("Invalid input. Only letters and spaces are allowed.")
    return user_input

# Secure email sending using smtplib instead of os.system (Command Injection risk)
# OWASP A03:2021 - Injection
def send_email(to, subject, body):
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(os.getenv("SMTP_SERVER", "smtp.example.com"), 465, context=context) as server:
            server.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASS"))  # Secure email credentials
            message = f"Subject: {subject}\n\n{body}"
            server.sendmail(os.getenv("EMAIL_USER"), to, message)
    except Exception as e:
        print(f"Email sending failed: {e}")
 
# Secure API request by setting a user-agent and handling errors
# OWASP A08:2021 - Software and Data Integrity Failures
def get_data():
    url = 'https://secure-api.com/get-data'  # Changed to HTTPS
    req = Request(url, headers={'User-Agent': 'SecureClient/1.0'})
    try:
        with urlopen(req) as response:
            data = response.read().decode()
    except Exception as e:
        print(f"Failed to fetch data: {e}")
        return None
    return data

# Prevent SQL Injection by using parameterized queries
# OWASP A03:2021 - Injection
def save_to_db(data):
    if not data:
        print("No data to save.")
        return
    try:
        connection = pymysql.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME', 'default_db')
        )
        cursor = connection.cursor()
        query = "INSERT INTO mytable (column1, column2) VALUES (%s, %s)"
        cursor.execute(query, (data, 'Another Value'))
        connection.commit()
    except pymysql.MySQLError as e:
        print(f"Database error: {e}")
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    user_input = get_user_input()
    data = get_data()
    save_to_db(data)
    send_email('admin@example.com', 'User Input', user_input)
