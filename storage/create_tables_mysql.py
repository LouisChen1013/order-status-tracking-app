import mysql.connector


db_conn = mysql.connector.connect(
    host="kafka-lab.westus2.cloudapp.azure.com", user="root", password="root", database="events")
db_cursor = db_conn.cursor()
db_cursor.execute(''' 
            CREATE TABLE add_orders
            (id INT NOT NULL AUTO_INCREMENT,
            customer_id VARCHAR(250) NOT NULL,
            order_id VARCHAR(250) NOT NULL,
            restaurant VARCHAR(250) NOT NULL,
            timestamp VARCHAR(100) NOT NULL,
            date_created VARCHAR(100) NOT NULL,
            order_total FLOAT NOT NULL,
            CONSTRAINT add_orders_pk PRIMARY KEY (id))
            ''')
db_cursor.execute(''' 
            CREATE TABLE payments 
            (id INT NOT NULL AUTO_INCREMENT,
            customer_id VARCHAR(250) NOT NULL,
            payment_id VARCHAR(250) NOT NULL,
            restaurant VARCHAR(250) NOT NULL,
            timestamp VARCHAR(100) NOT NULL,
            date_created VARCHAR(100) NOT NULL,
            CONSTRAINT payments PRIMARY KEY (id))
            ''')

db_conn.commit()
db_conn.close()
