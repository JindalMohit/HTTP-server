import mysql.connector
import getpass

password = getpass.getpass('Enter your mysql password: ')
cnx = mysql.connector.connect(user='root', password=password, database='My_http_server')
cursor = cnx.cursor()

query = ("SELECT first_name, last_name, gender FROM user")

cursor.execute(query)

print("\nFormat:\nFirst_name, Last_name, Gender\n")

for (first_name, last_name, gender) in cursor:
  print("{}, {}, {}".format(
    first_name, last_name, gender))

cursor.close()
cnx.close()