'''----------------------- LIBRARIES -------------------------- '''
import os
import mysql.connector
from mysql.connector import Error

'''----------------------- FUNCTIONS -------------------------- '''

try:
    connection = mysql.connector.connect(host='localhost', database='mydb', user='root', password=os.environ.get("MYSQL_PASSWORD"), use_pure=True)
    
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        print()
        
        table_name="DISEASE"
        sql_select_Query = "select * from "+table_name
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        print("Total number of rows in "+table_name+" is: ", cursor.rowcount)
        
        print("\nPrinting each "+table_name+" record:\n")
        for row in records:
            print("• Disease id = ", row[0], )
            print("• Disease name = ", row[1])
            print("• Pathogen = ", row[2])
            print("• Disease description = ", row[3])
            print()
        
        

except Error as e:
    print("Error while connecting to MySQL", e)
'''    
finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed")'''
        
