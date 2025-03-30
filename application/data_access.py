import traceback

import mysql.connector
import bcrypt


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database="girl_tech_member_id")


def insert_member(firstname, lastname, username, email, password, location):
  return_string = "Registration unsuccessful"
  cursor = None
  try:
    cursor = mydb.cursor()
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
    sql = "INSERT INTO member (firstname, lastname, username, email, password, location) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (firstname, lastname, username, email, hashed_password, location)
    cursor.execute(sql, val)
    mydb.commit() #saving
    return_string = (cursor.rowcount, "record inserted.")
    return return_string

  except mysql.connector.Error as err:
    print(f"Error: {err}")
    return err

  except Exception as e:
    print(traceback.format_exc())
    return e

  finally:
    cursor.close()


def get_password(username):
    cursor = mydb.cursor(dictionary=True)
    sql = "SELECT password FROM member WHERE username = %s"
    cursor.execute(sql, (username,))
    result = cursor.fetchone()
    return result