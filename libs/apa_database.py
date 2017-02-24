# AutoPositionerApp for Kyle Woodsworth
# Name: Aaron Bell
# Collaborators: None
# Time Spent: 6:00

print("Hi, I'm apa_database.py!!")

import sqlite3

def open_connection():

	global conn
	global c
	conn = sqlite3.connect('mydb.db')
	c= conn.cursor()

def close_connection():

	c.close()
	conn.close()

def create_table(table1, table2=None, table3=None):

	open_connection()

	print('create_table() was called')

	c.execute('CREATE TABLE IF NOT EXISTS ' + table1 + '(machineID TEXT, modelID TEXT, machine_status INTEGER)')

	if table2 is not None:

		c.execute('CREATE TABLE IF NOT EXISTS ' + table2 + '(modelID TEXT, positionNum INTEGER)')

		if table3 is not None:

			c.execute('CREATE TABLE IF NOT EXISTS ' + table3 + '(teammate TEXT, modelID	TEXT, positionNum INTEGER)')

	print('create_table() finished')

	close_connection()

def alter_table(table_name=None, column_name=None, column_type=None, default_value=None):

	c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct} DEFAULT '{df}'"\
				.format(tn=table_name, cn=column_name, ct=column_type, df=default_value))

	''' Example use:

	alter_table('modelID_positionnum', 'teammates', 'TEXT', 'needs_positioning') '''

def insert_data(tb=None, col1=None, data1=None, col2=None, data2=None, col3=None, 	data3=None, col4=None, 	data4=None, col5=None, 	data5=None):

	print('insert_data() was called')

	open_connection()

	if tb == None: pass

	elif col1 is None: pass

	elif col1 is not None or data1 is not None:

		if col2 is not None or data2 is not None:

			if col3 is not None or data3 is not None:

				if col4 is not None or data4 is not None:

					if col5 is not None or data5 is not None:

						c.execute('INSERT INTO ' + tb + '(' + col1 + ', ' + col2 + ', ' + col3 + ', ' + col4 + ', ' + col5 + ') VALUES(?, ?, ?, ?, ?)', (data1, data2, data3, data4, data5))

					else:

						c.execute('INSERT INTO ' + tb + '(' + col1 + ', ' + col2 + ', ' + col3 + ', ' + col4 + ') VALUES(?, ?, ?, ?)', (data1, data2, data3, data4))

				else:

					c.execute('INSERT INTO ' + tb + '(' + col1 + ', ' + col2 + ', ' + col3 + ') VALUES(?, ?, ?)', (data1, data2, data3))

			else:

				c.execute('INSERT INTO ' + tb + '(' + col1 + ', ' + col2 + ') VALUES(?, ?)', (data1, data2))

		else:

			c.execute('INSERT INTO ' + tb + '(' + col1 + ') VALUES(?)', (data1,))

	conn.commit()
	close_connection()

	print('insert_data() finished')

	'''Example use:

	insert_data('machineID_modelID_status', 'machineID', 'test', 'modelID', 'test')'''

def get_data(table_name=None, specific_data=False, column_name=None, model=None,
				order_by_column=None):

	open_connection()

	if specific_data == 'column':

		c.execute('SELECT {cn} FROM {tn} ORDER BY {cn}'.\
			format(tn=table_name, cn=column_name))

	elif model is not None:

		c.execute('SELECT * FROM {tn} WHERE {cn}="{mo}" ORDER BY {ob} '.\
			format(tn=table_name, cn=column_name, mo=model, ob=order_by_column))

	elif order_by_column is not None:

		c.execute('SELECT * FROM {tn} ORDER BY {ob} DESC'.\
			format(tn=table_name, ob=order_by_column))

	else:

		c.execute('SELECT * FROM {tn}'.format(tn=table_name))

	return c.fetchall()

	close_connection()

def prepopulate_teammate_table():

	open_connection()

	c.execute('SELECT * FROM modelID_position')
	current_positions = c.fetchall()
	print(str(current_positions))

	tm_name = input("Please enter the teammates's full name: ")

	if tm_name:

		for row in current_positions:

			insert_data('teammate_modelID_positionnum', 'teammate', tm_name, 'modelID', row[0], 'positionNum', row[1])
			print(row[0], row[1])

		if input("Would you like to add another person?"):

			prepopulate_teammate_table()

	close_connection()

def position_people():

	# Get a list of all the available people

	open_connection()

	current_model = "CSEG"
	current_position = 1

	c.execute('SELECT teammate FROM teammate_modelID_positionnum WHERE modelID=? AND positionNum=?', (current_model, str(current_position)))

	available_people = c.fetchall

	print(available_people)

	# # Compare the training of each person with the list
	# c.execute('SELECT * FROM teammate_modelID_positionnum WHERE modelID=current_position)

	# if current_person in c.fetchall:
		# current_position_list += current_person

	close_connection()

def list_positions():

	open_connection()

	c.execute("SELECT * FROM machineID_modelID_status WHERE machine_status='Up'")

	# Finally getting comfortable

	# Generate a list based on models of machines that are up.

	up_machines = c.fetchall()
	global positions
	positions = []

	for machine in up_machines:

		c.execute("SELECT * FROM modelID_positionnum WHERE modelID=?", (machine[1],))

		# Where I learned to use a '?..., (tuple,)' format instead of Python vars: http://bit.ly/2l6XCY0
		# Where I learned to make the last part a tuple, not just a single item: http://bit.ly/2l7KFwp

		positions.append(c.fetchall())

	close_connection()

	#print("The positions are: " + str(positions))

	# Positions done!
def update_machine_status(machineID, status):

	'''
	When I print the below values, it gives me:

	Out: update_machine_status(machineID, status) called... values are...
	Out: update_machine_status(I-41, Up)

	'''

	print('update_machine_status(machineID, status) called... values are...')
	print('update_machine_status(' + machineID + ', ' + status + ')')

	open_connection()

	c.execute('SELECT * FROM machineID_modelID_status')
	c.execute('UPDATE machineID_modelID_status SET machine_status=? WHERE machineID=?', (status, machineID))
	conn.commit()

	close_connection()

# def update_database(table, column_to_update, value_to_update_to, where_column, where_value):

	# open_connection()

	# print('(table, column_to_update, value_to_update_to, where_column, where_value)' + str((table, column_to_update, value_to_update_to, where_column, where_value)))

	# c.execute('UPDATE ? SET {}=? WHERE {}=?'.format(column_to_update, where_column), (table, value_to_update_to, where_value))

	'''
	def update_database(table, column_to_update, value_to_update_to, where_column, where_value):

	open_connection()


	conn.commit()
	'''

	# Where I learned this command: http://bit.ly/2k6oqXw

	#close_connection()

def get_number_of_people_trained_on_each_position():

	open_connection()

	c.execute('SELECT * FROM teammate_modelID_positionnum')

	global available_people
	current_position = ('', '')
	available_people = list(set({x[0] for x in c.fetchall() if (x[1], x[2]) == current_position}))
	global number_trained_in_position
	number_trained_in_position = []


	# Where I learned to use list comprehensions properly (i.e. list only things of a certain value, that the first part is what's usually below it.): http://bit.ly/2l368uq
	# Where I learned to create sets from list comprehensions: http://bit.ly/2l3cmdE

	# print('The people currently available are: ' + str(available_people))
	# print(positions)

	for each in positions:

		# print('The current positions handled are: ' + str(each))

		for each in each:

			# print('The single current position handled is: ' + str(each))

			c.execute('SELECT * FROM teammate_modelID_positionnum WHERE modelID=? AND positionNum=? AND available="Yes"', (each[0], each[1]) )
			number_trained_in_position.append((each, len(c.fetchall())))


			# for each in c.fetchall():

				# print(each)

	from operator import itemgetter
	number_trained_in_position = sorted(number_trained_in_position, key=itemgetter(1))
	print(number_trained_in_position)

	# Where I learned to sort lists: http://bit.ly/2l3hBKz

	return number_trained_in_position

	close_connection()

def assign_people_to_positions():

	''' Every time I* do a print, do a \n\n + the thing + \n\n + a few lines of what I was trying to do, followed by another \n\n'''

	import random

	# Untaken pool

	taken = []
	current_position_pool = []
	position_chart = []


	positions_to_post_on_screen = [] # Should be a list of tuples, (name, position)
	positions_of_all_current_models = [each[0] for each in number_trained_in_position]
	print('\n\nThe positions are: ' + str(positions_of_all_current_models) + '\n\n^ ^ : Trying to see what the list of positions I*m working with are like\n\n')

	for each in positions_of_all_current_models:

		# Untaken people trained in current position pool

		c.execute('SELECT teammate FROM teammate_modelID_positionnum WHERE modelID=? AND positionNum=?', (each[0], each[1]))



		current_position = each

		#print('\n\nThe pre-for current_position_pool is: ' + str(current_position_pool) + '\n\n^ ^ : Trying to see the effect the upcoming for loop has on my current_position_pool\n\n')
		#print('\n\nThe position_chart is: ' + str(position_chart) + '\n\n^ ^ : Trying to see how the position_chart updates with each consecutive loop\n\n')

		''' Create a non-tupled list of people for the pool'''

		current_position_pool = []

		for each in c.fetchall():

			#print(each[0] + ' is trained on ' + str(current_position[0]) + str(current_position[1]))
			current_position_pool.append(each[0])

		current_position_pool = [x for x in current_position_pool if x not in taken]

		#print('\n\nCPP: ' + str(current_position_pool) + '\n\n^ ^ : Trying to see how the current_position_pool looks after the for-loop detuplified it.\n\n')

		#print('\n\nTaken: ' + str(taken) + '\n\n^ ^ : Trying to see how the taken list updates over time, and with what type of data.')

		#print('\n\nLC: ' + str([x for x in current_position_pool if x not in taken]) + '\n\n^ ^ : See the effect of the list comprehension I* was trying to work with\n\n')

		# Randomly select one person from the untaken pool

		random_select_from_untaken_current_position_pool = random.choice(current_position_pool)

		#print('\n\nMy random belongs to...: ' + random_select_from_untaken_current_position_pool + '!\n\n^ ^ : See if my random choice worked well\n\n')

		# Where I learned to pick a random item from a list: http://bit.ly/2l7pgUQ

		# Place this person on the position chart

		# print('\n\nCurrent Position + Random Select: ' + str(current_position) + ' + ' +  str(random_select_from_untaken_current_position_pool) + '\n\n^ ^ : Trying to see what values are coming in for each.\n\n')

		my_sexy_tuple = (current_position, random_select_from_untaken_current_position_pool)
		# print(str(my_sexy_tuple))
		position_chart.append(my_sexy_tuple)
		taken.append(my_sexy_tuple[1])
		untaken = current_position_pool

	#print('\n\nThe position chart so far: ' + str(position_chart) + '\n\n^ ^ : Trying to see I* want to return to my main code.\n\n')

	# Delete Untaken people trained in current position pool

	'''Done with a list compo'''

	# Remove the person positioned from the untaken pool

	'''Done with a list compo'''

	# Repeat until there are no more positions left

	'''Done with the original for loop'''

	# Keep "the untaken" (haha, good movie title) in its own list


	# Choose randomly from every untaken person available and trained in it
	# Remove this person from the untaken pool

	return position_chart

	# How I learned to return from functions properly: http://bit.ly/1yn6OfQ



create_table('machineID_modelID_status', 'modelID_positionnum', 'teammate_modelID_positionnum')

list_positions()
get_number_of_people_trained_on_each_position()
assign_people_to_positions()
update_machine_status('I-39', 'Down')

# Python's guide that will probably help me learn fetchone and executemany: http://bit.ly/2kvtKXY
# Best SQLite3 guide to-date: http://bit.ly/2l2jsv4
# On listing tables: http://bit.ly/2k50OVC
