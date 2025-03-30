from flask import render_template, url_for, request, redirect, session

from application import app
from application.data_access import insert_member, get_all_members, get_password_by_username
from application.sample_data import top_reads, all_blogs
import bcrypt



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
    if not session.get('loggedIn'):
        return render_template('login.html', title="Login", message="You must be logged in to see this content.")
    users = get_all_members()
    return render_template('members.html', title='Meet GT Members', users=users)


@app.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        location = request.form['location']

        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        insert_member(firstname, lastname, username, email, hashed_pw, location)

        session['username'] = username
        session['loggedIn'] = True
        session['role'] = 'Member'

        return redirect(url_for('home'))
    return render_template('join.html', title='Join')


@app.route('/blog')
def blog():
    return render_template('blog.html', title='Girl Tech Blog', top_reads=top_reads, all_blogs=all_blogs)


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


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     # app.logger.debug("Start of login")
#     if request.method == 'POST':
#         session['username'] = request.form['username']
#         # app.logger.debug("Username is: " + session['username'])
#         session['loggedIn'] = True
#         session['role'] = 'Member'
#         return redirect(url_for('home'))
#     return render_template('login.html', title="Login")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        result = get_password_by_username(username)

        if result:
            stored_password = result['password']
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                session['username'] = username
                session['loggedIn'] = True
                session['role'] = 'Member'
                return redirect(url_for('home'))
            else:
                return render_template('login.html', title="Login", message="Incorrect password.")
        else:
            return render_template('login.html', title="Login", message="User not found.")
    return render_template('login.html', title="Login")

@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    session.pop('role', None)
    session['loggedIn'] = False
    return redirect(url_for('home'))
