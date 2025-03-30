from flask import render_template, url_for, request, redirect, session
from application import app


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
    # if request.method == 'POST':

    return render_template('members.html', title='Meet GT Members')


@app.route('/join')
def join():
    return render_template('join.html', title='Join')


@app.route('/blog')
def blog():
    return render_template('blog.html', title='Blog')

@app.route('/events')
def events():
    # Sort login / session code here - refer to line 100 on Victoria's code
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


@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    session.pop('role', None)
    session['loggedIn'] = False
    return redirect(url_for('home'))
