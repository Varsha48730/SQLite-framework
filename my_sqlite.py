import sqlite3
conn = sqlite3.connect('Framework.db')
cursor = conn.cursor()

global columns,rows,table_name
global menu,saved_msg,displayed_msg,Updated_msg,deleted_msg,found_msg,not_found_msg,sort
columns = []
table_name = "Item"

def to_exit():
	exit()

def get_columns():
	cursor.execute(f"PRAGMA table_info({table_name})")
	column_data = cursor.fetchall()
	for column in column_data:
		columns.append(column[1])

def sort_records():
	global columns
	print(f"\n{columns}")
	column_name = input("Enter the column name to sort by: ")
	order = input("Enter 'ASC' for ascending or 'DESC' for descending order: ").upper()
	cursor.execute(f"SELECT * FROM {table_name} ORDER BY {column_name} {order}")	
	sorted_records = cursor.fetchall()
	print(sort)
	for record in sorted_records:
		print(record)
	print("\n")

def get_column_and_value(operation):
	column_name = input(f"Enter the column name to {operation}: ")
	column_value = input(f"Enter the value to search for in {column_name}: ")
	return column_name,column_value

def search_record(operation):
	global columns
	print(f"\n{columns}")
	column_name, search_value = get_column_and_value(operation)
	cursor.execute(f"SELECT * FROM {table_name}")
	records = cursor.fetchall()
	column_index = columns.index(column_name)
	for record in records:
		if str(record[column_index]) == search_value:
			return column_name,search_value,1
	return column_name, search_value,0

def display_records():
	print(f"\n{displayed_msg}")
	cursor.execute(f"SELECT * FROM {table_name}")
	records = cursor.fetchall()
	for record in records:
		print(record)
	print("\n")

def add_record():
	global columns
	values_list = []
	for column in columns:
		value = input(f"Enter {column}: ")
		values_list.append(f"'{value}'")
	values = ",".join(values_list)
	cursor.execute(f"INSERT INTO {table_name} VALUES({values})")
	conn.commit()
	print(f"{saved_msg}\n")

def update_record():
	operation = 'match for updating'
	column_name, search_value, returned_value = search_record(operation)
	if returned_value == 1:
		update_column = input("Enter the column name to update: ")
		new_value = input(f"Enter the new value for {update_column}: ")
		cursor.execute(f"UPDATE {table_name} SET {update_column} = '{new_value}' WHERE {column_name} = '{search_value}'")
		conn.commit()
		print(f"{Updated_msg}\n")
	else:
		print(not_found_msg)

def delete_record():
	operation = 'match for deleting'
	column_name, search_value, returned_value = search_record(operation)
	if returned_value == 1:
		cursor.execute(f"DELETE FROM {table_name} WHERE {column_name} = '{search_value}'")
		conn.commit()
		print(f"{deleted_msg}\n")
	else:
		print(not_found_msg)


choice = 0
get_columns()
cursor.execute("SELECT * FROM Itemconfig")
rows = cursor.fetchall()
for row in rows:
	if row[0] == 'menu':
		menu = row[1].replace("\\n","\n")
	elif row[0] == 'saved_msg':
		saved_msg = row[1]
	elif row[0] == 'Display_msg':
		displayed_msg = row[1]
	elif row[0] == 'updated_msg':
		Updated_msg = row[1]
	elif row[0] == 'deleted_msg':
		deleted_msg = row[1]
	elif row[0] == 'sorted_msg':
		sort = row[1]	
	elif row[0] == 'search_found':
		found_msg = row[1]
	elif row[0] == 'search_notfound':
		not_found_msg = row[1]	

while choice != 7:
	print(menu)
	choice = int(input("Enter your choice: "))
	if choice == 1:
		add_record()
	elif choice == 2:
		display_records()
	elif choice == 3:
		update_record()
	elif choice == 4:
		delete_record()
	elif choice == 5:
		operation = 'search'
		column_value, search_value, returned_value = search_record(operation)
		if returned_value == 1:
			print(found_msg)
		else:
			print(not_found_msg)
	elif choice == 6:
		sort_records()
	elif choice == 7:
		to_exit()


