from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_mail import Mail, Message
import os

app = Flask(__name__)

# Secret key for session management
app.secret_key = 'your-secret-key-here'  

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

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/hello', methods=['GET'])
def hello_api():
    return jsonify({'message': 'Hello from Flask!'})

@app.route('/api/submit', methods=['POST'])
def submit():
    data = request.get_json()
    # Process the data here
    return jsonify({'status': 'success', 'data': data})

@app.route('/send_email', methods=['GET', 'POST'])
def send_email():
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']
            phone = request.form.get('phone', 'Not Provided')
            subject = request.form.get('subject', 'Contact Form Message')
            message = request.form['message']

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
                recipients=['girijalasravani09@gmail.com'],
                body=msg_body,
                reply_to=email
            )
            
            mail.send(msg)
            flash('Message sent successfully!', 'success')
            return redirect(url_for('home', _anchor='contact'))
        
        except Exception as e:
            print(f"Error sending email: {e}")
            flash('Failed to send message. Please try again.', 'error')
            return redirect(url_for('home', _anchor='contact'))
    
    return redirect(url_for('home'))

if __name__ == '__main__':
    # Get port from environment variable for Render deployment
    port = int(os.environ.get('PORT', 5000))
    # Run the app on 0.0.0.0 to accept external connections
    app.run(host='0.0.0.0', port=port, debug=False) 
