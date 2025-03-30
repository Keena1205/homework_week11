import bcrypt
from flask import render_template, url_for, request, redirect, session

from application import app
import os

from application.data_access import insert_member, get_password


# from application.sample_data import top_reads, all_blogs


@app.route('/')
@app.route('/home')
def home():
    session['loggedIn'] = False
    return render_template('home.html', title='Home')


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/meet-GT-members')
def meet_members():
    # Sort login / session code here - refer to line 100 on Victoria's code
    if not session.get('loggedIn'):
        return render_template('login.html', title="Login", message="You must be logged in to see this content.")
    return render_template('members.html', title='Meet GT Members')


@app.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'POST':
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        location = request.form['location']

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        return_string = insert_member(first_name, last_name, username, email, hashed_password, location)
        return redirect(url_for('join'))

    return render_template('join.html', title='Join')


# @app.route('/blog')
# def blog():
#     return render_template('blog.html', title='Blog', top_reads=top_reads, all_blogs=all_blogs)


@app.route('/blog/<blog_id>')
def blog_detail(blog_id):
    return render_template('blog.html', title='Blog')


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
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        result = get_password(username)

        if result:
            stored_password = result['password']
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                return "Login successful"
            else:
                return "Login failed"
        else:
            return "User not found"

    return render_template('login.html', title="Login")


@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    session.pop('role', None)
    session['loggedIn'] = False
    return redirect(url_for('home'))
