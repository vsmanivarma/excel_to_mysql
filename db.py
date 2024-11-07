import pandas as pd
import mysql.connector
from mysql.connector import Error
import os


def upload_data_to_mysql(file_path, table_name, host, user, password, database):
	try:

		file_extension = os.path.splitext(file_path)[1].lower()

		if file_extension == '.xlsx' or file_extension == '.xls':

			data = pd.read_excel(file_path)
		elif file_extension == '.csv':

			data = pd.read_csv(file_path)
		else:
			print("Unsupported file format. Only Excel (.xlsx, .xls) and CSV (.csv) are supported.")
			return


		connection = mysql.connector.connect(
			host=host,
			user=user,
			password=password,
			database=database
		)

		if connection.is_connected():
			cursor = connection.cursor()
			create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                date DATE,
                company_name VARCHAR(100),
                status VARCHAR(50),
                mobile_number VARCHAR(15),
                job_portal VARCHAR(50)
            );
            """
			cursor.execute(create_table_query)
			placeholders = ", ".join(["%s"] * len(data.columns))
			columns = ", ".join(
				[f"`{col}`" for col in ['date', 'company_name', 'status', 'mobile_number', 'job_portal']]
			)
			insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

			for row in data.itertuples(index=False):
				row_values = [None if pd.isna(value) else value for value in row]
				cursor.execute(insert_query, row_values)

			connection.commit()
			print("Data uploaded successfully.")

	except Error as e:
		print("Error:", e)
	finally:
		try:
			if connection.is_connected():
				cursor.close()
				connection.close()
		except NameError:
			pass


file_path = ''
table_name = ''
host = ''
user = ''
password = ''
database = ''

upload_data_to_mysql(file_path, table_name, host, user, password, database)
