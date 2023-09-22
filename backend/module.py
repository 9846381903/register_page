# importing binaries
from flask import Flask, request, jsonify
from flask_cors import CORS
from pre_register import register, verify_otp

# initializing the Flask application
app = Flask(__name__)
CORS(app)

# endpoint for registering username
@app.route('/pre-register', methods=['POST'])
def call_register():
    username = request.json.get('username')
    email = request.json.get('email')
    mobile_number = request.json.get('mobile_number')
    company_name = request.json.get('company_name')
    return register(username, email, mobile_number, company_name)

# endpoint for verifying OTP
@app.route('/verify-otp', methods=['POST'])
def call_verify_otp():
    email = request.json.get('email')
    otp = request.json.get('otp')
    if verify_otp(email, otp):
        return {'message': 'OTP verification successful'}
    else:
        return {'error': 'Incorrect OTP'}

# main function for enabling port
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
