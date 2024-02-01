import mysql.connector
from mysql.connector import errorcode

try:
  cnx = mysql.connector.connect(user='root',password='root',
                                database='liordb')
  print(cnx.get_server_info())
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
# TIKUN

if cnx and cnx.is_connected():

    with cnx.cursor() as cursor:

        result = cursor.execute("SELECT * FROM users WHERE user_id = '%s' AND password = '%s'")

        rows = cursor.fetchall()

        for rows in rows:

            print(rows)

    cnx.close()

else:

    print("Could not connect")