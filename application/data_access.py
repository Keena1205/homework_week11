import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database="girl_tech_blog")

# def hash_password(password):
#     salt = bcrypt.gensalt()
#     hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
#     return hashed_password
#
# password = "moRan4re@34"
# hashed_password = hash_password(password)



def insert_member(firstname, lastname, username, email, password, location):
    cursor = mydb.cursor()
    sql = "INSERT INTO member (firstname, lastname, username, email, password, Location) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (firstname, lastname, username, email, password, location)
    cursor.execute(sql, values)
    mydb.commit()
    cursor.close()


def get_all_members():
    cursor = mydb.cursor(dictionary=True)
    sql = "SELECT username, location FROM member"
    cursor.execute(sql)
    members = cursor.fetchall()
    cursor.close()
    return members


def get_password_by_username(username):
    cursor = mydb.cursor(dictionary=True)
    sql = "SELECT password FROM member WHERE username = %s"
    cursor.execute(sql, (username,))
    result = cursor.fetchone()
    cursor.close()
    return result


















# @app.route('/register', methods=['POST'])
# def register():
#     if request.method == 'POST':
#         first_name = request.form['first_name']
#         last_name = request.form['last_name']
#         username = request.form['username']
#         email = request.form['email']
#         password = request.form['password']
#         location = request.form['location']
#
#         hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
#
#         try:
#             cursor = mydb.cursor()
#             sql = "INSERT INTO member (firstname, lastname, username, email, password, location) VALUES (%s, %s, %s, %s, %s, %s)"
#             val = (first_name, last_name, username, email, hashed_password, location) #_
#             cursor.execute(sql, val)
#             mydb.commit()
#             return "Registration successful!"
#         except mysql.connector.Error as err:
#             return f"Error: {err}"
#         finally:
#             cursor.close()
#
#
#
# @app.route('/login', methods=['POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#
#         cursor = mydb.cursor(dictionary=True)
#         sql = "SELECT password FROM member WHERE username = %s"
#         cursor.execute(sql, (username,))
#         result = cursor.fetchone()
#
#         if result:
#             stored_password = result['password']
#             if bcrypt.checkpw(password.encode('utf-8'), stored_password):
#                 return "Login successful"
#             else:
#                 return "Login failed"
#         else:
#             return "User not found"
#
# @app.route('/')
# def index():
#     return """
#     <h2>Registration</h2>
#     <form action="/register" method="post">
#         First Name: <input type="text" name="first_name"><br>
#         Last Name: <input type="text" name="last_name"><br>
#         Username: <input type="text" name="username"><br>
#         Email: <input type="email" name="email"><br>
#         Password: <input type="password" name="password"><br>
#         Location: <input type="text" name="location"><br>
#         <input type="submit" value="Register">
#     </form>
#
#     <h2>Login</h2>
#     <form action="/login" method="post">
#         Username: <input type="text" name="username"><br>
#         Password: <input type="password" name="password"><br>
#         <input type="submit" value="Login">
#     </form>
#     """