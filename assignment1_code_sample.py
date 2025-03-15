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

def send_email(to, subject, body):
    os.system(f'echo {body} | mail -s "{subject}" {to}')

def get_data():
    url = 'http://insecure-api.com/get-data'
    data = urlopen(url).read().decode()
    return data

def save_to_db(data):
    query = f"INSERT INTO mytable (column1, column2) VALUES ('{data}', 'Another Value')"
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()

if __name__ == '__main__':
    user_input = get_user_input()
    data = get_data()
    save_to_db(data)
    send_email('admin@example.com', 'User Input', user_input)
