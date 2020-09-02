import mysql.connector
from mysql.connector import Error

username='sinems_hn'

try:
    connection = mysql.connector.connect(host='127.0.0.1',
                                                        user='root',
                                                        
                                                        password='elso3306',
                                                        database='labinstagram',
                                                        buffered=True)
    cursor=connection.cursor()
        
except Error as e:
    print("Error while connecting to MySQL", e)
print(username)
sql="SELECT password FROM users WHERE name = '{}';".format(username)
cursor.execute(sql)
m=cursor.fetchone()
connection.commit()
passwor= m[0]
print(passwor)
print(username)