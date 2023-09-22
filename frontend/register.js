function submitForm(event) {
    event.preventDefault();

    toggleRegisterButtonState(true);

    var username = document.getElementById('username').value;
    var email = document.getElementById('email').value;
    var mobileNumber = document.getElementById('mobile-number').value;
    var companyName = document.getElementById('company-name').value;

    if (!validateEmail(email)) {
        displayResponse("Please enter a valid email address!");
        toggleRegisterButtonState(false);
        return;
    }

    if (!validateMobileNumber(mobileNumber)) {
        displayResponse("Please enter a valid mobile number!");
        toggleRegisterButtonState(false);
        return;
    }

    var xhr = new XMLHttpRequest();
    xhr.open('POST', 'https://register.clockhash.com/pre-register', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function () {
        var response = JSON.parse(xhr.responseText);
        if (xhr.readyState == 4 && (xhr.status === 200 || xhr.status === 409)) {
            if ('error' in response) {
                displayResponse('Register failed! ' + response.error);
            } else {
                displayOtpModal();
            }
        } else {
            displayResponse('Register failed! Please try again');
        }
        toggleRegisterButtonState(false);
    };
    xhr.onerror = function() {
        displayResponse('Request failed');
        toggleRegisterButtonState(false);
    };
    xhr.send(JSON.stringify({username: username, email: email, mobile_number: mobileNumber, company_name: companyName}));
}

function verifyOtp(email, otp) {
    toggleOtpSubmitButtonState(true);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', 'https://register.clockhash.com/verify-otp', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function () {
        var response = JSON.parse(xhr.responseText);
        if (xhr.readyState == 4 && xhr.status === 200) {
            if ('message' in response) {
                displayResponse('Registration successful!');
                document.getElementById('register-form').reset();
                closeOtpModal();
            } else {
                displayResponse('Incorrect OTP. Please try again.');
            }
        } else {
            displayResponse('OTP verification failed. Please try again.');
        }
        // Clearing the OTP input box here
        document.getElementById('otpInput').value = '';
        toggleOtpSubmitButtonState(false);
    };
    xhr.onerror = function() {
        displayResponse('Request failed');
        // Clearing the OTP input box here as well, in case of an error
        document.getElementById('otpInput').value = '';
        toggleOtpSubmitButtonState(false);
    };
    xhr.send(JSON.stringify({email: email, otp: otp}));
}

function toggleRegisterButtonState(state) {
    var button = document.querySelector('#register-form button[type="submit"]');
    button.disabled = state;
}

function toggleOtpSubmitButtonState(state) {
    var button = document.querySelector('#otpModal button');
    button.disabled = state;
}

function validateEmail(email) {
    var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
}

function validateMobileNumber(mobileNumber) {
    var re = /^\d{10}$/;
    return re.test(mobileNumber);
}

function displayOtpModal() {
    var modal = document.getElementById('otpModal');
    modal.style.display = 'block';
}

function submitOtp() {
    var otp = document.getElementById('otpInput').value;
    var email = document.getElementById('email').value;
    verifyOtp(email, otp);
}

function closeOtpModal() {
    var modal = document.getElementById('otpModal');
    modal.style.display = 'none';
}

function displayResponse(message) {
    var modal = document.getElementById('responseModal');
    document.getElementById('serverResponse').textContent = message;
    modal.style.display = 'block';
}

function closeResponseModal() {
    var modal = document.getElementById('responseModal');
    modal.style.display = 'none';
}

document.getElementById('register-form').removeEventListener('submit', submitForm);
document.getElementById('register-form').addEventListener('submit', submitForm);

