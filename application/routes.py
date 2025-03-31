from flask import render_template, url_for, request, redirect, session

from application import app
from application.data_access import insert_member, get_all_members, get_password_by_username
from application.sample_data import top_reads, all_blogs
from application.data_access import insert_member, get_password

import bcrypt



@app.route('/')
@app.route('/home')
def home():
    # session['loggedIn'] = False
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/meet-GT-members')
def meet_members():
    if not session.get('loggedIn'):
        return render_template('login.html', title="Login", message="You must be logged in to see this content.")
    users = get_all_members()
    return render_template('members.html', title='Meet GT Members', users=users)


@app.route('/join', methods=['GET', 'POST'])
def join():
    error_message = None
    if request.method == 'POST':
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        location = request.form['location']

        return_string = insert_member(first_name, last_name, username, email, password, location)

        return redirect(url_for('home'))  # redirect on success

    return render_template('join.html', error_message=error_message)


@app.route('/blog')
def blog():
    return render_template('blog.html', top_reads=top_reads, all_blogs=all_blogs)


@app.route('/blog/<blog_id>')
def blog_detail(blog_id):
    blog = next((b for b in all_blogs if b['id'] == blog_id), None)
    return render_template('blog_detail.html', title=blog['title'], blog=blog)


@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form['email']
    return render_template('thank_you.html', title='Thank You', email=email)


@app.route('/events')
def events():
    if not session.get('loggedIn'):
        return render_template('login.html', title="Login", message="You must be logged in to see this content.")
    return render_template('events.html', title='Events')


@app.route('/resources')
def resources():
    return render_template('resources.html', title='Resources')


@app.route('/login', methods=['POST', 'GET'])
def login():
    message = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')  # encode the user input.

        result = get_password(username)

        if result:
            stored_password = result['password']
            if bcrypt.checkpw(password, stored_password):
                print('password matched')
                session['username'] = username
                session['loggedIn'] = True
                session['role'] = 'Member'
                message = 'Login Successful!'
                return redirect(url_for('home'))
            else:
                return render_template('login.html', title="Login", message="Incorrect password.")
        else:
            return render_template('login.html', title="Login", message="User not found.")

    return render_template('login.html', title="Login", message=message)

@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    session.pop('role', None)
    session['loggedIn'] = False
    return redirect(url_for('home'))


