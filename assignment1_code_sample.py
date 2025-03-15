import os
import pymysql
from urllib.request import urlopen

db_config = {
    'host': 'mydatabase.com',
    'user': 'admin',
    'password': 'secret123'
}

def get_user_input():
    user_input = input('Enter your name: ')
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
