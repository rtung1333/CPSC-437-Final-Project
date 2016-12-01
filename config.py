import sqlite3
import sys
import os

def main():
	if os.path.isfile('restaurantPredictions.db'):
		print('Database already exists')
		exit()
	initdb()

def initdb():
	con = sqlite3.connect('restaurantPredictions.db')
	
	con.execute('''CREATE TABLE Users
		(UserId 		INTEGER PRIMARY KEY     AUTOINCREMENT,
			Name           TEXT    NOT NULL,
			Age            INT     NOT NULL,
			Gender        CHAR(50));''')
	print "Table created successfully";

	con.execute('''INSERT INTO Users(Name, Age, Gender)
					VALUES ('Sean', 50, 'Male');''')
	con.commit()

	users = con.execute('''SELECT * FROM Users''')
	for user in users:
		print('UserId: {}, Name: {}, Age: {}, Gender: {}').format(user[0], user[1], user[2], user[3])

	con.execute('''CREATE TABLE Restaurants
		(RestaurantId		INTEGER 	PRIMARY KEY     AUTOINCREMENT,
			Name           	TEXT   		 NOT NULL,
			Price          	INTEGER  	 NOT NULL,
			Lat        		NUMERIC		NOT NULL,
			Lng 			NUMERIC		NOT NULL,
			Rating			NUMERIC		NOT NULL);''')
	print "Table created successfully";

	con.execute('''INSERT INTO Restaurants(Name, Price, Lat, Lng, Rating)
					VALUES ('Shake Shack', 3, 1.234, 5.678, 4.5);''')
	con.commit()

	rests = con.execute('''SELECT * FROM Restaurants''')
	for rest in rests:
		print('RestaurantId: {}, Name: {}, Price: {}, Lat: {}, Lng: {}, Rating: {}').format(rest[0], rest[1], rest[2], rest[3], rest[4], rest[5])

if __name__ == "__main__":
	main()