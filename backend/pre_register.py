# importing binaries
import mysql.connector as c
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random

# global variable to store otps and user data
otp_storage = {}

def register(username, email, mobile_number, company_name=None):
    if not username or not email or not mobile_number:
        return {'error': 'Username, email, and mobile number are required'}
    try:
        create_database()
        create_table()
        if username_exists(username):
            return {'error': 'Username already taken'}
        if email_exists(email):
            return {'error': 'Email already taken'}
        if mobile_number_exists(mobile_number):
            return {'error': 'Mobile number already taken'}
        
        sender_email = os.environ.get('EMAIL_ID')
        sender_password = os.environ.get('SMTP_TOKEN')
        subject = 'OTP Request'
        otp = generate_otp()
        email_content = load_email_template_with_otp(otp, username)
        send_email(sender_email, sender_password, email, subject, email_content, mime_type='html')
        
        user_data = {
            'username': username,
            'email': email,
            'mobile_number': mobile_number,
            'company_name': company_name
        }
        otp_storage[email] = {
            'user_data': user_data,
            'otp': otp
        }
        return {'message': 'OTP sent to email for verification'}
    except ValueError as e:
        return {'error': str(e)}

def load_email_template_with_otp(otp, username):
    with open('template.html', 'r') as file:
        template = file.read()
    template_with_username = template.replace('Hello User,', f'Hello {username},')
    return template_with_username.replace('764909', str(otp))

def create_database():
    connect = c.connect(host=os.environ.get('DB_HOST'),
                        user=os.environ.get('DB_USER'),
                        password=os.environ.get('DB_PASSWORD'))
    cursor = connect.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS clouddash")
    connect.commit()
    cursor.close()
    connect.close()

def create_table():
    connect = get_database_connection()
    cursor = connect.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `register` (`USERNAME` VARCHAR(100), `EMAIL` VARCHAR(100), `MOBILE_NUMBER` VARCHAR(100), `COMPANY_NAME` VARCHAR(100))")
    connect.commit()
    cursor.close()
    connect.close()

def username_exists(username):
    connect = get_database_connection()
    cursor = connect.cursor()
    cursor.execute("SELECT USERNAME FROM `register` WHERE USERNAME=%s", (username,))
    existing_user = cursor.fetchone()
    cursor.close()
    connect.close()
    return existing_user is not None

def email_exists(email):
    connect = get_database_connection()
    cursor = connect.cursor()
    cursor.execute("SELECT EMAIL FROM `register` WHERE EMAIL=%s", (email,))
    existing_email = cursor.fetchone()
    cursor.close()
    connect.close()
    return existing_email is not None

def mobile_number_exists(mobile_number):
    connect = get_database_connection()
    cursor = connect.cursor()
    cursor.execute("SELECT MOBILE_NUMBER FROM `register` WHERE MOBILE_NUMBER=%s", (mobile_number,))
    existing_mobile_number = cursor.fetchone()
    cursor.close()
    connect.close()
    return existing_mobile_number is not None

def store_user(username, email, mobile_number, company_name=None, otp_verified=False):
    if not otp_verified:
        return {'error': 'OTP verification required'}
    try:
        create_database()
        create_table()
        connect = get_database_connection()
        cursor = connect.cursor()
        cursor.execute("INSERT INTO `register` (`USERNAME`, `EMAIL`, `MOBILE_NUMBER`, `COMPANY_NAME`) VALUES (%s, %s, %s, %s)", (username, email, mobile_number, company_name))
        connect.commit()
        cursor.close()
        connect.close()
        return {'message': 'User information stored in the database'}
    except Exception as e:
        return {'error': str(e)}

def get_database_connection():
    connect = c.connect(host=os.environ.get('DB_HOST'),
                        user=os.environ.get('DB_USER'),
                        password=os.environ.get('DB_PASSWORD'),
                        database='clouddash')
    return connect

def generate_otp():
    return str(random.randint(100000, 999999))

def send_email(sender_email, sender_password, recipient_email, subject, message_content, mime_type='plain'):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message_content, mime_type))
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)
    server.send_message(msg)
    server.quit()

def verify_otp(email, otp):
    stored_data = otp_storage.get(email)
    if stored_data and stored_data['otp'] == otp:
        del otp_storage[email]
        store_user(**stored_data['user_data'], otp_verified=True)

        sender_email = os.environ.get('EMAIL_ID')
        sender_password = os.environ.get('SMTP_TOKEN')
        subject = 'Pre-registration Confirmation for Cloudash'

        # Reading content from feedback.html
        with open('feedback.html', 'r') as file:
            confirmation_message = file.read()

        send_email(sender_email, sender_password, email, subject, confirmation_message, mime_type='html')

        return True
    else:
        return False

