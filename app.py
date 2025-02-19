from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Secret key for session management - use environment variable
app.secret_key = os.environ.get('SECRET_KEY', 'default-secret-key')

# Rate limiter to prevent abuse
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Email configuration
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME=os.environ.get('MAIL_USERNAME'),
    MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD'),
    MAIL_DEFAULT_SENDER=os.environ.get('MAIL_DEFAULT_SENDER')
)

mail = Mail(app)

def validate_email_input(email, name, message):
    """Validate email form inputs"""
    if not all([email, name, message]):
        return False
    # Basic email validation
    if '@' not in email or '.' not in email:
        return False
    return True

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/hello', methods=['GET'])
@limiter.limit("5 per minute")
def hello_api():
    return jsonify({'message': 'Hello from Flask!'})

@app.route('/api/submit', methods=['POST'])
@limiter.limit("10 per minute")
def submit():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'status': 'error', 'message': 'No data provided'}), 400
        return jsonify({'status': 'success', 'data': data})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/send_email', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def send_email():
    if request.method == 'POST':
        try:
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip()
            phone = request.form.get('phone', 'Not Provided').strip()
            subject = request.form.get('subject', 'Contact Form Message').strip()
            message = request.form.get('message', '').strip()

            # Validate inputs
            if not validate_email_input(email, name, message):
                flash('Please fill in all required fields correctly.', 'error')
                return redirect(url_for('home', _anchor='contact'))

            msg_body = f"""
            New message from your portfolio website:
            
            Name: {name}
            Email: {email}
            Phone: {phone}
            Subject: {subject}
            
            Message:
            {message}
            """

            msg = Message(
                subject=f"Portfolio Contact: {subject}",
                recipients=[os.environ.get('RECIPIENT_EMAIL', 'girijalasravani09@gmail.com')],
                body=msg_body,
                reply_to=email
            )
            
            mail.send(msg)
            flash('Message sent successfully!', 'success')
            return redirect(url_for('home', _anchor='contact'))
        
        except Exception as e:
            app.logger.error(f"Error sending email: {e}")
            flash('Failed to send message. Please try again.', 'error')
            return redirect(url_for('home', _anchor='contact'))
    
    return redirect(url_for('home'))

@app.errorhandler(429)
def ratelimit_handler(e):
    """Handle rate limit exceeded"""
    flash("Too many requests. Please try again later.", "error")
    return redirect(url_for('home'))

if __name__ == '__main__':
    # Get port from environment variable for Render deployment
    port = int(os.environ.get('PORT', 5000))
    # Run the app
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('FLASK_DEBUG', 'False').lower() == 'true') 
