from flask import render_template, url_for, request, redirect, session

from application import app
import os

from application.sample_data import top_reads, all_blogs


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


@app.route('/join')
def join():
    return render_template('join.html', title='Join')


@app.route('/blog')
def blog():
    return render_template('blog.html', title='Blog', top_reads=top_reads, all_blogs=all_blogs)


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


@app.route('/login', methods=['GET', 'POST'])
def login():
    # app.logger.debug("Start of login")
    if request.method == 'POST':
        session['username'] = request.form['username']
        # app.logger.debug("Username is: " + session['username'])
        session['loggedIn'] = True
        session['role'] = 'Member'
        return redirect(url_for('home'))
    return render_template('login.html', title="Login")

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = mydb.cursor(dictionary=True)
        sql = "SELECT password FROM member WHERE username = %s"
        cursor.execute(sql, (username,))
        result = cursor.fetchone()

        if result:
            stored_password = result['password']
            if bcrypt.checkpw(password.encode('utf-8'), stored_password):
                return "Login successful"
            else:
                return "Login failed"
        else:
            return "User not found"


@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    session.pop('role', None)
    session['loggedIn'] = False
    return redirect(url_for('home'))
