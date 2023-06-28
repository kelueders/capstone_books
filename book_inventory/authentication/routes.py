from flask import Blueprint, render_template, request, redirect, url_for, flash
from book_inventory.forms import UserLoginForm
from book_inventory.models import User, db

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    userform = UserLoginForm()

    try:
        if request.method == 'POST' and userform.validate_on_submit():
            email = userform.email.data
            username = userform.username.data
            first_name = userform.first_name.data
            last_name = userform.last_name.data
            password = userform.password.data
            print(email, password)

            user = User(email, username, password, first_name, last_name)
            
            db.session.add(user)
            db.session.commit()

            flash(f'You have successfully created a user account {email}', 'user-created')

            return redirect(url_for('site.home'))
        
    except:
        raise Exception('Invalid Form Data. Please check your form.')
    
    return render_template('signup.html', form = userform)

@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    return render_template('signin.html')

