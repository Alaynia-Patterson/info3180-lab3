from app import app
from flask import render_template, request, redirect, url_for, flash
from app.forms import ContactForm
from app import mail  # Import the mail instance
from flask_mail import Message  # Import the Message class from Flask-Mail

###
# Routing for your application.
###


@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")
    

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()  # Create the form instance
    if form.validate_on_submit():  # Check if the form is validated on submission
        # Extract form data
        name = form.name.data
        email = form.email.data
        subject = form.subject.data
        message = form.message.data

        # Create a message instance using form data
        msg = Message(
            subject,  # Use the subject provided by the user
            sender=("Your Name", "from@example.com"),  
            recipients=["to@example.com"]  
        )
        
        # Set the email body
        msg.body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        
        # Send the email
        try:
            mail.send(msg)
            flash(f'Message sent successfully from {email}!', 'success')
            return redirect(url_for('contact'))  # Redirect to the contact page after success
        except Exception as e:
            flash(f"An error occurred while sending the email: {str(e)}", 'danger')
    else:
        # Inspect and flash form errors
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                flash(f"Error in {fieldName}: {err}", 'danger')

    # If the form is not validated, render the contact form again
    return render_template('contact.html', form=form)


###
# The functions below should be applicable to all Flask apps.
###


# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404

